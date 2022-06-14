from datetime import datetime, timedelta
from decimal import Decimal
from typing import TYPE_CHECKING

from electrum.network import TxBroadcastError, BestEffortRequestFailed
from electrum.staking.tx_type import TxType
from electrum.wallet import Abstract_Wallet
from electrum.logging import get_logger

if TYPE_CHECKING:
    from electrum import Network, Transaction

_logger = get_logger(__name__)

from PyQt5.QtWidgets import QMessageBox

def broadcast_transaction(network: 'Network', tx: 'Transaction'):
    try:
        network.run_from_another_thread(network.broadcast_transaction(tx))
    except TxBroadcastError as e:
        msg = f'Broadcasting transaction to network failed. {e}; txid: {tx.txid()}'
        _logger.error(msg)
        QMessageBox.critical(None, "Broadcasting Error",msg)
    except BestEffortRequestFailed as e:
        msg = f'No network found. {e}; txid: {tx.txid()}'
        _logger.error(msg)
        QMessageBox.critical(None, "Best Effort Request Failed",msg)


def get_data_for_available_rewards_tab(wallet: Abstract_Wallet):
    transactions = wallet.db.transactions

    payout_dates = []
    amounts = []
    status = []

    for t in transactions:
        if transactions[t].tx_type.name == 'STAKING_DEPOSIT' \
                and transactions[t].staking_info is not None \
                and transactions[t].staking_info.fulfilled and not transactions[t].staking_info.paid_out \
                and not (hasattr(wallet, 'in_claiming') and t in wallet.in_claiming):
            finish_height = transactions[t].staking_info.deposit_height + transactions[t].staking_info.staking_period
            block_header = wallet.network.run_from_another_thread(
                wallet.network.get_block_header(finish_height, 'catchup'))
            payout_dates.append(datetime.fromtimestamp(block_header['timestamp']).strftime("%Y-%m-%d"))
            amount = f"{transactions[t].staking_info.accumulated_reward:.8f}"
            amounts.append(
                amount
            )
            status.append("Ready to Claim")

    return payout_dates, amounts, status


def get_all_stake_amount(wallet: Abstract_Wallet):
    transactions = wallet.db.transactions
    amount = 0
    for t in transactions:
        if (
                transactions[t].tx_type == TxType.STAKING_DEPOSIT
                and transactions[t].staking_info
                and not transactions[t].staking_info.paid_out
        ):
            amount += transactions[t].staking_info.staking_amount

    return amount


def get_sum_available_rewards(wallet: Abstract_Wallet):
    transactions = wallet.db.transactions
    av = 0
    for t in transactions:
        if (
                transactions[t].tx_type == TxType.STAKING_DEPOSIT
                and transactions[t].staking_info
                and transactions[t].staking_info.fulfilled
                and not transactions[t].staking_info.paid_out
                and not (hasattr(wallet, 'in_claiming') and t in wallet.in_claiming)
        ):
            av += transactions[t].staking_info.accumulated_reward
    return av

def _get_estimated_reward(staking_settings, wallet, tx):
    blocks_in_year = 51840  # 360 * 24 * 6
    intrest_info = staking_settings['interestInfo']
    percent_per_year = intrest_info[str(tx.staking_info.staking_period)]
    current_height = wallet.network.get_server_height()
    stake_amount = tx.staking_info.staking_amount
    stake_period = tx.staking_info.staking_period
    stake_deposit_height = tx.staking_info.deposit_height
    stake_accumulated_reward = tx.staking_info.accumulated_reward

    estimated_max_reward = stake_amount * Decimal(percent_per_year) * stake_period / blocks_in_year
    mined_blocks = current_height - stake_deposit_height + 1

    if mined_blocks == 0:
        return 0

    estimated_max_current_reward = estimated_max_reward * Decimal(mined_blocks / stake_period)
    estimated_reward = estimated_max_reward * stake_accumulated_reward / estimated_max_current_reward

    return estimated_reward

def get_predicted_reward(wallet: Abstract_Wallet, tx):
    staking_settings = wallet.network.run_from_another_thread(wallet.network.get_staking_info())

    return _get_estimated_reward(staking_settings, wallet, tx)

def get_sum_predicted_rewards(wallet: Abstract_Wallet):
    staking_settings = wallet.network.run_from_another_thread(
        wallet.network.get_staking_info()
                                                              )
    transactions = wallet.db.transactions
    pr = 0

    for t in transactions:
        tx = transactions[t]
        if (
                tx.tx_type == TxType.STAKING_DEPOSIT
                and tx.staking_info
                and not tx.staking_info.fulfilled
                and not tx.staking_info.paid_out
        ):

            pr += _get_estimated_reward(staking_settings, wallet, tx)
    return pr

def get_governance_power(wallet: Abstract_Wallet):
    res = wallet.network.run_from_another_thread(
        wallet.network.get_govpower(
            address=wallet.get_staking_address()
            )
        )
    return res

def get_predicted_rewards_data(wallet: Abstract_Wallet):
    amounts = []
    payout_dates = []
    status = []

    transactions = wallet.db.transactions
    verified_tx = wallet.db.verified_tx
    staking_settings = wallet.network.run_from_another_thread(wallet.network.get_staking_info())
    current_height = wallet.network.get_server_height()
    for t in transactions:
        tx = transactions[t]
        if (
                transactions[t].tx_type == TxType.STAKING_DEPOSIT
                and transactions[t].staking_info
                and not transactions[t].staking_info.fulfilled
                and not transactions[t].staking_info.paid_out
        ):

            pr = _get_estimated_reward(staking_settings, wallet, tx)

            amounts.append(f'{pr:0.8f}')

            payout_date = datetime.fromtimestamp(verified_tx[t][1]) + timedelta(tx.staking_info.staking_period / 144)
            payout_dates.append(payout_date.strftime("%Y-%m-%d"))
            status.append('Stake')
    return payout_dates, amounts, status