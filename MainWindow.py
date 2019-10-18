from Model.Instruments.Camera.Chameleon import Chameleon
from Utilities.Helper import settings, Helper
from Utilities.IO import IOHelper
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from Widget.CoreWidget.PlotMainWindowWidget import PlotMainWindow
from Widget.CoreWidget.ImgQueueWidget import ImgQueueWidget
from Widget.CoreWidget.ImgDisplaySetting import ImgDisplaySetting
from Widget.CoreWidget.AnalyseDataWidget import ImgAnalysisSetting
from Widget.CoreWidget.PromptWidget import PromptWidget
from Widget.CoreWidget.ResultWidget import ResultWidget
from Widget.CoreWidget.FittingdataWidget import FittingdataWidget
from Widget.CustomWidget.CameraSettingWidget import CameraOption

import numpy as np
import sys
from PIL import Image
import time
from pathlib import Path
import datetime


class TestMainWindow(QMainWindow):

    sig_abort_workers = pyqtSignal()

    def __init__(self):
        super(TestMainWindow, self).__init__()
        self.move(82, 0)
        ### MENUS AND TOOLBARS ###
        self.fileMenu = self.menuBar().addMenu("File")
        self.windowMenu = self.menuBar().addMenu("Window")
        self.optionMenu = self.menuBar().addMenu("Options")
        self.path = self.menuBar().addMenu("")
        self.path.setEnabled(False)

        self.plotToolbar = self.addToolBar("Plot")
        self.expToolbar = self.addToolBar("Experiment")
        self.testToolbar = self.addToolBar("test")

        # experiment start/stop buttons
        self.start_exp_action = Helper.create_action(self, "Start Experiment", slot=self.start_exp, icon="start")#name and action and image
        self.stop_exp_action = Helper.create_action(self, "Stop Experiment", slot=self.stop_exp, icon="stop")
        self.stop_exp_action.setEnabled(False)

        # plot buttons
        self.clear_img_stack_action = Helper.create_action(self, "clear image stack", slot=self.clear_img_stack, icon="clear_img_stack")
        self.clear_main_win_action = Helper.create_action(self, "clear main window", slot=self.clear_main_win, icon="clear_main_win")

        ### CREATE WIDGET ###
        # global parameters
        settings.inintParams()

        self.plot_main_window = PlotMainWindow()
        self.setCentralWidget(self.plot_main_window)# set central

        # image queue dock
        self.img_queue = ImgQueueWidget()
        # create a QDockWidget
        imgQueueDockWidget = QDockWidget("Image Stack", self)
        imgQueueDockWidget.setObjectName("imgStackDockWidget")
        imgQueueDockWidget.setAllowedAreas(
            Qt.LeftDockWidgetArea)
        imgQueueDockWidget.setWidget(self.img_queue)
        self.addDockWidget(Qt.LeftDockWidgetArea, imgQueueDockWidget)
        self.windowMenu.addAction(imgQueueDockWidget.toggleViewAction())


        # # image display setting dock
        # self.img_display_setting = ImgDisplaySetting()
        # self.img_display_setting.img_sub.connect(self.plot_main_window.img_plot2)
        # self.img_display_setting.img_sub2.connect(self.plot_main_window.img_plot3)
        #
        # # create a QDockWidget
        # displaySettingDockWidget = QDockWidget("Display Setting", self)
        # displaySettingDockWidget.setObjectName("displaySettingDockWidget")
        # displaySettingDockWidget.setAllowedAreas(Qt.RightDockWidgetArea)
        # displaySettingDockWidget.setWidget(self.img_display_setting)
        # self.addDockWidget(Qt.RightDockWidgetArea, displaySettingDockWidget)
        # # enable the toggle view action
        # self.windowMenu.addAction(displaySettingDockWidget.toggleViewAction())

        # image analyse setting dock
        self.img_analyse_setting = ImgAnalysisSetting()
        analyseDataDockWidget = QDockWidget("Analyse Data", self)
        analyseDataDockWidget.setObjectName("analyseDataDockWidget")
        analyseDataDockWidget.setAllowedAreas(Qt.RightDockWidgetArea)
        analyseDataDockWidget.setWidget(self.img_analyse_setting)
        self.addDockWidget(Qt.RightDockWidgetArea, analyseDataDockWidget)
        self.windowMenu.addAction(analyseDataDockWidget.toggleViewAction())

        self.img_analyse_setting.prefix_text.editingFinished.connect(self.editFinished)

        # camera setting dock
        self.camera_setting = CameraOption()
        cameraSettingDockWidget = QDockWidget("Setting", self)
        cameraSettingDockWidget.setObjectName("cameraSettingDockWidget")
        cameraSettingDockWidget.setAllowedAreas(Qt.BottomDockWidgetArea)
        cameraSettingDockWidget.setWidget(self.camera_setting)
        self.addDockWidget(Qt.BottomDockWidgetArea, cameraSettingDockWidget)
        self.windowMenu.addAction(cameraSettingDockWidget.toggleViewAction())

        self.camera_setting.img_sub.connect(self.plot_main_window.img_plot2)
        self.camera_setting.img_sub2.connect(self.plot_main_window.img_plot3)

        # output dock
        # self.prompt_dock = PromptWidget()
        # promptDockWidget = QDockWidget("Output Console", self)
        # promptDockWidget.setObjectName("consoleDockWidget")
        # # promptDockWidget.setAllowedAreas(Qt.RightDockWidgetArea)
        # promptDockWidget.setWidget(self.prompt_dock)
        # self.addDockWidget(Qt.RightDockWidgetArea, promptDockWidget)
        # # redirect print statements to show a copy on "console"
        sys.stdout = Helper.print_redirect()
        sys.stdout.print_signal.connect(self.update_console)
        # # sys.stdout.print_signal.connect(self.update_pro)
        # self.windowMenu.addAction(promptDockWidget.toggleViewAction())

        # Fitting dock
        self.Fitting_dock = FittingdataWidget()
        fittingDockWidget = QDockWidget("Fitting Console", self)
        fittingDockWidget.setObjectName("FittingDockWidget")
        fittingDockWidget.setAllowedAreas(Qt.BottomDockWidgetArea)
        fittingDockWidget.setWidget(self.Fitting_dock)
        self.addDockWidget(Qt.BottomDockWidgetArea, fittingDockWidget)
        self.windowMenu.addAction(fittingDockWidget.toggleViewAction())

        # result dock
        self.result_dock = ResultWidget()
        resultDockWidget = QDockWidget("Result Console", self)
        resultDockWidget.setObjectName("resultDockWidget")
        resultDockWidget.setAllowedAreas(Qt.RightDockWidgetArea)
        resultDockWidget.setWidget(self.result_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, resultDockWidget)
        self.windowMenu.addAction(resultDockWidget.toggleViewAction())

        ### TOOLBAR MENU ###
        self.expToolbar.setObjectName("ExperimentToolbar")

        self.expToolbar.addAction(self.start_exp_action)
        self.expToolbar.addAction(self.stop_exp_action)

        self.plotToolbar.setObjectName("PlotToolbar")

        self.plotToolbar.addAction(self.clear_img_stack_action)
        self.plotToolbar.addAction(self.clear_main_win_action)

        self.LoadfolderAction = Helper.create_action(self,
                                                           "Load folder",
                                                           slot=self.load_img2stack,
                                                           shortcut=None,
                                                           icon=None,
                                                           tip="Load previous images to image stack from file")

        self.LoadImgAction = Helper.create_action(self,
                                                      "Load Images",
                                                      slot=self.file_load_imgs,
                                                      shortcut=None,
                                                      icon=None,
                                                      tip="Load previous images to image stack")

        self.SaveImgAction = Helper.create_action(self,
                                                       "Save all stack images",
                                                       slot=self.file_save_imgs,
                                                       shortcut=None,
                                                       icon=None,
                                                       tip="Save image stack's images")

        self.SaveMainImgAction = Helper.create_action(self,
                                                  "Save MainWindow's images",
                                                  slot=self.Mainwindowfile_save_imgs,
                                                  shortcut=None,
                                                  icon=None,
                                                  tip="Save MainWidnow's images")

        self.SetpathAction = Helper.create_action(self,
                                                      "Set the default save path",
                                                      slot=self.Setpath,
                                                      shortcut=None,
                                                      icon=None,
                                                      tip="Set the default save path")

        self.AbsorbImageAction = Helper.create_action(self,
                                                  "Absorb Image",
                                                  slot=self.img_analyse_setting.absorb_setting,
                                                  shortcut=None,
                                                  icon=None,
                                                  tip="Processing absorption imaging")

        self.PrefixsettingAction = Helper.create_action(self,
                                                      "Prefix setting",
                                                      slot=self.img_analyse_setting.prefix_setting,
                                                      shortcut=None,
                                                      icon=None,
                                                      tip="Prefix setting")

        self.fileMenu.addAction(self.LoadImgAction)
        self.fileMenu.addAction(self.LoadfolderAction)
        self.fileMenu.addAction(self.SaveMainImgAction)
        self.fileMenu.addAction(self.SaveImgAction)
        self.optionMenu.addAction(self.SetpathAction)
        self.optionMenu.addAction(self.AbsorbImageAction)
        self.optionMenu.addAction(self.PrefixsettingAction)


        # queue for update main window when camera is in video mode
        self.acquiring = False
        # thread for acquiring image from camera to queue
        self.thread = None
        self.worker = None
        self.connect_slot2signal()
        self.setWindowIcon(QIcon('images/icon/UALab.png'))
        self.show()

    def editFinished(self):
        settings.widget_params["Analyse Data Setting"]["Prefix"] = str(self.img_analyse_setting.prefix_text.text())
        # print(settings.widget_params["Analyse Data Setting"]["Prefix"])
        # print(type(settings.widget_params["Analyse Data Setting"]["Prefix"]))

    def change_camera_params(self):
        self.camera_setting.apply_button.setEnabled(False)
        if self.acquiring:
            self.sig_abort_workers.emit()
            self.thread.quit()  # this will quit **as soon as thread event loop unblocks**
            self.thread.wait()  # <- so you need to wait for it to *actually* quit
            print("camera thread quit")
            self.worker = Worker()
            self.thread = QThread()
            self.worker.moveToThread(self.thread)
            self.worker.sig_video_mode_img.connect(self.update_main_plot_win)
            self.worker.sig_hardware_mode_img.connect(self.update_image_queue)
            # control worker:
            self.sig_abort_workers.connect(self.worker.abort)
            self.thread.started.connect(self.worker.work)
            self.thread.start()  # this will emit 'started' and start thread's event loop
            print("camera setting is applied ")
        self.camera_setting.apply_button.setEnabled(True)

    def change_camera_mode(self, mode):
        if self.acquiring:
            if mode.isChecked():
                self.sig_abort_workers.emit()
                self.thread.quit()  # this will quit **as soon as thread event loop unblocks**
                self.thread.wait()  # <- so you need to wait for it to *actually* quit
                # print("camera thread quit")
                if mode.text() == 'video mode':
                    settings.widget_params["Image Display Setting"]["mode"] = 0
                    self.camera_setting.hardware_mode.setEnabled(True)
                    self.camera_setting.video_mode.setEnabled(False)
                    self.camera_setting.hardware_mode.setChecked(False)
                    self.camera_setting.apply_button.setEnabled(True)
                    self.camera_setting.camera_further_setting.gain_value.setEnabled(True)
                    self.camera_setting.camera_further_setting.exposure_time.setEnabled(True)
                    self.camera_setting.camera_further_setting.shutter_time.setEnabled(True)
                    print('video mode')

                elif mode.text() == 'hardware mode':
                    settings.widget_params["Image Display Setting"]["mode"] = 2
                    self.camera_setting.hardware_mode.setEnabled(False)
                    self.camera_setting.video_mode.setChecked(False)
                    self.camera_setting.video_mode.setEnabled(True)
                    self.camera_setting.apply_button.setEnabled(False)
                    self.camera_setting.camera_further_setting.gain_value.setEnabled(False)
                    self.camera_setting.camera_further_setting.exposure_time.setEnabled(False)
                    self.camera_setting.camera_further_setting.shutter_time.setEnabled(False)
                    # self.img_display_setting.video_mode.setChecked(True)
                    print('hardware mode')

                self.worker = Worker()
                self.thread = QThread()
                self.worker.moveToThread(self.thread)
                self.worker.sig_video_mode_img.connect(self.update_main_plot_win)
                self.worker.sig_hardware_mode_img.connect(self.update_image_queue)
                # control worker:
                self.sig_abort_workers.connect(self.worker.abort)
                self.thread.started.connect(self.worker.work)
                self.thread.start()  # this will emit 'started' and start thread's event loop
            # print("camera is in new mode")

    def start_exp(self):
        """
        start basis experiment include capturing images, more operations can be
        added here or use a script file to control instrument accurately.
        :return:
        """
        if settings.instrument_params["Camera"]["index"] is not None:

            self.start_exp_action.setEnabled(False)#CANNOT START

            self.LoadfolderAction.setEnabled(False)#CANNOT LOAD AND SAVE
            self.SaveImgAction.setEnabled(False)
            self.SaveMainImgAction.setEnabled(False)
            self.LoadImgAction.setEnabled(False)
            self.camera_setting.AbsTriger.setEnabled(False)

            self.camera_setting.video_mode.setEnabled(True)
            self.camera_setting.hardware_mode.setEnabled(True)

            self.clear_img_stack_action.setEnabled(False)
            self.clear_main_win_action.setEnabled(False)

            self.worker = Worker()
            self.thread = QThread()
            self.worker.moveToThread(self.thread)
            self.worker.sig_video_mode_img.connect(self.update_main_plot_win)
            self.worker.sig_hardware_mode_img.connect(self.update_image_queue)
            # control worker:
            self.sig_abort_workers.connect(self.worker.abort)
            self.thread.started.connect(self.worker.work)
            self.thread.start()  # this will emit 'started' and start thread's event loop

            # finish camera index setting, then can't change camera index during experiment,
            # if want to change camera index, then stop experiment
            self.camera_setting.cb.setEnabled(False)
            self.camera_setting.further_setting.setEnabled(True)
            self.camera_setting.apply_button.setEnabled(True)
            settings.widget_params["Image Display Setting"]["imgSource"] = "camera"
            self.acquiring = True

            if settings.widget_params["Analyse Data Setting"]["AbsTrigerStatus"]:
                self.camera_setting.hardware_mode.setChecked(True)
                self.camera_setting.hardware_mode.setEnabled(False)
                self.camera_setting.video_mode.setEnabled(False)
            else:
                settings.widget_params["Image Display Setting"]["mode"] = 0
                self.camera_setting.video_mode.setChecked(True)
                self.camera_setting.video_mode.setEnabled(False)
            # self.acquiring = True
            self.stop_exp_action.setEnabled(True)
        else:
            print("select a camera for further experiment")

    def stop_exp(self):
        """
        stop basis experiment include capturing images when image source is camera.
        :return:
        """
        self.stop_exp_action.setEnabled(False)#already stop, so connot stop
        if self.acquiring:
            self.sig_abort_workers.emit()
            self.thread.quit()  # this will quit **as soon as thread event loop unblocks**
            self.thread.wait()  # <- so you need to wait for it to *actually* quit

        self.camera_setting.AbsTriger.setEnabled(True)
        settings.widget_params["Image Display Setting"]["mode"] = 0

        self.acquiring = False
        self.start_exp_action.setEnabled(True)   # already stop can start
        self.LoadfolderAction.setEnabled(True)  #can load
        self.SaveImgAction.setEnabled(True)  #can save
        self.SaveMainImgAction.setEnabled(True)
        self.LoadImgAction.setEnabled(True)
        self.clear_img_stack_action.setEnabled(True)  #can clear stack
        self.clear_main_win_action.setEnabled(True)   #can clear all
        self.camera_setting.cb.setEnabled(True)
        self.camera_setting.further_setting.setEnabled(False)
        settings.widget_params["Image Display Setting"]["imgSource"] = "disk"

        self.camera_setting.video_mode.setChecked(False)
        self.camera_setting.hardware_mode.setChecked(False)
        self.camera_setting.video_mode.setEnabled(False)
        self.camera_setting.hardware_mode.setEnabled(False)


    def connect_slot2signal(self):

        # image display widget
        # all parameters' signal are connected to global parameters.

        self.camera_setting.video_mode.stateChanged.connect(
            lambda: self.change_camera_mode(self.camera_setting.video_mode)
        )
        self.camera_setting.hardware_mode.stateChanged.connect(
            lambda: self.change_camera_mode(self.camera_setting.hardware_mode)
        )

        # image stack widget
        for i in range(settings.widget_params["Image Display Setting"]["img_stack_num"]):
            plot_win = self.img_queue.plot_wins.get()  #得到 一个作图小窗口
            plot_win.img_dict.connect(self.plot_main_window.img_plot)
            self.img_queue.plot_wins.put(plot_win)
        # plot main window widget
        self.plot_main_window.atom_number.connect(self.result_dock.change_atom_num)
        self.plot_main_window.Pxatom_num.connect(self.result_dock.change_Pxatom_num)
        self.plot_main_window.TotalPhotons_num.connect(self.result_dock.change_TotalPhotons_num)
        self.plot_main_window.fittingdata.connect(self.Fitting_dock.change_label)
        self.Fitting_dock.fitting_jud.connect(self.plot_main_window.add_fitting)

        # analyse data widget
        self.camera_setting.roi.stateChanged.connect(
            lambda: self.plot_main_window.add_roi(self.camera_setting.roi, self.camera_setting.rawdata, self.camera_setting.cross_axes))
        self.camera_setting.rawdata.stateChanged.connect(
            lambda: self.plot_main_window.add_rawdata(self.camera_setting.rawdata))
        self.camera_setting.cross_axes.stateChanged.connect(
            lambda: self.plot_main_window.add_cross_axes(self.camera_setting.cross_axes))
        self.camera_setting.AbsTriger.stateChanged.connect(
            lambda: self.absclick(self.camera_setting.AbsTriger))
        self.camera_setting.auto_save.stateChanged.connect(
            lambda: self.autosave(self.camera_setting.auto_save))

        # camera setting widget
        self.camera_setting.apply_button.clicked.connect(self.camera_setting.camera_further_setting.change_exposure)
        self.camera_setting.apply_button.clicked.connect(self.camera_setting.camera_further_setting.change_gain)
        self.camera_setting.apply_button.clicked.connect(self.camera_setting.camera_further_setting.change_shutter)
        self.camera_setting.apply_button.clicked.connect(self.change_camera_params)

    def autosave(self,auto_save_state):
        if auto_save_state.isChecked():
            settings.widget_params["Analyse Data Setting"]["autoStatus"] = True

        else:
            settings.widget_params["Analyse Data Setting"]["autoStatus"] = False
        # print(settings.widget_params["Analyse Data Setting"]["autoStatus"])

    def absclick(self,abs_state):
        if abs_state.isChecked():
            P = 0
            for i in range(settings.widget_params["Image Display Setting"]["img_stack_num"]):
                plot_win = self.img_queue.plot_wins.get()
                if plot_win.video.image is not None:
                    P = P+1
                self.img_queue.plot_wins.put(plot_win)
            if P != 0:
                print('clear the image stack first')
                abs_state.setCheckState(0)
                settings.widget_params["Analyse Data Setting"]["AbsTrigerStatus"] = False
                return
            else:
                settings.widget_params["Analyse Data Setting"]["AbsTrigerStatus"] = True
                settings.widget_params["Image Display Setting"]["mode"] = 2
                print('Absorption imaging mode')
        else:
            settings.widget_params["Analyse Data Setting"]["AbsTrigerStatus"] = False
            settings.widget_params["Image Display Setting"]["mode"] = 0
            abs_state.setCheckState(0)
        # print(settings.widget_params["Analyse Data Setting"]["AbsTrigerStatus"])

    def clear_img_stack(self):
        """
        clear image stack
        :return:
        """
        if self.acquiring and settings.widget_params["Image Display Setting"]["mode"] == 0:
            print("video mode can't clear image stack")
            return
        # make sure that queue isn't changing when using qsize()
        for i in range(settings.widget_params["Image Display Setting"]["img_stack_num"]):
            plot_win = self.img_queue.plot_wins.get()
            plot_win.clear_win()
            self.img_queue.plot_wins.put(plot_win)

        settings.absimgData[0] = []  # Erase the last data
        settings.absimgData[1] = []
        settings.absimgData[2] = []
        settings.absimgData[3] = []

    def clear_main_win(self):
        """
              clear main windows
              :return:
              """
        if self.acquiring and settings.widget_params["Image Display Setting"]["mode"] == 0:
            print("video mode can't clear main window")
            return
        self.plot_main_window.clear_win()
        settings.imgData["Img_photon_range"] = []
        settings.imgData["Img_data"] = []


    ### LOAD CUSTOM SETTING FOR INSTRUMENT CONNECT AND PARAMETERS ###

    def file_save_imgs(self):
        """
        save image stack's images to disk
        :return:
        """
        # try:
        fpath = IOHelper.get_config_setting('DATA_PATH')
        fpath = Path(fpath)
        dir_path = fpath.joinpath(str(datetime.datetime.now()).split('.')[0].replace(' ', '-').replace(':', '_'))
        # print("save images to {}".format(dir_path))
        if settings.m_path != []:
            dir_path = settings.m_path
        if not dir_path.exists():
            dir_path.mkdir()
        for i in range(settings.widget_params["Image Display Setting"]["img_stack_num"]):
            plot_win = self.img_queue.plot_wins.get()
            if plot_win.video.image is not None:
                img_data = np.array(plot_win.video.image)
                # load image name by path
                img_name2 = (plot_win.img_label.text())[0:20].replace(' ', '~').replace(':', '').replace('-', '')
                img_name = str(img_name2)
                img_data = img_data[::-1]
                # img_data = Image.fromarray(img_data)
                # img_data.save(r"{}\{}.png".format(dir_path, img_name))
                import numpy
                numpy.savetxt(r"{}\{}.data".format(dir_path, img_name), img_data, fmt='%.2e', delimiter=' ',newline='\n', header='', footer='', comments=' ', encoding=None)
            self.img_queue.plot_wins.put(plot_win)
        print("save images to {}".format(dir_path))
        # print("images have saved.")
        # except OSError:
        #     print("Only new version files can be saved.")

    def Setpath(self):
        mpath = QFileDialog.getExistingDirectory(self, "Set path")
        settings.m_path = Path(mpath)
        self.path.setTitle('##  Save file to: ' + str(settings.m_path) + '  ##')
        # print(settings.m_path)


    def Mainwindowfile_save_imgs(self):
        # try:
        if self.plot_main_window.img.image is None:
            print("have no image in Mainwindow")
            return
        fpath = IOHelper.get_config_setting('DATA_PATH')
        fpath = Path(fpath)
        dir_path = fpath.joinpath(str(datetime.datetime.now())[2:].split('.')[0].replace(' ', '-').replace(':', '_'))
        # print("save images to {}".format(dir_path))
        if settings.m_path != []:
            dir_path = settings.m_path
        if not dir_path.exists():
            dir_path.mkdir()
        img_data = np.array(self.plot_main_window.img.image)
        # load image name by path
        img_name2 = (self.plot_main_window.img_label.text())[0:20].replace(' ', '~').replace(':', '').replace('-', '')
        img_name = str(img_name2)
        img_data = img_data[::-1]
        # img_data = Image.fromarray(img_data)
        # img_data.save(r"{}\{}.png".format(dir_path, img_name))
        import numpy
        numpy.savetxt(r"{}\{}.data".format(dir_path, img_name), img_data, fmt='%.2e', delimiter=' ', newline='\n',header='', footer='', comments=' ',encoding=None)
        print("save images to {}".format(dir_path))
        # print("images have saved.")
        # except OSError:
        #     print('Only new version files can be saved.')

    def file_load_imgs(self):
        """
        Load previous image to stack.
        :return:
        """
        settings.widget_params["Image Display Setting"]["imgSource"] = "disk"
        fpath = IOHelper.get_config_setting('DATA_PATH')

        img_fpath = QFileDialog.getOpenFileName(self, "Open File", fpath)  # name path
        strimg_fpath = str(img_fpath)
        img_file = strimg_fpath[2:len(strimg_fpath) - 19]
        img_file = Path(img_file)
        img_paths = img_file

        if img_fpath[0] != '':
            plot_win = self.img_queue.plot_wins.get()
            try:
                plot_win.img_plot(self.load_img_dict(img_paths))
                self.img_queue.plot_wins.put(plot_win)
            except TypeError:
                return
            except PermissionError:
                return

    def load_img2stack(self):#load single picture
        """
        load images to image queue, with image name and data
        """
        settings.widget_params["Image Display Setting"]["imgSource"] = "disk"
        fpath = IOHelper.get_config_setting('DATA_PATH')

        img_fpath = QFileDialog.getExistingDirectory(self, "Open File", fpath)  # name path
        img_file = Path(img_fpath)
        img_path1 = list(img_file.glob('*.png'))
        img_path2 = list(img_file.glob('*.data'))
        img_paths = img_path1 + img_path2

        for win_index in range(settings.widget_params["Image Display Setting"]["img_stack_num"]):
            if win_index == len(img_paths):
                break
            if img_paths != []:
                plot_win = self.img_queue.plot_wins.get()
                plot_win.img_plot(self.load_img_dict(img_paths[win_index]))
                self.img_queue.plot_wins.put(plot_win)

    ### MISCELLANY ###

    def load_img_dict(self, img_path):
        # pathjud = str(img_path)
        # pathjud = pathjud[len(pathjud) - 3:]   #Get the version of the file

        # if pathjud == 'ata':
        # settings.Type_of_file = 'data'
        file = open(img_path)
        linescontent = file.readlines()                     #Read the file as a behavior unit
        rows = len(linescontent)                            #get the numbers fo line
        lines = len(linescontent[0].strip().split(' '))
        # print(rows)
        # print(lines)
        img_data = np.zeros((rows, lines))                  # Initialization matrix
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
            'img_data': img_data
        }
        return img


    def update_console(self, stri):
        MAX_LINES = 50
        stri = str(stri)
        new_text = self.result_dock.console_text() + '\n' + stri
        line_list = new_text.splitlines()
        N_lines = min(MAX_LINES, len(line_list))
        # limit output lines
        new_text = '\n'.join(line_list[-N_lines:])
        self.result_dock.console_text(new_text)
        self.result_dock.automatic_scroll()
        # self.prompt.setTitle(stri)


    def update_main_plot_win(self, img_dict): #video_mode do this
        """
        Updates the main plot window at regular intervals. It designs for video mode
        """
        # take the newest image in the queue
        if img_dict is None:
            return
        self.plot_main_window.img_plot(img_dict)

    def update_image_queue(self, img_dict):   #hardware_mode do this
        # QApplication.processEvents()
        plot_win = self.img_queue.plot_wins.get()
        plot_win.img_plot(img_dict)
        img_name2 = (plot_win.img_label)[0:20].replace(' ', '~').replace(':', '').replace('-', '')
        self.img_queue.plot_wins.put(plot_win)
        if settings.widget_params["Analyse Data Setting"]["autoStatus"] == True:
            QApplication.processEvents()
            fpath = IOHelper.get_config_setting('DATA_PATH')
            fpath = Path(fpath)
            dir_path = fpath.joinpath(str(datetime.datetime.now())[2:].split('.')[0].replace(' ', '').replace(':', '_'))
            if settings.m_path != []:
                dir_path = settings.m_path
            if not dir_path.exists():
                dir_path.mkdir()
            img_data = np.array(img_dict['img_data'])
            # load image name by path
            img_name1 = settings.widget_params["Analyse Data Setting"]["Prefix"]
            # img_name2 = (self.img_label)[0:20].replace(' ', '~').replace(':', '').replace('-', '')
            img_name = str(img_name1) + str(img_name2)
            img_data = img_data[::-1]
            from numpy import savetxt
            savetxt(r"{}\{}.data".format(dir_path, img_name), img_data, fmt='%.2e', delimiter=' ', newline='\n',header='', footer='', comments=' ',encoding=None)
            print("save images to {}".format(dir_path))
        print("update image queue")


class Worker(QObject):
    """
    Must derive from QObject in order to emit signals, connect slots to other signals, and operate in a QThread.
    """

    sig_video_mode_img = pyqtSignal(dict)
    sig_hardware_mode_img = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.camera = Chameleon()
        self.camera.initializeCamera(settings.instrument_params["Camera"]["index"])
        self.camera.setAcquisitionMode(settings.widget_params["Image Display Setting"]["mode"])

        self.camera.setExposure(settings.instrument_params["Camera"]["exposure time"])
        self.camera.setShutter(settings.instrument_params["Camera"]["shutter time"])
        self.camera.setGain(settings.instrument_params["Camera"]["gain value"])
        # set a low grab timeout to avoid crash when retrieve image.
        self.camera.set_grab_timeout(grab_timeout=10)
        self.__abort = False

    @pyqtSlot()
    def work(self):
        print("camera start workt")
        self.camera.startAcquisition()
        if settings.widget_params["Analyse Data Setting"]["AbsTrigerStatus"]:
            # TestMainWindow().stop_exp_action.setEnabled(False)  # already stop, so connot stop
            settings.absimgData[0] = []  #Erase the last data
            settings.absimgData[1] = []
            settings.absimgData[2] = []
            settings.absimgData[3] = []
            for i in range(3):
                while True:
                    QApplication.processEvents()  # this could cause change to self.__abort
                    if self.__abort:
                        break

                    img_data = self.camera.retrieveOneImg()  # retrieve image from camera buffer
                    if img_data is None:
                        continue
                    else:
                        timestamp = datetime.datetime.now()
                        self.sig_hardware_mode_img.emit({'img_name': str(timestamp)[2:], 'img_data': Helper.split_list(img_data)})
                        settings.absimgData[i] = Helper.split_list(img_data)
                        break
            # time.sleep(2)
            # self.camera.stopCamera()
            # print(type(settings.absimgData[1]))
            if settings.absimgData[0] != [] and settings.absimgData[1] !=[] and settings.absimgData[2] != []:
                withatom = np.zeros((settings.absimgData[0].shape[0], settings.absimgData[0].shape[1]))
                withoutatom = np.zeros((settings.absimgData[1].shape[0], settings.absimgData[1].shape[1]))
                settings.absimgData[3] = np.zeros((settings.absimgData[1].shape[0], settings.absimgData[1].shape[1]))
                print('In the calculation')
                import warnings
                warnings.filterwarnings("ignore")
                for ii in range(settings.absimgData[1].shape[0]):
                    for jj in range(settings.absimgData[1].shape[1]):
                        withatom[ii,jj] = settings.absimgData[0][ii,jj] - settings.absimgData[2][ii,jj]####
                        withoutatom[ii,jj] = settings.absimgData[1][ii,jj] - settings.absimgData[2][ii,jj]###

                        if withoutatom[ii,jj] != 0:
                            settings.absimgData[3][ii,jj] = withatom[ii,jj] / withoutatom[ii,jj]##########
                        else:
                            settings.absimgData[3][ii, jj] = 1

                        if settings.absimgData[3][ii,jj] >= 1 or settings.absimgData[3][ii,jj] <= 0:
                            settings.absimgData[3][ii, jj] = 1

                        settings.absimgData[3][ii,jj] = -np.log(settings.absimgData[3][ii,jj])
                # print(settings.absimgData[3][0:20,0:20])
                img_name1 = settings.widget_params["Analyse Data Setting"]["Prefix"]
                timestamp = datetime.datetime.now()
                self.sig_hardware_mode_img.emit({'img_name': str(img_name1)+str(timestamp)[2:], 'img_data': settings.absimgData[3]})
                # TestMainWindow.stop_exp_action.setEnabled(True)  # already stop, so connot stop
        else:
            while True:
                # check if we need to abort the loop; need to process events to receive signals;
                QApplication.processEvents()  # this could cause change to self.__abort
                if self.__abort:
                    break

                img_data = self.camera.retrieveOneImg()  # retrieve image from camera buffer
                if img_data is None:
                    continue
                else:
                    timestamp = datetime.datetime.now()
                    if settings.widget_params["Image Display Setting"]["mode"] == 2:
                        self.sig_hardware_mode_img.emit({'img_name': str(timestamp)[2:], 'img_data': Helper.split_list(img_data)})
                    else:
                        self.sig_video_mode_img.emit({'img_name': str(timestamp)[2:], 'img_data': Helper.split_list(img_data)})
                        # set a appropriate refresh value
                        time.sleep(0.1)
        self.camera.stopCamera()

    def abort(self):
        self.__abort = True


def start_main_win():
    app = QApplication(sys.argv)
    # Force the style to be the same on all OSs:
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette() #调色板
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    app.setApplicationName("UALab")
    window = TestMainWindow()
    window.show()
    sys.exit(app.exec_())




if __name__ == "__main__":
    app = QApplication(sys.argv)
    # print(sys.argv[0][-13:-1])
    # print(sys.argv)
    # Force the style to be the same on all OSs:
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    app.setApplicationName("UALab")
    window = TestMainWindow()
    window.show()
    sys.exit(app.exec_())

