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


class ImgAnalysisSetting(QWidget):

    abs_img = pyqtSignal(dict)


    def __init__(self, parent=None):
        super(ImgAnalysisSetting, self).__init__(parent=parent)
        self.parent = parent

        self.horizontalGroupBox1 = QGroupBox("Analyse Data Setting")
        self.horizontalGroupBox2 = QGroupBox("Experiment Parameters")
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()

        self.roi = QCheckBox("roi", self)
        self.cross_axes = QCheckBox("cross axes", self)
        # self.cross_axes2 = QCheckBox("cross axes2", self)
        self.auto_save = QCheckBox("auto save", self)
########################################################################################
        # self.absorb_img.clicked.connect(self.absorb_setting)
        self.dia = QDialog()  # create a dialog
        self.dia2 = QDialog()  # create a dialog
        self.prefix_label = QLabel('Prefix',self)
        self.prefix_text = QLineEdit('Data',self)
        self.layoutprefix = QHBoxLayout(self)
        self.layoutprefix.addWidget(self.prefix_label)
        self.layoutprefix.addWidget(self.prefix_text)
        self.dia2.setLayout(self.layoutprefix)

        self.layoutv = QHBoxLayout(self)
        self.layoutv1 = QVBoxLayout(self)
        self.layoutv3 = QHBoxLayout(self)
        # win = pg.GraphicsView()
        l1 = pg.GraphicsLayout(border=(100, 100, 100))
        win1 = pg.GraphicsLayoutWidget()
        win1.setCentralItem(l1)
        pg.setConfigOptions(imageAxisOrder='row-major')
        # pg.setConfigOptions(leftButtonPan=False)
        self.viewBox = l1.addPlot()
        self.img = pg.ImageItem()
        self.viewBox.setMouseEnabled(x=False, y=False)  # make it can not move
        # pg.setConfigOptions(leftButtonPan=False)
        self.viewBox.addItem(self.img)
        self.layoutv1.addWidget(win1)
        self.img_labelt1 = QLabel()
        self.img_Push1 = QPushButton("=>", self)
        self.img_Push2 = QPushButton('save', self)
        self.img_Push1.clicked.connect(self.push_state)
        self.img_Push2.clicked.connect(self.push2_state)
        # self.img_labelt1.setText()
        self.layoutv3.addWidget(self.img_labelt1)
        self.layoutv3.addWidget(self.img_Push2)
        self.layoutv1.addLayout(self.layoutv3)
        # self.img_Push1.setEnabled(False)
        self.img_Push2.setEnabled(False)


        self.layoutv2 = QVBoxLayout(self)

        plot_win1 = PlotWindow()
        plot_win1.myserial = 0
        plot_win2 = PlotWindow()
        plot_win2.myserial = 1
        plot_win3 = PlotWindow()
        plot_win3.myserial = 2
        self.layoutv2.addWidget(plot_win1)
        self.layoutv2.addWidget(plot_win2)
        self.layoutv2.addWidget(plot_win3)
        ##################
        self.layoutv.addLayout(self.layoutv2)
        self.layoutv.addWidget(self.img_Push1)
        self.layoutv.addLayout(self.layoutv1)

        self.abs_img.connect(self.update_image2)

        self.dia.setLayout(self.layoutv)
        screen = QtGui.QDesktopWidget().screenGeometry()  # Control window size
        self.dia.setFixedSize(screen.width() * 56/ 100, screen.height() * 50/ 100)
        win1.setFixedSize(screen.width() * 30 / 100, screen.height() * 45/ 100)
###################################################################################
        ToPwrLabel = QLabel('TotPwr_mW')
        self.ToPwr = QDoubleSpinBox()
        self.ToPwr.setMaximum(999)
        self.ToPwr.setMinimum(0)
        self.ToPwr.setSingleStep(1)
        DetuLabel = QLabel('Detu_MHz')
        self.Detu = QDoubleSpinBox()
        self.Detu.setMaximum(999)
        self.Detu.setMinimum(0)
        self.Detu.setSingleStep(1)
        DiaLabel = QLabel('Dia_mm')
        self.Dia = QDoubleSpinBox()
        self.Dia.setMaximum(999)
        self.Dia.setMinimum(0)
        self.Dia.setSingleStep(1)

        layout1.addWidget(self.roi)
        layout1.addWidget(self.cross_axes)
        # layout1.addWidget(self.cross_axes2)
        layout1.addWidget(self.auto_save)
        # layout1.addWidget(self.piefix)
        # layout1.addWidget(self.absorb_img)

        layout2.addWidget(ToPwrLabel)
        layout2.addWidget(self.ToPwr)
        layout2.addWidget(DetuLabel)
        layout2.addWidget(self.Detu)
        layout2.addWidget(DiaLabel)
        layout2.addWidget(self.Dia)

        self.horizontalGroupBox1.setLayout(layout1)
        self.horizontalGroupBox2.setLayout(layout2)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.horizontalGroupBox1)
        self.vertical_layout.addWidget(self.horizontalGroupBox2)

        self.setLayout(self.vertical_layout)

        self.default_setting()

        self.Detu.valueChanged.connect(self.change_Detu)
        self.Dia.valueChanged.connect(self.change_Dia)
        self.ToPwr.valueChanged.connect(self.change_ToPwr)
        self.setFixedSize(screen.width()*34/100,screen.height()*18/100)

    def update_image2(self,img_dict):
        self.img.setImage(img_dict['img_data'])
        self.img_labelt1.setText(img_dict['img_name'])
        # self.data = img_dict['img_data']
        # self.data_shape = self.data.shape

    def push2_state(self):
        fpath = IOHelper.get_config_setting('DATA_PATH')
        fpath = Path(fpath)
        dir_path = fpath.joinpath(str(datetime.datetime.now())[2:].split('.')[0].replace(' ', '-').replace(':', '_'))
        # print("save images to {}".format(dir_path))
        if settings.m_path != []:
            dir_path = settings.m_path
        if not dir_path.exists():
            dir_path.mkdir()
        img_data = np.array(self.img.image)
        # load image name by path
        img_name = (self.img_labelt1.text())[0:20].replace(' ', '~').replace(':', '_').replace('-', '')
        img_data = img_data[::-1]
        import numpy
        numpy.savetxt(r"{}\{}.ndata".format(dir_path, img_name), img_data, fmt='%.2e', delimiter=' ', newline='\n',
                      header='', footer='', comments=' ', encoding=None)
        print("save images to {}".format(dir_path))


    def push_state(self):
        if settings.absimgDatas[0] != [] and settings.absimgDatas[1] != [] and settings.absimgDatas[2] != []:
            withatom = np.zeros((settings.absimgDatas[0].shape[0], settings.absimgDatas[0].shape[1]))
            withoutatom = np.zeros((settings.absimgDatas[1].shape[0], settings.absimgDatas[1].shape[1]))
            totalmat = np.zeros((settings.absimgDatas[1].shape[0], settings.absimgDatas[1].shape[1]))
            settings.absimgDatas[3] = np.zeros((settings.absimgDatas[1].shape[0], settings.absimgDatas[1].shape[1]))

            # print('In the calculation')
            import warnings
            warnings.filterwarnings("ignore")
            for ii in range(settings.absimgDatas[1].shape[0]):
                for jj in range(settings.absimgDatas[1].shape[1]):
                    withatom[ii, jj] = settings.absimgDatas[0][ii, jj] - settings.absimgDatas[2][ii, jj]  ####
                    withoutatom[ii, jj] = settings.absimgDatas[1][ii, jj] - settings.absimgDatas[2][ii, jj]  ###

                    if withoutatom[ii, jj] != 0:
                        totalmat[ii, jj] = withatom[ii, jj] / withoutatom[ii, jj]  ##########
                    else:
                        totalmat[ii, jj] = 1

                    if totalmat[ii, jj] >= 1 or totalmat[ii, jj] <= 0:
                        totalmat[ii, jj] = 1

                    settings.absimgDatas[3][ii, jj] = -np.log(totalmat[ii, jj])
            # print(settings.absimgData[3][0:20,0:20])

            timestamp = datetime.datetime.now()
            self.abs_img.emit({'img_name': str(timestamp)[2:], 'img_data': settings.absimgDatas[3]})
            self.img_Push2.setEnabled(True)
        else:
            print('Please add images')


    def absorb_setting(self):
        self.dia.setWindowTitle('absorb image')
        self.dia.setWindowModality(Qt.ApplicationModal)
        self.dia.exec_()

    def prefix_setting(self):
        self.dia2.setWindowTitle('prefix setting')
        self.dia2.setWindowModality(Qt.ApplicationModal)
        self.dia2.exec_()

    def default_setting(self):

        self.roi.setChecked(False)
        self.cross_axes.setChecked(False)
        # self.cross_axes2.setChecked(False)

        self.Detu.setValue(settings.widget_params["Analyse Data Setting"]["Detu"])
        self.Dia.setValue(settings.widget_params["Analyse Data Setting"]["Dia"])
        self.ToPwr.setValue(settings.widget_params["Analyse Data Setting"]["ToPwr"])

    def change_Detu(self):
        settings.widget_params["Analyse Data Setting"]["Detu"] = self.Detu.value()
        print("new Detu is ", settings.widget_params["Analyse Data Setting"]["Detu"])

    def change_Dia(self):
        settings.widget_params["Analyse Data Setting"]["Dia"] = self.Dia.value()
        print("new Dia is ", settings.widget_params["Analyse Data Setting"]["Dia"])

    def change_ToPwr(self):
        settings.widget_params["Analyse Data Setting"]["ToPwr"] = self.ToPwr.value()
        print("new toPwr is ", settings.widget_params["Analyse Data Setting"]["ToPwr"])


class PlotWindow(QWidget):

    img_dict = pyqtSignal(object)

    myserial = 5

    def __init__(self):
        super(PlotWindow, self).__init__()
        self.layout = QHBoxLayout(self)

        pg.setConfigOptions(imageAxisOrder='row-major')
        self.viewport = GraphicsLayoutWidget()
        self.video_view = self.viewport.addViewBox()
        self.video = pg.ImageItem()
        self.video_view.addItem(self.video)
        self.video_view.setMouseEnabled(x=False, y=False)#make it can not move

        self.setLayout(self.layout)

        self.layout.addWidget(self.viewport)
        self.img_label = QLabel()

        self.push_btn = QPushButton("load", self)
        self.push_btn.clicked.connect(self.load_state)
        self.save_btn = QPushButton("save", self)
        self.save_btn.clicked.connect(self.save_image)
        self.horizontalLayout = QVBoxLayout()
        self.horizontalLayout.addWidget(self.push_btn)
        self.horizontalLayout.addWidget(self.save_btn)
        self.horizontalLayout.addWidget(self.img_label)
        self.layout.addLayout(self.horizontalLayout)
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setFixedSize(screen.width() * 18 / 100, screen.height() * 14.5 / 100)


    def load_state(self):
        try:
            fpath = IOHelper.get_config_setting('DATA_PATH')

            img_fpath = QFileDialog.getOpenFileName(self, "Open File", fpath)  # name path
            strimg_fpath = str(img_fpath)
            img_file = strimg_fpath[2:len(strimg_fpath) - 19]
            img_path = Path(img_file)

            file = open(img_path)
            linescontent = file.readlines()  # Read the file as a behavior unit
            rows = len(linescontent)  # get the numbers fo line
            lines = len(linescontent[0].strip().split(' '))
            img_data = np.zeros((rows, lines))  # Initialization matrix
            row = 0
            for line in linescontent:
                line = line.strip().split(' ')
                img_data[row, :] = line[:]
                row += 1
            file.close()

            img_data = img_data[::-1]
            img_name = img_path.stem
            img = {
                'img_name': img_name,
                'img_data': img_data}
            settings.absimgDatas[self.myserial] = img_data

            self.img_plot(img)
        except TypeError:
            return
        except PermissionError:
            return

    def update_console(self, stri):
        MAX_LINES = 50
        stri = str(stri)
        new_text = self.prompt_dock.console_text() + '\n' + stri
        line_list = new_text.splitlines()
        N_lines = min(MAX_LINES, len(line_list))
        # limit output lines
        new_text = '\n'.join(line_list[-N_lines:])
        self.prompt_dock.console_text(new_text)
        self.prompt_dock.automatic_scroll()

    def save_image(self):
        try:
            if self.video.image is None:
                print("have no image in window")
                return
            fpath = IOHelper.get_config_setting('DATA_PATH')
            fpath = Path(fpath)
            dir_path = fpath.joinpath(str(datetime.datetime.now()).split('.')[0].replace(' ', '-').replace(':', '_'))
            # print("save images to {}".format(dir_path))
            if not dir_path.exists():
                dir_path.mkdir()
                img_data = np.array(self.video.image)
                # load image name by path
                img_name1 = settings.widget_params["Analyse Data Setting"]["Prefix"]
                img_name2 = (self.img_label.text())[0:20].replace(' ', '~').replace(':', '').replace('-', '')
                img_name = str(img_name1) + str(img_name2)
                img_data = img_data[::-1]
                img_data = Image.fromarray(img_data)
                img_data.save(r"{}\{}.png".format(dir_path, img_name))
            print("save images to {}".format(dir_path))
            # print("images have saved.")
        except OSError:
            print('Only new version files can be saved.')

    def img_plot(self, img_dict):
        self.video.setImage(img_dict['img_data'])
        self.img_label.setText(img_dict['img_name'])

    def clear_win(self):
        self.video.clear()
        self.img_label.setText('')
