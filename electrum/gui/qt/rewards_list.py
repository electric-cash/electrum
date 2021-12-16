from datetime import datetime, timedelta

from ...common.services import CustomTableWidgetController
from ...common.widgets import CustomTableWidget
from ...staking.tx_type import TxType
from ...wallet import Abstract_Wallet


class AvailablePredictedRewardsList(CustomTableWidget):
    pass


def refresh_available_rewards_window(wallet: Abstract_Wallet):
    payoudates, amounts, status = get_data_for_available_rewards_tab(wallet)

    available_predicted_rewards_controller.insert_data(
        table_data={
            'Payout date': payoudates,
            'Amount': amounts,
            'Status': status
        }
    )


def get_data_for_available_rewards_tab(wallet: Abstract_Wallet):
    transactions = wallet.db.transactions
    # verified_tx = wallet.db.verified_tx

    payout_dates = []
    amounts = []
    status = []

    for t in transactions:
        if transactions[t].tx_type.name == 'STAKING_DEPOSIT' \
                and transactions[t].staking_info.fulfilled and not transactions[t].staking_info.paid_out:
            finish_height = transactions[t].staking_info.deposit_height + transactions[t].staking_info.staking_period
            block_header = wallet.network.run_from_another_thread(wallet.network.get_block_header(finish_height, 'catchup'))
            payout_dates.append(datetime.fromtimestamp(block_header['timestamp']).strftime("%Y-%m-%d"))
            amounts.append(
                transactions[t].staking_info.accumulated_reward
            )
            status.append("Ready to Claim")

    return payout_dates, amounts, status


def refresh_predicted_rewards_window(wallet: Abstract_Wallet, data: dict):
    payout_dates, amounts, status = get_predicted_rewards_data(wallet=wallet)
    available_predicted_rewards_controller.insert_data(table_data={
        'Payout date': payout_dates,
        'Amount': amounts,
        'Status': status,
    })


def get_predicted_rewards_data(wallet: Abstract_Wallet):
    amounts = []
    payout_dates = []
    status = []

    transactions = wallet.db.transactions
    verified_tx = wallet.db.verified_tx
    staking_info = wallet.network.run_from_another_thread(wallet.network.get_staking_info())
    period_info = staking_info['interestInfo']
    current_height = wallet.network.get_server_height()
    for t in transactions:
        tx = transactions[t]
        if tx.tx_type == TxType.STAKING_DEPOSIT and not tx.staking_info.fulfilled and not tx.staking_info.paid_out:
            max_reward = tx.staking_info.staking_amount * (period_info[str(tx.staking_info.staking_period)] * tx.staking_info.staking_period / 51840)
            completed_period = (current_height - tx.staking_info.deposit_height) / tx.staking_info.staking_period
            max_current_reward = max_reward * completed_period
            pr = max_reward * max_current_reward / tx.staking_info.accumulated_reward
            amounts.append(pr)
            payout_date = datetime.fromtimestamp(verified_tx[t][1]) + timedelta(tx.staking_info.staking_period / 144)
            payout_dates.append(payout_date.strftime("%Y-%m-%d"))
            status.append('Stake')
    return payout_dates, amounts, status


available_predicted_rewards_list = AvailablePredictedRewardsList(
    column_names=['Payout date', 'Amount', 'Status'],
)

available_predicted_rewards_controller = CustomTableWidgetController(table_widget=available_predicted_rewards_list)


#####
class GovernancePowerList(CustomTableWidget):
    pass


def refresh_governance_power_window():
    governance_power_controller.insert_data(table_data={
        'Date': ['2021-12-12', '2021-12-12'],
        'Total reward': ['11111.00000001', '1'],
    })


governance_power_list = GovernancePowerList(
    column_names=['Date', 'Total reward'],
)

governance_power_controller = CustomTableWidgetController(table_widget=governance_power_list)


class FreeLimitList(CustomTableWidget):
    pass


def free_limit_window():
    free_limit_controller.insert_data(table_data={
        'Payout date': ['2021-12-12', '2021-12-12'],
        'Total reward': ['1000 bytes', '1bytes'],
    })


free_limit_list = FreeLimitList(
    column_names=['Payout date', 'Total reward'],
)

free_limit_controller = CustomTableWidgetController(table_widget=free_limit_list)
