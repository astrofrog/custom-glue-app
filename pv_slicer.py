import numpy as np

from glue.qt import get_qapp
from glue.external.qt.QtGui import QMainWindow
from glue.core.application_base import Application

from PyQt4.uic import loadUi
from glue.qt.widgets.image_widget import ImageWidget, PVSliceWidget
from glue.qt.qtutil import data_wizard


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
        self.resize(1200, 800)

        self.image = ImageWidget(session=self._session)
        image = np.random.random((12,12))
        x = np.linspace(-5., 5., 12)
        y = np.linspace(-5., 5., 12)

        self.slice = PVSliceWidget(image, x, y, self.image)

        self.image._slice_widget = self.slice

        self.ui.main_layout.addWidget(self.image)
        self.ui.main_layout.addWidget(self.slice)

        self.ui.load_button.clicked.connect(self._load_data)

    def _load_data(self):

        for data in list(self.data_collection):
            self.data_collection.remove(data)

        self.add_datasets(self.data_collection, data_wizard())
        self.image.add_data(self.data_collection[0])

    def start(self):
        """
        Show the GUI and start the application.
        """
        self.show()
        self.raise_()  # bring window to front
        return self.app.exec_()

    exec_ = start

    # TODO: the following are needed to run, but don't do anything useful. Make
    # it so that they are not required.

    def add_widget(self, new_widget, label=None, tab=None,
                   hold_position=False):
        sub = new_widget.mdi_wrap()
        return sub

    def _load_settings(self):
        pass




if __name__ == "__main__":

    ga = PVSlicer()
    ga.start()
