import numpy as np

from glue.qt import get_qapp
from glue.external.qt.QtGui import QMainWindow
from glue.core.application_base import Application

from PyQt4.uic import loadUi
from glue.qt.widgets.image_widget import ImageWidget, PVSliceWidget


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

        self.ui = loadUi('slicer.ui', None)
        self.setCentralWidget(self.ui)
        self.resize(1024, 768)

        w1 = ImageWidget(session=self._session)
        image = np.random.random((12,12))
        x = np.linspace(-5., 5., 12)
        y = np.linspace(-5., 5., 12)

        w2 = PVSliceWidget(image, x, y, w1)

        self.ui.main_layout.addWidget(w1)
        self.ui.main_layout.addWidget(w2)

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

    def add_widget(self, new_widget, label=None, tab=None,
                   hold_position=False):
        sub = new_widget.mdi_wrap()
        return sub



if __name__ == "__main__":

    ga = PVSlicer()
    ga.start()
