
from qgis.PyQt.QtWidgets import QAction, QMessageBox
from .gui.geocheck_dialog import GeoCheckDialog


class GeoCheckPlugin:

    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dialog = None

    def initGui(self):
        self.action = QAction(
            "GeoCheck",
            self.iface.mainWindow()
        )

        self.action.triggered.connect(self.run)

        self.iface.addPluginToMenu(
            "&GeoCheck",
            self.action
        )

        self.iface.addToolBarIcon(self.action)

    def run(self):
        if self.dialog is None:
            self.dialog = GeoCheckDialog(self.iface.mainWindow())

        self.dialog.load_layers()
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()

    def unload(self):
        if self.action:
            self.iface.removePluginMenu(
                "&GeoCheck",
                self.action
            )
            self.iface.removeToolBarIcon(self.action)

        if self.dialog:
            self.dialog.close()
            self.dialog = None
