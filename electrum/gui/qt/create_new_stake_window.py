#!/usr/bin/env python
#
# Electrum - lightweight Bitcoin client
# Copyright (C) 2015 Thomas Voegtlin
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import TYPE_CHECKING

from PyQt5 import QtCore, QtWidgets, QtGui

from electrum.gui.qt.util import WindowModalDialog, PasswordLineEdit
from electrum.i18n import _
from electrum.logging import get_logger

_logger = get_logger(__name__)


class CreateNewStakingWindow(WindowModalDialog):

    def __call__(self, *args, **kwargs):
        self.value_change()
        self.open()

    def __init__(self, parent, min_amount=5, default_period=30, default_amount=5):

        super().__init__(parent)
        self.parent = parent
        self.min_amount = min_amount
        self.stake_value = 0
        self.period_days = default_period
        self.default_amount = default_amount
        self.setEnabled(True)
        self.setMinimumSize(QtCore.QSize(440, 400))
        self.setMaximumSize(QtCore.QSize(440, 400))
        self.setBaseSize(QtCore.QSize(440, 400))
        self.setWindowTitle(_("Create New Stake"))
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.Main_v_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.Main_v_layout.setContentsMargins(10, 10, 10, 10)
        self.Main_v_layout.setSpacing(10)

        self.setup_title()
        self.setup_description()
        self.setup_amount()
        self.setup_radios()
        self.setup_rewards()
        self.setup_description2()
        self.setup_next_cancel_buttons()

    def setup_title(self):
        self.title = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.title.setText(_("Create New Stake"))
        self.title.setMinimumSize(QtCore.QSize(300, 0))
        self.title.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.Main_v_layout.addWidget(self.title)

    def setup_description(self):
        self.description_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.description_label.setText(
            _("Sed ut perspiciatis, unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, "
              "totam rem aperiam eaque ipsa, "))
        self.description_label.setMinimumSize(QtCore.QSize(300, 0))
        self.description_label.setMaximumSize(QtCore.QSize(900, 60))
        self.description_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.description_label.setWordWrap(True)
        self.description_label.setIndent(-1)
        self.description_label.setOpenExternalLinks(False)
        self.Main_v_layout.addWidget(self.description_label)

    def setup_amount(self):
        self.amount_value_error_label = QtWidgets.QLabel()
        self.amount_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.spinBox_amount = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget)
        self.period_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.gridLayout = QtWidgets.QGridLayout()
        self.period_label.setText(_("Period"))
        self.gridLayout.addWidget(self.period_label, 3, 0, 1, 1)
        self.spinBox_amount.setDecimals(8)
        self.spinBox_amount.setRange(self.min_amount, self.get_spendable_coins())
        self.spinBox_amount.setValue(self.default_amount)
        self.spinBox_amount.valueChanged.connect(self.value_change)

        self.gridLayout.addWidget(self.spinBox_amount, 0, 1, 1, 4)
        self.amount_label.setText(_("Amount"))
        self.gridLayout.addWidget(self.amount_label, 0, 0, 1, 1)

        self.amount_value_error_label.setText(_(f"The minimum stake value is {self.min_amount} ELCASH"))
        self.amount_value_error_label.setStyleSheet('color: red')
        self.amount_value_error_label.hide()

        if not self.valid_enough_coins(min_coins=self.min_amount):
            self.amount_value_error_label.show()

        self.gridLayout.addWidget(self.amount_value_error_label, 1, 0, 1, 5)

    def setup_radios(self):
        self.radio30 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radio90 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radio180 = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radio360 = QtWidgets.QRadioButton(self.verticalLayoutWidget)

        self.radio30.setText(_("30 Days"))
        if self.period_days == 30:
            self.radio30.setChecked(True)
        self.radio30.toggled.connect(lambda: self.radio_state(self.radio30))
        self.radio30.toggled.connect(self.value_change)
        self.gridLayout.addWidget(self.radio30, 3, 1, 1, 1)
        self.radio90.setText(_("90 Days"))
        if self.period_days == 90:
            self.radio90.setChecked(True)
        self.radio90.toggled.connect(lambda: self.radio_state(self.radio90))
        self.radio90.toggled.connect(self.value_change)
        self.gridLayout.addWidget(self.radio90, 3, 2, 1, 1)
        self.radio180.setText(_("180 Days"))
        if self.period_days == 180:
            self.radio180.setChecked(True)
        self.radio180.toggled.connect(lambda: self.radio_state(self.radio180))
        self.radio180.toggled.connect(self.value_change)
        self.gridLayout.addWidget(self.radio180, 3, 3, 1, 1)
        self.radio360.setText(_("360 Days"))
        if self.period_days == 360:
            self.radio360.setChecked(True)
        self.radio360.toggled.connect(lambda: self.radio_state(self.radio360))
        self.radio360.toggled.connect(self.value_change)
        self.gridLayout.addWidget(self.radio360, 3, 4, 1, 1)

        self.Main_v_layout.addLayout(self.gridLayout)

    def setup_rewards(self):
        self.estimate_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.pred_rew = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.free_trans_label = QtWidgets.QLabel()
        self.gp_value_label = QtWidgets.QLabel()
        self.rewards_text_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.vl_rewards = QtWidgets.QVBoxLayout()

        self.vl_rewards.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.rewards_text_label.setText(_("Guaranteed rewards:"))
        self.rewards_text_label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.vl_rewards.addWidget(self.rewards_text_label)
        self.gp_value_label.setText(
            _("Governance Power: ") + str(self.spinBox_amount.value() * self.period_days * 0.008) + ' GP')
        self.gp_value_label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.vl_rewards.addWidget(self.gp_value_label)
        self.free_trans_label.setText(
            _("Daily free transactions limit:") + str(self.spinBox_amount.value() * self.period_days * 0.01) +
            ' bytes')
        self.free_trans_label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.vl_rewards.addWidget(self.free_trans_label)
        spacer_item = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.vl_rewards.addItem(spacer_item)
        self.pred_rew.setText(_("Predicted Rewords:"))
        self.pred_rew.setMaximumSize(QtCore.QSize(16777215, 30))
        self.pred_rew.setBaseSize(QtCore.QSize(0, 30))
        self.vl_rewards.addWidget(self.pred_rew)
        self.estimate_label.setText(
            _("Estimated payout: ") + str(self.spinBox_amount.value() * self.period_days * 0.21) + ' ELCASH')
        self.estimate_label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.vl_rewards.addWidget(self.estimate_label)
        self.Main_v_layout.addLayout(self.vl_rewards)

    def setup_description2(self):
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.description2_label = QtWidgets.QLabel()
        self.terms_button = QtWidgets.QPushButton()

        self.description2_label.setText(_("Click Next to go confirmation view. "))
        self.description2_label.setMaximumSize(QtCore.QSize(16777215, 50))
        self.Main_v_layout.addWidget(self.description2_label)
        self.gridLayout_2.setSpacing(2)
        self.terms_button.setText(_("Terms & Conditions"))
        self.terms_button.setMaximumSize(QtCore.QSize(140, 16777215))
        font = QtGui.QFont()
        font.setUnderline(True)
        self.terms_button.setFont(font)
        self.terms_button.setText(_("Terms & Conditions"))
        self.terms_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.terms_button.setStyleSheet("border: none;")
        self.terms_button.setAutoDefault(True)
        self.gridLayout_2.addWidget(self.terms_button, 0, 1, 1, 1)

    def setup_next_cancel_buttons(self):
        self.next_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.cancel_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        spacer_item1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacer_item1)
        self.cancel_button.setText(_("Cancel"))
        self.cancel_button.clicked.connect(self.on_push_cancel_button)
        self.cancel_button.setMaximumSize(QtCore.QSize(60, 16777215))
        self.cancel_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.horizontalLayout.addWidget(self.cancel_button)
        self.next_button.setText(_("Next"))

        if not self.valid_enough_coins(self.min_amount):
            self.next_button.setEnabled(False)

        self.next_button.setMaximumSize(QtCore.QSize(60, 16777215))
        self.next_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.next_button.clicked.connect(self.on_push_next_button)
        self.horizontalLayout.addWidget(self.next_button)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 5, 1, 2)
        self.Main_v_layout.addLayout(self.gridLayout_2)

    def on_push_next_button(self):
        if self.valid_enough_coins(min_coins=self.spinBox_amount.value()):
            self.dialog = dialog = CreateNewStakingTwo(parent=self)
            dialog.show()
            self.hide()

    def on_push_cancel_button(self):
        self.close()

    def value_change(self):
        self.spinBox_amount.setRange(self.min_amount, self.get_spendable_coins())

        if self.valid_enough_coins(min_coins=self.spinBox_amount.value()):
            self.amount_value_error_label.hide()
            self.next_button.setEnabled(True)
        else:
            self.amount_value_error_label.show()
            self.next_button.setEnabled(False)

        self.estimate_label.setText(
            _("Estimated payout: ") +
            str(self.spinBox_amount.value() * self.period_days * 0.21) +
            ' ELCASH')

        self.free_trans_label.setText(
            _("Daily free transactions limit:") +
            str(self.spinBox_amount.value() * self.period_days * 0.017) +
            ' bytes')

        self.gp_value_label.setText(
            _("Governance Power: ") +
            str(self.spinBox_amount.value() * self.period_days * 0.008) +
            ' GP')

    def get_period_blocks(self):
        return self.period_days * 144

    def radio_state(self, b):
        if not b.isChecked():
            return
        elif b.text() == "30 Days":
            self.period_days = 30
        elif b.text() == "90 Days":
            self.period_days = 90
        elif b.text() == "180 Days":
            self.period_days = 180
        elif b.text() == "360 Days":
            self.period_days = 360

    def valid_enough_coins(self, min_coins):
        return self.get_spendable_coins() >= min_coins

    def get_spendable_coins(self):
        coins = sum((i._trusted_value_sats for i in self.parent.wallet.get_spendable_coins(None, nonlocal_only=True)))
        return coins * 0.00000001


class CreateNewStakingTwo(WindowModalDialog):

    def __call__(self, *args, **kwargs):
        self.show()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.wallet = parent.parent.wallet
        self.password_required = self.wallet.has_keystore_encryption()
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setEnabled(True)
        self.setMinimumSize(QtCore.QSize(420, 500))
        self.setMaximumSize(QtCore.QSize(420, 500))
        self.setWindowTitle("Create New Stake")
        self.main_box = QtWidgets.QVBoxLayout(self)

        self.title = QtWidgets.QLabel()
        self.setup_title()

        self.data_grid_box = QtWidgets.QGridLayout()
        self.payout_label_2 = QtWidgets.QLabel()

        self.amount_label = QtWidgets.QLabel()
        self.period_label = QtWidgets.QLabel()
        self.period_text_label = QtWidgets.QLabel()
        self.block_label_2 = QtWidgets.QLabel()
        self.gp_label_2 = QtWidgets.QLabel()
        self.g_reward = QtWidgets.QLabel()
        self.amount_label_2 = QtWidgets.QLabel()
        self.fee_label = QtWidgets.QLabel()
        self.fee_label_2 = QtWidgets.QLabel()
        self.gp_label = QtWidgets.QLabel()
        self.rewards_label = QtWidgets.QLabel()
        self.block_label = QtWidgets.QLabel()
        self.payout_label = QtWidgets.QLabel()
        self.setup_detail()
        self.setup_rewards()

        self.penalty_label = QtWidgets.QLabel()
        self.description_label = QtWidgets.QLabel()
        self.setup_description()

        self.password_layout = QtWidgets.QHBoxLayout()
        self.password_label = QtWidgets.QLabel()
        self.password_lineEdit = PasswordLineEdit()
        self.password_error_label = QtWidgets.QLabel()
        self.setup_password_label()

        self.text_tabel = QtWidgets.QLabel()
        self.button_layout = QtWidgets.QHBoxLayout()
        self.back_button = QtWidgets.QPushButton()
        self.cancel_button = QtWidgets.QPushButton()
        self.send_button = QtWidgets.QPushButton()
        self.setup_buttons()

    def setup_title(self):
        self.title.setText(_("Staking Detail"))
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(size_policy)
        self.title.setMaximumSize(QtCore.QSize(600, 35))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.main_box.addWidget(self.title)

    def setup_detail(self):
        self.payout_label_2.setText(
            str(self.parent.spinBox_amount.value() * self.parent.period_days * 0.021) +
            ' ELCASH'
        )
        self.data_grid_box.addWidget(self.payout_label_2, 7, 1, 1, 1)
        self.gp_label_2.setText(str(self.parent.spinBox_amount.value() * self.parent.period_days * 0.008) + ' GP')
        self.data_grid_box.addWidget(self.gp_label_2, 4, 1, 1, 1)
        self.payout_label.setText(_("Estimated payout:"))
        self.data_grid_box.addWidget(self.payout_label, 7, 0, 1, 1)
        self.block_label.setText(_("Block required:"))
        self.data_grid_box.addWidget(self.block_label, 2, 0, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.rewards_label.setFont(font)
        self.rewards_label.setText(_("Predicted rewards:"))
        self.data_grid_box.addWidget(self.rewards_label, 6, 0, 1, 1)
        self.gp_label.setText(_("Governance Power:"))
        self.data_grid_box.addWidget(self.gp_label, 4, 0, 1, 1)
        self.fee_label_2.setText(_("Daily free transactions limit:"))
        self.data_grid_box.addWidget(self.fee_label_2, 5, 0, 1, 1)

        self.fee_label.setText(
            str(self.parent.spinBox_amount.value() * self.parent.period_days * 0.017) +
            ' bytes')
        self.data_grid_box.addWidget(self.fee_label, 5, 1, 1, 1)
        amount = self.parent.spinBox_amount.value()
        self.amount_label_2.setText(str(amount) + _(" Elcash"))
        self.data_grid_box.addWidget(self.amount_label_2, 0, 1, 1, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.g_reward.setFont(font)

    def setup_rewards(self):
        self.g_reward.setText(_("Guaranted rewards:"))
        self.data_grid_box.addWidget(self.g_reward, 3, 0, 1, 1)
        self.block_label_2.setText(str(self.parent.get_period_blocks()))
        self.data_grid_box.addWidget(self.block_label_2, 2, 1, 1, 1)
        self.period_text_label.setText(_("Period:"))
        self.data_grid_box.addWidget(self.period_text_label, 1, 0, 1, 1)
        self.period_label.setText(str(self.parent.period_days) + _(" days"))
        self.data_grid_box.addWidget(self.period_label, 1, 1, 1, 1)
        self.amount_label.setText(_("Amount to be staked:"))
        self.data_grid_box.addWidget(self.amount_label, 0, 0, 1, 1)
        self.main_box.addLayout(self.data_grid_box)

    def setup_description(self):
        self.penalty_label.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.penalty_label.setFont(font)
        self.penalty_label.setText(_("PENALTY"))
        self.main_box.addWidget(self.penalty_label)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(239, 41, 41))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 41, 41))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.description_label.setPalette(palette)
        self.description_label.setText(_("If you unstake this transaction ealier you will be charged 3% as "
                                         "penality and you will loose daily free transaction limit."))
        self.description_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.description_label.setWordWrap(True)
        self.main_box.addWidget(self.description_label)

    def setup_password_label(self):
        self.password_label.setText(_("Password:"))
        self.password_label.setMaximumSize(QtCore.QSize(16777215, 40))
        self.password_layout.addWidget(self.password_label)
        self.password_lineEdit.setText("")
        self.password_layout.addWidget(self.password_lineEdit)
        self.main_box.addLayout(self.password_layout)
        self.password_error_label.setText(_("incorrect password"))
        self.password_error_label.setStyleSheet('color: red')
        self.main_box.addWidget(self.password_error_label)
        self.password_error_label.hide()

        if not self.password_required:
            self.password_label.hide()
            self.password_lineEdit.hide()

    def setup_buttons(self):
        self.text_tabel.setText(_("Click Send to proceed"))
        self.main_box.addWidget(self.text_tabel)
        spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.button_layout.addItem(spacer_item)
        self.back_button.setText(_("Back"))
        self.back_button.clicked.connect(self.on_push_back_button)
        self.button_layout.addWidget(self.back_button)
        self.cancel_button.setText(_("Cancel"))
        self.cancel_button.clicked.connect(self.on_push_cancel_button)
        self.button_layout.addWidget(self.cancel_button)
        self.send_button.setText(_("Send"))
        self.send_button.clicked.connect(self.on_push_send_window)
        self.button_layout.addWidget(self.send_button)
        self.main_box.addLayout(self.button_layout)

    def on_push_back_button(self):
        dialog = self.parent
        dialog.show()
        self.hide()

    def on_push_cancel_button(self):
        self.close()

    def on_push_send_window(self):
        password = self.password_lineEdit.text() or None
        if self.password_required:
            if password is None:
                return
            try:
                self.wallet.check_password(password)
            except Exception as e:
                self.password_error_label.show()
                self.password_lineEdit.setStyleSheet("background-color: red;")
                return

        self.is_send = True
        self.hide()
        dialog = CreateNewStakingFinish(parent=self)
        dialog.show()


class CreateNewStakingFinish(WindowModalDialog):

    def __call__(self, *args, **kwargs):
        self.show()

    def __init__(self, parent, transaction_id='(this should be tx hash)'):
        super().__init__(parent)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setEnabled(True)
        self.setMinimumSize(QtCore.QSize(720, 100))
        self.setMaximumSize(QtCore.QSize(720, 100))
        self.setWindowTitle(_("Create New Stake"))
        self.main_box = QtWidgets.QVBoxLayout(self)
        self.info_label = QtWidgets.QLabel()
        self.info_label.setText(_("Succes!"))
        self.main_box.addWidget(self.info_label)
        self.info_label1 = QtWidgets.QLabel()
        self.info_label1.setText(_("Transaction ID:") + transaction_id)
        self.main_box.addWidget(self.info_label1)
        self.button_layout = QtWidgets.QHBoxLayout()
        spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.button_layout.addItem(spacer_item)
        self.cancel_button = QtWidgets.QPushButton()
        self.cancel_button.setText(_("View in explorer"))
        self.cancel_button.clicked.connect(self.on_push_explorer_button)
        self.button_layout.addWidget(self.cancel_button)
        self.ok_button = QtWidgets.QPushButton()
        self.ok_button.setText(_("ok"))
        self.ok_button.clicked.connect(self.on_push_ok_button)
        self.button_layout.addWidget(self.ok_button)
        self.main_box.addLayout(self.button_layout)

    def on_push_explorer_button(self):
        url = QtCore.QUrl("https://explorer.electriccash.global/")
        QtGui.QDesktopServices.openUrl(url)
        self.close()

    def on_push_ok_button(self):
        self.close()
