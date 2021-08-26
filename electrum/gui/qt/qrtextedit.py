from electrum.i18n import _
from electrum.plugin import run_hook
from electrum.simple_config import SimpleConfig

from .util import ButtonsTextEdit, MessageBoxMixin, ColorScheme, getOpenFileName


class ShowQRTextEdit(ButtonsTextEdit):

    def __init__(self, text=None, *, config: SimpleConfig):
        ButtonsTextEdit.__init__(self, text)
        self.config = config
        self.setReadOnly(True)
        icon = "qrcode_white.png" if ColorScheme.dark_scheme else "qrcode.png"
        self.addButton(icon, self.qr_show, _("Show as QR code"))

        run_hook('show_text_edit', self)

    def qr_show(self):
        from .qrcodewidget import QRDialog
        try:
            s = str(self.toPlainText())
        except:
            s = self.toPlainText()
        QRDialog(
            data=s,
            parent=self,
            config=self.config,
        ).exec_()

    def contextMenuEvent(self, e):
        m = self.createStandardContextMenu()
        m.addAction(_("Show as QR code"), self.qr_show)
        m.exec_(e.globalPos())


class ScanQRTextEdit(ButtonsTextEdit, MessageBoxMixin):

    def __init__(self, text="", allow_multi=False, *, config: SimpleConfig, file_filter: str=""):
        ButtonsTextEdit.__init__(self, text)
        self.allow_multi = allow_multi
        self.config = config
        self.setReadOnly(False)
        self.addButton("file.png", self.file_input, _("Read file"))
        icon = "camera_white.png" if ColorScheme.dark_scheme else "camera_dark.png"
        self.addButton(icon, self.qr_input, _("Read QR code"))
        run_hook('scan_text_edit', self)
        self.file_filter = file_filter

    def file_input(self):
        fileName = getOpenFileName(
            parent=self,
            title='select file',
            config=self.config,
            filter=self.file_filter
        )
        if not fileName:
            return
        try:
            try:
                with open(fileName, "r") as f:
                    data = f.read()
            except UnicodeError as e:
                with open(fileName, "rb") as f:
                    data = f.read()
                data = data.hex()
        except BaseException as e:
            self.show_error(_('Error opening file') + ':\n' + repr(e))
        else:
            self.setText(data)

    # Due to the asynchronous nature of the qr reader we need to keep the
    # dialog instance as member variable to prevent reentrancy/multiple ones
    # from being presented at once.
    qr_dialog = None

    def qr_input(self, *, callback=None) -> None:
        if self.qr_dialog:
            self.logger.warning("QR dialog is already presented, ignoring.")
            return
        from . import ElectrumGui
        if ElectrumGui.warn_if_cant_import_qrreader(self):
            return
        from .qrreader import QrReaderCameraDialog, CameraError, MissingQrDetectionLib
        try:
            self.qr_dialog = QrReaderCameraDialog(parent=self.top_level_window(), config=self.config)

            def _on_qr_reader_finished(success: bool, error: str, data):
                if self.qr_dialog:
                    self.qr_dialog.deleteLater()
                    self.qr_dialog = None
                if not success:
                    if error:
                        self.show_error(error)
                    return
                if not data:
                    data = ''
                if self.allow_multi:
                    new_text = self.text() + data + '\n'
                else:
                    new_text = data
                self.setText(new_text)
                if callback and success:
                    callback(data)

            self.qr_dialog.qr_finished.connect(_on_qr_reader_finished)
            self.qr_dialog.start_scan(self.config.get_video_device())
        except (MissingQrDetectionLib, CameraError) as e:
            self.qr_dialog = None
            self.show_error(str(e))
        except Exception as e:
            self.logger.exception('camera error')
            self.qr_dialog = None
            self.show_error(repr(e))

    def contextMenuEvent(self, e):
        m = self.createStandardContextMenu()
        m.addAction(_("Read QR code"), self.qr_input)
        m.exec_(e.globalPos())
