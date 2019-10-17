from PyQt5.QtWidgets import *
from PIL import Image
import numpy as np
from pathlib import Path
from PyQt5.QtCore import *
from PyQt5 import QtGui

from Model.Instruments.Camera.Chameleon import Chameleon
import Utilities.Helper.settings as settings


class CameraOption(QWidget):
    img_sub = pyqtSignal(object)
    img_sub2 = pyqtSignal(object)

    def __init__(self, parent=None):
        super(CameraOption, self).__init__(parent=parent)
        self.parent = parent

        self.GroupBox1 = QGroupBox("Camera")
        layouth = QHBoxLayout()
        layoutT = QGridLayout()#camera setting

        self.AbsTriger = QCheckBox("AbsTriger", self)
        self.video_mode = QCheckBox("video mode", self)
        self.hardware_mode = QCheckBox("hardware mode", self)
        self.cb = QComboBox()#camera select
        self.further_setting = QPushButton("further setting")
        self.auto_save = QCheckBox("auto save", self)
        self.lab = QLabel('',self)
        layoutT.addWidget(self.AbsTriger,1,0,1,1)
        layoutT.addWidget(self.video_mode,1,1,1,1)
        layoutT.addWidget(self.hardware_mode,1,2,1,1)
        layoutT.addWidget(self.cb,0,0,1,2)
        layoutT.addWidget(self.further_setting,0,2,1,1)
        layoutT.addWidget(self.auto_save,2,0,1,1)
        layoutT.addWidget(self.lab,2,1,1,2)
        self.GroupBox1.setLayout(layoutT)
        layouth.addWidget(self.GroupBox1)
        # self.setLayout(layouth)


        self.further_setting.clicked.connect(self.camera_setting)
        # after click the start experiment button, then can change camera setting in detail
        self.further_setting.setEnabled(False)

        # background image
        self.GroupBox2 = QGroupBox("Display")
        layoutT2 = QGridLayout()#camera setting

        self.bkgStatus = QCheckBox("subtract background image", self)
        self.bkgLoad = QPushButton("load background image", self)

        # photon filter
        self.pfStatus = QCheckBox('photon filter', self)

        self.pfMin = QDoubleSpinBox(self)
        self.pfMin.setMinimum(0)  # Prevent numerical underflow
        self.pfMin.setMaximum(1000)
        self.pfMin.setSingleStep(1)

        self.tolab = QLabel('to', self)
        self.pfMax = QDoubleSpinBox(self)
        self.pfMax.setMinimum(0)
        self.pfMax.setMaximum(1000)
        self.pfMax.setSingleStep(1)

        self.roi = QCheckBox("roi", self)
        self.rawdata = QCheckBox("raw data", self)
        self.cross_axes = QCheckBox("cross axes", self)

        layoutT2.addWidget(self.bkgStatus,0,4,1,1)
        layoutT2.addWidget(self.bkgLoad,0,5,1,3)
        layoutT2.addWidget(self.pfStatus,1,4,1,1)
        layoutT2.addWidget(self.pfMin,1,5,1,1)
        layoutT2.addWidget(self.tolab,1,6,1,1)
        layoutT2.addWidget(self.pfMax,1,7,1,1)
        layoutT2.addWidget(self.roi,2,4,1,1)
        layoutT2.addWidget(self.rawdata,2,5,1,1)
        layoutT2.addWidget(self.cross_axes,2,7,1,1)


        # print(1)

        self.GroupBox2.setLayout(layoutT2)
        layouth.addWidget(self.GroupBox2)

        # self.xlab = QLabel('this is for tz', self)

        layoutv = QVBoxLayout()
        layoutv.addLayout(layouth)
        # layoutv.setStretchFactor(layouth, 4)
        # layoutv.addWidget(self.xlab)
        # layoutv.setStretchFactor(self.xlab, 1)

        self.setLayout(layoutv)

        self.default_setting()

        self.bkgStatus.stateChanged.connect(lambda: self.ckbstate(self.bkgStatus))
        # self.magStatus.stateChanged.connect(lambda: self.ckbstate(self.magStatus))
        self.pfStatus.stateChanged.connect(lambda: self.ckbstate(self.pfStatus))

        # self.magValue.valueChanged.connect(self.changeMagValue)
        self.pfMin.valueChanged.connect(self.changePfMin)
        self.pfMax.valueChanged.connect(self.changePfMax)

        self.bkgLoad.clicked.connect(self.loadbkgImg)

        screen = QtGui.QDesktopWidget().screenGeometry()#Control window size
        self.setFixedWidth(screen.width()*47/100)

        ########
        self.d = QDialog()  # create a dialog
        dialog_layout = QVBoxLayout()
        self.apply_button = QPushButton("Apply")
        self.camera_further_setting = CameraSettingWidget()  # set three parameters
        dialog_layout.addWidget(self.camera_further_setting)
        dialog_layout.addWidget(self.apply_button)
        self.d.setLayout(dialog_layout)

        camera_infos = Chameleon.getPortInfo()
        if camera_infos is not None:
            self.cb.addItems(camera_infos)  # get camera num
            # if detect cameras, default camera index is 0
            settings.instrument_params["Camera"]["index"] = 0
        else:
            print("No camera detected !!!")
            self.cb.setEnabled(False)
            return
        # setting widget size

    #######################



    def select_camera_index(self):
        settings.instrument_params["Camera"]["index"] = int(self.cb.currentText().split()[-1])

    def camera_setting(self):
        self.d.setWindowTitle(self.cb.currentText())
        self.d.setWindowModality(Qt.ApplicationModal)
        self.d.exec_()

    def loadbkgImg(self):
        path = QFileDialog.getOpenFileName(self, "Open File")  # name path
        strimg_path = str(path)
        img_file = strimg_path[2:len(strimg_path) - 19]
        img_path = Path(img_file)

        pathjud = str(img_path)
        pathjud = pathjud[len(pathjud) - 3:]  # Get the version of the file
        if pathjud == 'ata':
            file = open(img_path)
            linesc = file.readlines()  # Read the file as a behavior unit
            rows = len(linesc)  # get the numbers fo line
            lines = len(linesc[0].strip().split(' '))
            img_data = np.zeros((rows, lines))  # Initialization matrix
            row = 0
            for line2 in linesc:
                line2 = line2.strip().split(' ')
                img_data[row, :] = line2[:]
                row += 1
            file.close()
        else:
            settings.Type_of_file = 'png'
            try:
                img_data = np.array(Image.open(img_path))
            except TypeError:
                return
            except PermissionError:
                return

        img = img_data[::-1]
        # path, _ = QFileDialog.getOpenFileName(self, 'Open Image', 'c:\\', 'Image files(*.jpg *.gif *.png)')
        # img = Image.open(path)
        settings.imgData["BkgImg"] = np.array(img)
        print('The background image has been added.')

    def default_setting(self):
        self.video_mode.setChecked(False)
        self.hardware_mode.setChecked(False)
        self.video_mode.setEnabled(False)
        self.hardware_mode.setEnabled(False)

        self.bkgStatus.setChecked(settings.widget_params["Image Display Setting"]["bkgStatus"])
        self.pfStatus.setChecked(settings.widget_params["Image Display Setting"]["pfStatus"])
        # self.magStatus.setChecked(settings.widget_params["Image Display Setting"]["magStatus"])

        self.pfMax.setValue(settings.widget_params["Image Display Setting"]["pfMax"])
        self.pfMin.setValue(settings.widget_params["Image Display Setting"]["pfMin"])
        # self.magValue.setValue(settings.widget_params["Image Display Setting"]["magValue"])

    def changeMagValue(self):
        settings.widget_params["Image Display Setting"]["magValue"] = self.magValue.value()
        # print("magnification value is ", settings.widget_params["Image Display Setting"]["magValue"])

    def changePfMin(self):
        settings.widget_params["Image Display Setting"]["pfMin"] = self.pfMin.value()
        # self.img_sub2.emit(1)

    def changePfMax(self):
        settings.widget_params["Image Display Setting"]["pfMax"] = self.pfMax.value()
        # self.img_sub2.emit(1)

    def ckbstate(self, b):
        if b.text() == "subtract background image":
            if b.isChecked() == True:
                if settings.imgData["BkgImg"] !=[]:
                    settings.widget_params["Image Display Setting"]["bkgStatus"] = True
                    print('subtract background image ： finish.')
                    self.img_sub.emit(1)
                    # print("background status", settings.widget_params["Image Display Setting"]["bkgStatus"])
                else:
                    print('No background image.')
            else:
                settings.widget_params["Image Display Setting"]["bkgStatus"] = False

        if b.text() == "photon filter":
            if b.isChecked() == True:
                settings.widget_params["Image Display Setting"]["pfStatus"] = True
                self.img_sub2.emit(1)
                # print('photon filter ： finish.')
                # print("photon filter Status status", settings.widget_params["Image Display Setting"]["pfStatus"])
            else:
                settings.widget_params["Image Display Setting"]["pfStatus"] = False



class CameraSettingWidget(QWidget):
    """
        camera setting and control widget for initialization and running,
        including basis camera settings and control.

    """
    def __init__(self, parent=None):
        super(CameraSettingWidget, self).__init__(parent)
        self.parent = parent
        self.GroupBox = QGroupBox("Camera Setting")
        layout = QVBoxLayout()
        exposure = QHBoxLayout()
        self.exposure_time_label = QLabel("Exposure time: ")
        self.exposure_time = QDoubleSpinBox()
        self.exposure_time.setRange(10, 80)
        self.exposure_time.setSingleStep(1)
        exposure.addWidget(self.exposure_time_label)
        exposure.addWidget(self.exposure_time)

        shutter = QHBoxLayout()
        self.shutter_label = QLabel("Shutter time: ")
        self.shutter_time = QDoubleSpinBox()
        self.shutter_time.setRange(10, 80)
        self.shutter_time.setSingleStep(1)
        shutter.addWidget(self.shutter_label)
        shutter.addWidget(self.shutter_time)

        gain = QHBoxLayout()
        self.gain_label = QLabel("Gain: ")
        self.gain_value = QDoubleSpinBox()
        self.gain_value.setRange(1, 10)
        self.gain_value.setSingleStep(1)
        gain.addWidget(self.gain_label)
        gain.addWidget(self.gain_value)

        layout.addLayout(exposure)
        layout.addLayout(shutter)
        layout.addLayout(gain)

        self.GroupBox.setLayout(layout)
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.GroupBox)

        self.setLayout(self.vertical_layout)

        self.default_setting()

        # self.exposure_time.valueChanged.connect(self.change_exposure)
        # self.shutter_time.valueChanged.connect(self.change_shutter)
        # self.gain_value.valueChanged.connect(self.change_gain)

    def default_setting(self):
        self.shutter_time.setValue(settings.instrument_params["Camera"]["shutter time"])
        self.exposure_time.setValue(settings.instrument_params["Camera"]["exposure time"])
        self.gain_value.setValue(settings.instrument_params["Camera"]["gain value"])

    def change_shutter(self):
        settings.instrument_params["Camera"]["shutter time"] = self.shutter_time.value()
        # print("shutter time is ", settings.instrument_params["Camera"]["shutter time"])

    def change_exposure(self):
        settings.instrument_params["Camera"]["exposure time"] = self.exposure_time.value()
        # print("exposure time is ", settings.instrument_params["Camera"]["exposure time"])

    def change_gain(self):
        settings.instrument_params["Camera"]["gain value"] = self.gain_value.value()
        # print("gain value is ", settings.instrument_params["Camera"]["gain value"])

