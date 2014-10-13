import numpy as np

from glue.qt import get_qapp
from glue.external.qt.QtGui import QMainWindow, QWidget, QStackedWidget, QFileDialog
from glue.core.application_base import Application

from PyQt4.uic import loadUi
from glue.qt.widgets.image_widget import ImageWidget as GlueImageWidget
from glue.plugins.pv_slicer import PVSliceWidget, PVSlicerTool as GluePVSlicerTool
from glue.qt.qtutil import data_wizard

from astropy.io import fits


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

        self.ui = loadUi('slicer5.ui', None)
        self.setCentralWidget(self.ui)
        self.resize(1200, 800)

        box1 = QStackedWidget()
        box2 = QStackedWidget()

        class PVSlicerTool(GluePVSlicerTool):

            def _extract_pv_slice(self, mode):
                super(PVSlicerTool, self)._extract_pv_slice(mode)
                box2.setCurrentIndex(1)

        class ImageWidget(GlueImageWidget):

            def _setup_tools(self):
                self._tools = [PVSlicerTool(self)]

        self.box1 = box1
        self.box2 = box2

        self.image = ImageWidget(session=self._session)

        self.slice = PVSliceWidget(image_widget=self.image)

        for tool in self.image._tools:
            if isinstance(tool, PVSlicerTool):
                tool._slice_widget = self.slice

        self.dummy1 = QWidget()
        self.dummy2 = QWidget()

        self.box1.addWidget(self.dummy1)
        self.box1.addWidget(self.image)

        self.box2.addWidget(self.dummy2)
        self.box2.addWidget(self.slice)

        self.ui.data_layout.addWidget(self.box1, stretch=1)
        self.ui.data_layout.addWidget(self.box2, stretch=1)

        self.ui.load_button.clicked.connect(self._load_data)
        self.ui.save_button.clicked.connect(self._save_data)

    def _save_data(self):

        fname, fltr = QFileDialog.getSaveFileName(caption="Select an output filename",
                                                  filter='FITS mask (*.fits);; Fits mask (*.fits)')
        fname = str(fname)
        if not fname:
            return

        # TODO: need glue to save WCS
        pv_slice = self.slice._im_array

        fits.writeto(fname, pv_slice, clobber=True)


    def _load_data(self):

        for data in list(self.data_collection):
            self.data_collection.remove(data)

        data = data_wizard()

        if not data:
            return

        self.add_datasets(self.data_collection, data)
        self.image.add_data(self.data_collection[0])

        self.box1.setCurrentIndex(1)

        self.ui.top_bar.insertWidget(1,self.image.ui.slice._slices[0]._ui_slider)

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
