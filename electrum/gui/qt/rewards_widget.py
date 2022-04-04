from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QVBoxLayout, QLabel, QPushButton, QWidget, QHBoxLayout

from .rewards_list import available_predicted_rewards_list, refresh_available_rewards_window, \
    refresh_predicted_rewards_window, governance_power_controller, refresh_governance_power_window, \
    governance_power_list, free_limit_list, free_limit_window
from .staking.utils import get_sum_available_rewards, get_sum_predicted_rewards
from .util import WindowModalDialog
from ...i18n import _


class Section:
    TITLE_LABEL = None

    def __init__(self, root_widget, wallet, predicted_rewards=None):
        self._wallet = wallet
        self.predicted_rewards = predicted_rewards
        self._text = None
        self._root_widget = root_widget

        self._section_layout = QVBoxLayout()
        self._section_layout.setContentsMargins(-1, 2, -1, 2)
        spacer_item = QSpacerItem(6, 6, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self._title_label = QLabel(root_widget)
        self._title_label.setAlignment(Qt.AlignCenter)
        title_label_font = QtGui.QFont()
        title_label_font.setBold(True)
        title_label_font.setWeight(75)
        self._title_label.setFont(title_label_font)
        self._title_label.setText(self.TITLE_LABEL)
        self._section_layout.addWidget(self._title_label)

        self._value_label = QLabel(root_widget)
        self._value_label.setAlignment(QtCore.Qt.AlignCenter)
        self._section_layout.addWidget(self._value_label)

        self._button_layout = QVBoxLayout()
        self._section_layout.addLayout(self._button_layout)

        self._details_button = QPushButton()
        self._button_layout.addWidget(self._details_button, alignment=Qt.AlignCenter)
        self._details_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._details_button.setText('Details')
        self._details_button.clicked.connect(lambda: self.display_detail_popup())
        self._section_layout.addItem(spacer_item)

    def display_detail_popup(self):
        raise NotImplemented()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self._value_label.setText(value)

    @property
    def layout(self):
        return self._section_layout


class RewardPopup(WindowModalDialog):
    def __init__(self, parent, title, text, table=None):
        super().__init__(parent)
        self.setEnabled(True)
        self._setup_window()

        self.main_layout = self.create_main_layout()
        self.title_label = self._setup_title(title=title)
        self.text_label = self._setup_text(main_text=text)
        if table is not None:
            self._setup_table(table=table)

    def create_main_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        return main_layout

    def _setup_window(self):
        self.setMinimumSize(QtCore.QSize(440, 400))
        self.setMaximumSize(QtCore.QSize(440, 400))
        self.setBaseSize(QtCore.QSize(440, 400))

    def _setup_title(self, title):
        title_label = QLabel()
        title_label.setMinimumSize(QtCore.QSize(0, 40))
        title_label.setMaximumSize(QtCore.QSize(16777215, 40))
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        title_label_text = QtGui.QFont()
        title_label_text.setBold(True)
        title_label_text.setPointSize(16)

        title_label.setFont(title_label_text)
        title_label.setText(title)

        self.main_layout.addWidget(title_label)

        return title_label

    def _setup_text(self, main_text):
        text_label = QLabel()
        text_label.setWordWrap(True)
        text_label.setText(main_text)

        self.main_layout.addWidget(text_label)

        return text_label

    def _setup_table(self, table):
        self.main_layout.addWidget(table)


class AvailableRewardsSection(Section):
    TITLE_LABEL = 'Available reward'

    def __init__(self, root_widget, wallet):
        super().__init__(root_widget, wallet)

    def display_detail_popup(self):
        available_reward_popup = RewardPopup(
            parent=self._root_widget,
            title='Available Rewards',
            text=_(
                "Check the details of the rewards you can already claim. "
                "These are your guaranteed payouts, so you can already "
                "start thinking about what you will spend them on."
            ),
            table=available_predicted_rewards_list
        )

        refresh_available_rewards_window(wallet=self._wallet)
        available_reward_popup.open()


class TotalPredictedStakingRewardSection(Section):
    TITLE_LABEL = 'Total predicted staking reward'

    def display_detail_popup(self):
        predicted_staking_popup = RewardPopup(
            parent=self._root_widget,
            title='Predicted staking rewards',
            text=_(
                "Check the details of your predicted rewards. The "
                "payout amount is dependent on multiple factors and "
                "may change dynamically, so don't plan what you will "
                "buy with it just yet."
            ),
            table=available_predicted_rewards_list
        )
        refresh_predicted_rewards_window(wallet=self._wallet)
        predicted_staking_popup.open()


class GovernancePowerSection(Section):
    TITLE_LABEL = 'Governance Power'

    def display_detail_popup(self):
        governance_power_popup = RewardPopup(
            parent=self._root_widget,
            title='Governance Power',
            text=_(
                "Governance Power lets you decide on the future of"
                "Electric Cash.\n\n"
                "You can use it to vote on important community issues"
                "and propose your own improvements.\n\n"
                "To cast a vote, you need GP points earned through"
                "staking. You will see and use them here when Governance"
                "Power become available."
            ),
            table=governance_power_list
        )
        refresh_governance_power_window()
        governance_power_popup.open()


class RewardsWidget(QWidget):
    def __init__(self, wallet, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._main_layout = QHBoxLayout(self)
        self.wallet = wallet
        spacer_item = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self._main_layout.addItem(spacer_item)
        self._available_section = AvailableRewardsSection(root_widget=self, wallet=self.wallet)
        self._main_layout.addLayout(self._available_section.layout)
        self._main_layout.addItem(spacer_item)

        self._predicted_section = TotalPredictedStakingRewardSection(root_widget=self, wallet=self.wallet, )
        self._main_layout.addLayout(self._predicted_section.layout)
        self._main_layout.addItem(spacer_item)

        self._governance_power_section = GovernancePowerSection(root_widget=self, wallet=self.wallet)
        self._main_layout.addLayout(self._governance_power_section.layout)
        self._main_layout.addItem(spacer_item)

    def set_available_rewards_text(self, value):
        self._available_section.text = f'{value:.8f} ELCASH'

    def set_total_predicted_staking_reward_text(self, value):
        self._predicted_section.text = f'{value:.8f} ELCASH'

    def set_governance_power_text(self, value):
        self._governance_power_section.text = f'{value} GP'

    def update(self):
        self.set_available_rewards_text(value=get_sum_available_rewards(self.wallet))
        self.set_total_predicted_staking_reward_text(value=get_sum_predicted_rewards(self.wallet))
        self.set_governance_power_text(value='14200(mock)')
