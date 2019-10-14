import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget
from Utilities.IO import IOHelper
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utilities.Helper import settings
from pathlib import Path
import numpy as np
from PIL import Image
import datetime
from queue import Queue
from PyQt5 import QtGui
from Widget.CoreWidget import AnalyseDataWidget


class ImgQueueWidget(QWidget):

    def __init__(self, parent=None):
        super(ImgQueueWidget, self).__init__(parent)
        # plot image history
        self.verticalLayout = QVBoxLayout()
        self.plot_wins = Queue(settings.widget_params['Image Display Setting']['img_stack_num'])
        for i in range(settings.widget_params['Image Display Setting']['img_stack_num']):
            plot_win = PlotWindow()
            plot_win.video.image = None
            self.plot_wins.put(plot_win)
            self.verticalLayout.addWidget(plot_win)
        self.setLayout(self.verticalLayout)
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setFixedSize(screen.width()*16/100,screen.width()*(9/16)*(60/100))
        # print(self.width(), self.height())


class PlotWindow(QWidget):

    img_dict = pyqtSignal(object)

    def __init__(self):
        super(PlotWindow, self).__init__()
        self.layout = QHBoxLayout(self)

        pg.setConfigOptions(imageAxisOrder='row-major')
        self.viewport = GraphicsLayoutWidget()
        self.video_view = self.viewport.addViewBox()
        self.video = pg.ImageItem()
        # self.video_view.clicked.connect(self.btn_state)
        self.video_view.addItem(self.video)
        self.video_view.setMouseEnabled(x=False, y=False)#make it can not move

        self.setLayout(self.layout)

        self.layout.addWidget(self.viewport)
        self.img_label = QLabel()

        # self.push_btn = QPushButton("sent", self)
        # self.push_btn.clicked.connect(self.btn_state)
        # self.save_btn = QPushButton("save", self)
        # self.save_btn.clicked.connect(self.save_image)
        # self.horizontalLayout = QVBoxLayout()
        # self.horizontalLayout.addWidget(self.push_btn)
        # self.horizontalLayout.addWidget(self.save_btn)
        # self.horizontalLayout.addWidget(self.img_label)
        # self.layout.addLayout(self.horizontalLayout)

        screen = QtGui.QDesktopWidget().screenGeometry()
        # print(screen)
        self.setFixedSize(screen.width() * 15 / 100, screen.width() * (9/16)*(14 / 100))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.btn_state()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.save_image()

    def btn_state(self):
        if self.video.image is None:
            print("have no image in window")
            # from MainWindow import TestMainWindow
            # TestMainWindow.path.setTitle(str('have no image in window'))
            return
        # img_analyse_setting.roi.setChecked(False)
        img_dict = {'img_data': np.array(self.video.image), 'img_name': self.img_label.text()}
        settings.imgData["Img_data"] = img_dict['img_data']
        self.img_dict.emit(img_dict)
######################################
    # def save_image(self):
    #     # try:
    #     if self.video.image is None:
    #         print("have no image in window")
    #         return
    #     fpath = IOHelper.get_config_setting('DATA_PATH')
    #     fpath = Path(fpath)
    #     dir_path = fpath.joinpath(str(datetime.datetime.now()).split('.')[0].replace(' ', '-').replace(':', '_'))
    #     if settings.m_path != []:
    #         dir_path = settings.m_path
    #     # print("save images to {}".format(dir_path))
    #     if not dir_path.exists():
    #         dir_path.mkdir()
    #     img_data = np.array(self.video.image)
    #     # load image name by path
    #     img_name = (self.img_label.text()).split('.')[0].replace(' ', '-').replace(':', '_')
    #     img_data = img_data[::-1]
    #     img_data = Image.fromarray(img_data)
    #     img_data.save(r"{}\{}.png".format(dir_path, img_name))
    #     print("save images to {}".format(dir_path))
    #         # print("images have saved.")
    #     # except OSError:
    #     #     print('Image cannot be saved.')
########################################################################33
    def save_image(self):
        # try:
        if self.video.image is None:
            print("have no image in window")
            return
        fpath = IOHelper.get_config_setting('DATA_PATH')
        fpath = Path(fpath)
        dir_path = fpath.joinpath(str(datetime.datetime.now())[2:].split('.')[0].replace(' ', '').replace(':', '_'))
        if settings.m_path != []:
            dir_path = settings.m_path
        # print("save images to {}".format(dir_path))
        if not dir_path.exists():
            dir_path.mkdir()
        img_data = np.array(self.video.image)
        # load image name by path
        img_name1 = settings.widget_params["Analyse Data Setting"]["Prefix"]
        img_name2 = (self.img_label.text())[0:20].replace(' ', '~').replace(':', '').replace('-', '')
        img_name = str(img_name1) + str(img_name2)
        img_data = img_data[::-1]
        # img_data = Image.fromarray(img_data)
        # img_data.save(r"{}\{}.png".format(dir_path, img_name))
        import  numpy
        numpy.savetxt(r"{}\{}.data".format(dir_path, img_name), img_data, fmt='%.2e', delimiter=' ', newline='\n', header='', footer='', comments=' ',
                      encoding=None)
        print("save images to {}".format(dir_path))
            # print("images have saved.")
        # except OSError:
        #     print('Image cannot be saved.')

#############################################################3
    def img_plot(self, img_dict):
        # print(img_dict['img_data'].ndim)
        self.video.setImage(img_dict['img_data'])
        self.img_label.setText(img_dict['img_name'])

    def clear_win(self):
        self.video.clear()
        self.img_label.setText('')


