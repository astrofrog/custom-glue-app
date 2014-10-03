from glue.qt import get_qapp
from glue.external.qt.QtCore import Qt
from glue.external.qt.QtGui import QMainWindow
from glue.core.application_base import Application

from PyQt4.uic import loadUi


class PVSlicer(Application, QMainWindow):
    """
    A proof-of-concept position-velocity slicer using glue
    """

    def __init__(self, data_collection=None, session=None):

        QMainWindow.__init__(self)
        Application.__init__(self,
                             data_collection=data_collection,
                             session=session)

        self.app = get_qapp()

        ui = loadUi('slicer.ui', None)
        self.setCentralWidget(ui)
        # self.setWindowState(Qt.WindowMaximized)
        self.resize(1024, 768)

    def _load_settings(self):
        pass

    def start(self):
        """
        Show the GUI and start the application.
        """
        self.show()
        self.raise_()  # bring window to front
        return self.app.exec_()

    exec_ = start


if __name__ == "__main__":

    # dc = DataCollection()
    ga = PVSlicer()
    ga.start()
