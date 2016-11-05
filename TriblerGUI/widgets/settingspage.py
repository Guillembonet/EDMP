import json
from PyQt5.QtWidgets import QWidget

from TriblerGUI.defs import PAGE_SETTINGS_GENERAL, PAGE_SETTINGS_CONNECTION, PAGE_SETTINGS_BANDWIDTH, \
    PAGE_SETTINGS_SEEDING, PAGE_SETTINGS_ANONYMITY, BUTTON_TYPE_NORMAL
from TriblerGUI.dialogs.confirmationdialog import ConfirmationDialog
from TriblerGUI.tribler_request_manager import TriblerRequestManager
from TriblerGUI.utilities import seconds_to_string


class SettingsPage(QWidget):
    """
    This class is responsible for displaying and adjusting the settings present in Tribler.
    """

    def initialize_settings_page(self):
        self.window().settings_tab.initialize()
        self.window().settings_tab.clicked_tab_button.connect(self.clicked_tab_button)
        self.window().settings_save_button.clicked.connect(self.save_settings)

        self.window().developer_mode_enabled_checkbox.stateChanged.connect(self.on_developer_mode_checkbox_changed)
        self.window().always_ask_location_checkbox.stateChanged.connect(self.on_always_ask_location_checkbox_changed)

        self.settings = None

    def on_developer_mode_checkbox_changed(self, event):
        self.window().gui_settings.setValue("debug", self.window().developer_mode_enabled_checkbox.isChecked())
        self.window().left_menu_button_debug.setHidden(not self.window().developer_mode_enabled_checkbox.isChecked())

    def on_always_ask_location_checkbox_changed(self, event):
        should_hide = self.window().always_ask_location_checkbox.isChecked()
        self.window().default_download_settings_header.setHidden(should_hide)
        self.window().download_settings_anon_label.setHidden(should_hide)
        self.window().download_settings_anon_checkbox.setHidden(should_hide)
        self.window().download_settings_anon_seeding_label.setHidden(should_hide)
        self.window().download_settings_anon_seeding_checkbox.setHidden(should_hide)

    def initialize_with_settings(self, settings):
        self.settings = settings
        settings = settings["settings"]

        # General settings
        self.window().developer_mode_enabled_checkbox.setChecked(self.window().gui_settings.value("debug", False))
        self.window().family_filter_checkbox.setChecked(settings['general']['family_filter'])
        self.window().download_location_input.setText(settings['downloadconfig']['saveas'])
        self.window().always_ask_location_checkbox.setChecked(settings['Tribler']['showsaveas'])
        self.window().download_settings_anon_checkbox.setChecked(settings['Tribler']['default_anonymity_enabled'])
        self.window().download_settings_anon_seeding_checkbox.setChecked(settings['Tribler']['default_safeseeding_enabled'])
        self.window().watchfolder_enabled_checkbox.setChecked(settings['watch_folder']['enabled'])
        self.window().watchfolder_location_input.setText(settings['watch_folder']['watch_folder_dir'])

        # Connection settings
        self.window().firewall_current_port_input.setText(str(settings['general']['minport']))
        self.window().lt_proxy_type_combobox.setCurrentIndex(settings['libtorrent']['lt_proxytype'])
        if settings['libtorrent']['lt_proxyserver']:
            self.window().lt_proxy_server_input = settings['libtorrent']['lt_proxyserver'][0]
            self.window().lt_proxy_port_input = settings['libtorrent']['lt_proxyserver'][1]
        if settings['libtorrent']['lt_proxyauth']:
            self.window().lt_proxy_username_input = settings['libtorrent']['lt_proxyauth'][0]
            self.window().lt_proxy_password_input = settings['libtorrent']['lt_proxyauth'][1]
        self.window().lt_utp_checkbox.setChecked(settings['libtorrent']['utp'])

        # Bandwidth settings
        self.window().upload_rate_limit_input.setText(str(settings['Tribler']['maxuploadrate']))
        self.window().download_rate_limit_input.setText(str(settings['Tribler']['maxdownloadrate']))

        # Seeding settings
        getattr(self.window(), "seeding_" + settings['downloadconfig']['seeding_mode'] + "_radio").setChecked(True)
        self.window().seeding_time_input.setText(seconds_to_string(settings['downloadconfig']['seeding_time']))
        ind = self.window().seeding_ratio_combobox.findText(str(settings['downloadconfig']['seeding_ratio']))
        if ind != -1:
            self.window().seeding_ratio_combobox.setCurrentIndex(ind)

        # Anonymity settings
        self.window().allow_exit_node_checkbox.setChecked(settings['tunnel_community']['exitnode_enabled'])
        self.window().number_hops_slider.setValue(int(settings['Tribler']['default_number_hops']) - 1)
        self.window().multichain_enabled_checkbox.setChecked(settings['multichain']['enabled'])

    def load_settings(self):
        self.settings_request_mgr = TriblerRequestManager()
        self.settings_request_mgr.perform_request("settings", self.initialize_with_settings)

    def clicked_tab_button(self, tab_button_name):
        if tab_button_name == "settings_general_button":
            self.window().settings_stacked_widget.setCurrentIndex(PAGE_SETTINGS_GENERAL)
        elif tab_button_name == "settings_connection_button":
            self.window().settings_stacked_widget.setCurrentIndex(PAGE_SETTINGS_CONNECTION)
        elif tab_button_name == "settings_bandwidth_button":
            self.window().settings_stacked_widget.setCurrentIndex(PAGE_SETTINGS_BANDWIDTH)
        elif tab_button_name == "settings_seeding_button":
            self.window().settings_stacked_widget.setCurrentIndex(PAGE_SETTINGS_SEEDING)
        elif tab_button_name == "settings_anonymity_button":
            self.window().settings_stacked_widget.setCurrentIndex(PAGE_SETTINGS_ANONYMITY)

    def save_settings(self):
        # Create a dictionary with all available settings
        settings_data = {'general': {}, 'Tribler': {}, 'downloadconfig': {}, 'libtorrent': {}, 'watch_folder': {},
                         'tunnel_community': {}, 'multichain': {}}
        settings_data['general']['family_filter'] = self.window().family_filter_checkbox.isChecked()
        settings_data['downloadconfig']['saveas'] = self.window().download_location_input.text()
        settings_data['Tribler']['showsaveas'] = self.window().always_ask_location_checkbox.isChecked()
        if settings_data['Tribler']['showsaveas']:
            settings_data['Tribler']['default_anonymity_enabled'] = self.window().download_settings_anon_checkbox.isChecked()
            settings_data['Tribler']['default_safeseeding_enabled'] = self.window().download_settings_anon_seeding_checkbox.isChecked()
        settings_data['watch_folder']['enabled'] = self.window().watchfolder_enabled_checkbox.isChecked()
        if settings_data['watch_folder']['enabled']:
            settings_data['watch_folder']['watch_folder_dir'] = self.window().watchfolder_location_input.text()

        settings_data['general']['minport'] = self.window().firewall_current_port_input.text()
        settings_data['libtorrent']['lt_proxytype'] = self.window().lt_proxy_type_combobox.currentIndex()
        settings_data['libtorrent']['lt_proxyserver'] = [None, None]
        settings_data['libtorrent']['lt_proxyserver'][0] = self.window().lt_proxy_server_input.text()
        settings_data['libtorrent']['lt_proxyserver'][1] = self.window().lt_proxy_port_input.text()
        settings_data['libtorrent']['lt_proxyauth'] = [None, None]
        settings_data['libtorrent']['lt_proxyauth'][0] = self.window().lt_proxy_username_input.text()
        settings_data['libtorrent']['lt_proxyauth'][1] = self.window().lt_proxy_password_input.text()
        settings_data['libtorrent']['utp'] = self.window().lt_utp_checkbox.isChecked()

        if self.window().upload_rate_limit_input.text():
            settings_data['Tribler']['maxuploadrate'] = self.window().upload_rate_limit_input.text()
        if self.window().download_rate_limit_input.text():
            settings_data['Tribler']['maxdownloadrate'] = self.window().download_rate_limit_input.text()

        settings_data['tunnel_community']['exitnode_enabled'] = self.window().allow_exit_node_checkbox.isChecked()
        settings_data['Tribler']['default_number_hops'] = self.window().number_hops_slider.value() + 1
        settings_data['multichain']['enabled'] = self.window().multichain_enabled_checkbox.isChecked()

        self.settings_request_mgr = TriblerRequestManager()
        self.settings_request_mgr.perform_request("settings", self.on_settings_saved,
                                                  method='POST', data=json.dumps(settings_data))

    def on_settings_saved(self, _):
        self.saved_dialog = ConfirmationDialog(TriblerRequestManager.window, "Settings saved",
                                               "Your settings have been saved.", [('close', BUTTON_TYPE_NORMAL)])
        self.saved_dialog.button_clicked.connect(self.on_dialog_cancel_clicked)
        self.saved_dialog.show()
        self.window().fetch_settings()

    def on_dialog_cancel_clicked(self, _):
        self.saved_dialog.setParent(None)
        self.saved_dialog = None