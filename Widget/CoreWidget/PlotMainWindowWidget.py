import pyqtgraph as pg
from pyqtgraph.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from scipy import optimize
from Model.DataAnalysis.CaculateAtoms import *
from decimal import *
from copy import deepcopy
getcontext().prec = 4#Set significant number


class PlotMainWindow(QWidget):

    atom_number = pyqtSignal(object)
    Pxatom_num = pyqtSignal(object)
    TotalPhotons_num = pyqtSignal(object)
    fittingdata = pyqtSignal(dict)


    def __init__(self):
        super(PlotMainWindow, self).__init__()
        self.layout = QVBoxLayout(self)

        # win = pg.GraphicsView()
        l = pg.GraphicsLayout(border=(100, 100, 100))
        win = pg.GraphicsLayoutWidget()
        win.setCentralItem(l)
        pg.setConfigOptions(imageAxisOrder='row-major')
        # pg.setConfigOptions(leftButtonPan=False)
        self.viewBox = l.addPlot()
        self.viewBox.hideAxis('left')#hide the left and right
        self.viewBox.hideAxis('bottom')
        self.img = pg.ImageItem()
        self.viewBox.setMouseEnabled(x=False, y=False)#make image can not move
        # pg.setConfigOptions(leftButtonPan=False)
        self.viewBox.addItem(self.img)
        self.layout.addWidget(win)
        self.img_label = QLabel()
        self.layout.addWidget(self.img_label)
        self.setLayout(self.layout)
        self.h_axes = None
        self.v_axes = None
        self.data = None
        self.data_shape = None
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setFixedSize(screen.width()*44/100,screen.width()*(9/16)*63/100)
        # print(self.width(), self.height())


    def add_roi(self, roi_cbk_state, axes_cbk_state, line_cbk_state):
        if roi_cbk_state.isChecked():
            # video mode doesn't have roi statistics
            if settings.widget_params["Image Display Setting"]["imgSource"] == "camera":
                if settings.widget_params["Image Display Setting"]["mode"] == 0:
                    print("video mode doesn't have roi statistics, please choose another mode.")
                    # 0 doesn't check, 2 means check
                    roi_cbk_state.setCheckState(0)
                    settings.widget_params["Analyse Data Setting"]["roiStatus"] = False
                    return
            if self.data is None:
                print("Main plot window doesn't handle image, please load image first")
                roi_cbk_state.setCheckState(0)
                settings.widget_params["Analyse Data Setting"]["roiStatus"] = False
                return
            self.roi = pg.ROI([300, 300], [100, 100], maxBounds=QtCore.QRect(0, 0, self.data_shape[1], self.data_shape[0]),removable=True)
            self.roi.setPen(color='r', width=3)  # set roi width and color
            self.roi.addScaleHandle([0.5, 1], [0.5, 0.5])
            self.roi.addScaleHandle([0, 0.5], [0.5, 0.5])

            self.viewBox.addItem(self.roi)
            # make sure ROI is drawn above image
            self.roi.setZValue(10)
            # if settings.widget_params["Analyse Data Setting"]["add_ten"]:
            # self.vLine = pg.InfiniteLine(angle=90, movable=False)
            # self.hLine = pg.InfiniteLine(angle=0, movable=False)
            # self.vLine.setPen(color='r', width=3)
            # self.hLine.setPen(color='r', width=3)
            # self.vLine.setPos(self.roi.pos()[0]+self.roi.size()[0]/2)
            # self.hLine.setPos(self.roi.pos()[1]+self.roi.size()[1]/2)
            # self.viewBox.addItem(self.vLine, ignoreBounds=True)
            # self.viewBox.addItem(self.hLine, ignoreBounds=True)
            self.roi.sigRegionChanged.connect(self.update_ch_fitting_cs)
            self.roi.sigRegionChanged.connect(self.calculate_roi)
            settings.widget_params["Analyse Data Setting"]["roiStatus"] = True
        else:
            roi_cbk_state.setCheckState(0)
            axes_cbk_state.setCheckState(0)
            line_cbk_state.setCheckState(0)
            settings.widget_params["Analyse Data Setting"]["roiStatus"] = False
            settings.widget_params["Analyse Data Setting"]["add_rawdata"] = False
            # remove viewBox's items
            # self.viewBox.clear()
            # add image item
            self.viewBox.removeItem(self.roi)


    def add_rawdata(self, cbk_state):
        if cbk_state.isChecked():
            if settings.widget_params["Analyse Data Setting"]["roiStatus"]:
                settings.widget_params["Analyse Data Setting"]["add_rawdata"] = True
                # add horizontal axes and vertical axes
                self.h_axes = self.viewBox.plot()
                self.h_axes.setPen(color='y', width=2)#x
                # TODO: vertical axes hasn't finishe
                self.v_axes = self.viewBox.plot()
                self.v_axes.setPen(color='y', width=2)

            else:
                print("please add roi first.")
                # 0 doesn't check, 2 means check
                cbk_state.setCheckState(0)
                settings.widget_params["Analyse Data Setting"]["add_rawdata"] = False
                return
        else:
            cbk_state.setCheckState(0)
            self.viewBox.removeItem(self.h_axes)
            self.viewBox.removeItem(self.v_axes)

            if settings.widget_params["Analyse Data Setting"]["roiStatus"]:
                self.viewBox.addItem(self.roi)
            settings.widget_params["Analyse Data Setting"]["add_rawdata"] = False
            # remove plotItem if cross axes has added
            if self.h_axes is not None and self.v_axes is not None:
                self.viewBox.removeItem(self.h_axes)
                self.viewBox.removeItem(self.v_axes)

    def add_fitting(self):
        if settings.widget_params["Fitting Setting"]["mode"] == 1:
            self.h_axes2 = self.viewBox.plot()
            self.h_axes2.setPen(color='w', width=2)  # x
            self.v_axes2 = self.viewBox.plot()
            self.v_axes2.setPen(color='w', width=2)
        else:
            self.viewBox.removeItem(self.h_axes2)
            self.viewBox.removeItem(self.v_axes2)

    def add_cross_axes(self, cbk_state):
        if cbk_state.isChecked():
            if settings.widget_params["Analyse Data Setting"]["roiStatus"]:
                settings.widget_params["Analyse Data Setting"]["add_cross_axes"] = True
                self.vLine = pg.InfiniteLine(angle=90, movable=False)
                self.hLine = pg.InfiniteLine(angle=0, movable=False)
                self.vLine.setPen(color='r', width=3)
                self.hLine.setPen(color='r', width=3)
                self.vLine.setPos(self.roi.pos()[0] + self.roi.size()[0] / 2)
                self.hLine.setPos(self.roi.pos()[1] + self.roi.size()[1] / 2)
                self.viewBox.addItem(self.vLine, ignoreBounds=True)
                self.viewBox.addItem(self.hLine, ignoreBounds=True)
            else:
                settings.widget_params["Analyse Data Setting"]["add_cross_axes"] = False
                print("please add roi first.")
                cbk_state.setCheckState(0)
                return
        else:
            cbk_state.setCheckState(0)
            try:
                self.viewBox.removeItem(self.vLine)
                self.viewBox.removeItem(self.hLine)
            except AttributeError:
                pass

    def update_ch_fitting_cs(self):
        if settings.widget_params["Analyse Data Setting"]["add_cross_axes"]:
            self.vLine.setPos(self.roi.pos()[0]+self.roi.size()[0]/2)
            self.hLine.setPos(self.roi.pos()[1]+self.roi.size()[1]/2)
        if settings.widget_params["Analyse Data Setting"]["add_rawdata"] or settings.widget_params["Fitting Setting"]["mode"] == 1:

            h_data = self.data[int(self.roi.pos()[1] + self.roi.size()[1] / 2), :]
            num_h = range(len(h_data))
            num_h_data = list(num_h)

            v_data = self.data[:, int(self.roi.pos()[0] + self.roi.size()[0] / 2)]
            num_v = range(len(v_data))
            num_v_data = list(num_v)

            # vlen = np.ones(len(v_data))# make it at right
            # vlenlist = list(len(h_data) * vlen)
            # v_data = list(map(lambda x: x[0] - x[1], zip(vlenlist, v_data)))
            # print(self.roi.pos())
            # num_v_data = list([x*len(h_data) for x in num_v_data])
            if settings.widget_params["Fitting Setting"]["mode"] == 1:
                num_h_data2 = num_h_data[int(self.roi.pos()[0]): int(self.roi.pos()[0] + self.roi.size()[0])]
                num_h_data2 = np.array(num_h_data2)
                h_data2 = self.data[int(self.roi.pos()[1] + self.roi.size()[0] / 2), int(self.roi.pos()[0]) : int(self.roi.pos()[0] + self.roi.size()[1])]
                h_data2 = np.array(h_data2)
                import warnings
                warnings.filterwarnings("ignore")#撤销runtimewarning提醒
                p0 = [1 ,int(self.roi.pos()[1] + self.roi.size()[0] / 2), int(self.roi.size()[0] / 2), 0]
                plesq = optimize.leastsq(residuals, p0, args=(h_data2, num_h_data2))
                list1 = [plesq[0][0],plesq[0][1],plesq[0][2],plesq[0][3]]
                list1[3] = 0  #tuple cannot change, so list it
                if list1[0] < 0 or list1[0] > 2000 or list1[1] > 1500or list1[0] < 0 or abs(list1[2]) > 100:
                    list1 = [0,0,0,0]       #When the fitting data deviates too much, do not draw, Same thing down here.

                list1 = np.array(tuple(list1))
                h_data2 = peval(num_h_data, list1)

                num_v_data2 = num_v_data[int(self.roi.pos()[1]): int(self.roi.pos()[1] + self.roi.size()[1])]
                num_v_data2 = np.array(num_v_data2)
                # v_data2 = self.data[int(self.roi.pos()[0] + self.roi.size()[0] / 2), int(self.roi.pos()[1]): int(self.roi.pos()[1] + self.roi.size()[1])]
                v_data2 = self.data[int(self.roi.pos()[1]): int(self.roi.pos()[1] + self.roi.size()[1]), int(self.roi.pos()[0] + self.roi.size()[0] / 2)]
                v_data2 = np.array(v_data2)
                p1 = [1, int(self.roi.pos()[0] + self.roi.size()[1] / 2), int(self.roi.size()[1] / 2), 0]
                plesq2 = optimize.leastsq(residuals, p1, args=(v_data2, num_v_data2))
                list2 = [plesq2[0][0], plesq2[0][1], plesq2[0][2], plesq2[0][3]]
                # if list2[2] > 1500:
                list2[3] = 0
                if list2[0] < 0 or list2[0] > 2000 or list2[1] > 1500 or list2[0] < 0 or abs(list2[2]) > 100:
                    list2 = [0, 0, 0, 0]   #

                list2 = np.array(tuple(list2))
                v_data2 = peval(num_v_data, list2)
                data7 = abs(2*np.pi*np.sqrt(plesq[0][0]*plesq2[0][0])*plesq[0][2]*plesq2[0][2])
                CCDPlSize = [3.75, 3.75]
                Magnification = settings.widget_params["Analyse Data Setting"]["magValue"]
                data8 = plesq[0][2]*CCDPlSize[0]*Magnification*1E-3
                data9 = plesq2[0][2]*CCDPlSize[1]*Magnification*1E-3
                self.fittingdata.emit({'data1': plesq[0][0] , 'data2': plesq[0][1], 'data3': plesq[0][2], 'data4': plesq2[0][0],'data5': plesq2[0][1], 'data6': plesq2[0][2],'data7': data7, 'data8': data8,'data9': data9})
                self.h_axes2.setData(num_h_data, h_data2)
                self.v_axes2.setData(v_data2, num_v_data)
            if settings.widget_params["Analyse Data Setting"]["add_rawdata"]:
                self.h_axes.setData(num_h_data, h_data)
                self.v_axes.setData(v_data, num_v_data)


    def calculate_roi(self):
        # [(lower-left corner), (size)]
        # pos = left down corner(x,y) note: x means normal x axis
        # size = (roi_height, roi_width)
        # roi = {'pos': [int(self.roi.pos()[0]), int(self.roi.pos()[1])], 'size': [int(self.roi.size()[0]), int(self.roi.size()[1])]}
        # calculate atom number
        if self.roi.pos()[0] < 0 or self.roi.pos()[1] < 0 or self.roi.size()[1] > self.data_shape[1] or self.roi.size()[0] > self.data_shape[0]:
            return
        if len(self.data_shape) == 3:
            # three channel data
            # atom_num = sum(sum(self.data[int(self.roi.pos()[1]):int(self.roi.pos()[1]+self.roi.size()[0]), int(self.roi.pos()[0]):int(self.roi.pos()[0]+self.roi.size()[1]), 1]))
            # TotalPhotons = 7.11e2   #for test
            # global TotalPhotons ,calculatedata ,atom_num
            TotalPhotons = sum(sum(self.data[int(self.roi.pos()[1]):int(self.roi.pos()[1] + self.roi.size()[0]),int(self.roi.pos()[0]):int(self.roi.pos()[0] + self.roi.size()[1]), 1]))
            calculatedata = calculateAtom(TotalPhotons)
            atom_num = round(calculatedata[0])
        else:
            # single channel
            TotalPhotons = sum(sum(self.data[int(self.roi.pos()[1]):int(self.roi.pos()[1] + self.roi.size()[0]), int(self.roi.pos()[0]):int(self.roi.pos()[0] + self.roi.size()[1])]))
            calculatedata = calculateAtom(TotalPhotons)
            atom_num = round(calculatedata[0])
        TotalPhotons = Decimal(1) * Decimal(TotalPhotons)
        TotalPhotons = round(TotalPhotons)
        ROIsize = self.roi.size()[0]*self.roi.size()[1]
        Pxatom_num = atom_num/(ROIsize)
        Pxatom_num = Decimal(1) * Decimal(Pxatom_num)#Out number
        Pxatom_num = round(Pxatom_num)
        # Pxatom_num = Decimal(1) * Decimal(Pxatom_num)
        atom_num = Decimal(1) * Decimal(atom_num)
        self.TotalPhotons_num.emit(TotalPhotons)
        self.atom_number.emit(atom_num)
        self.Pxatom_num.emit(Pxatom_num)
        # print(settings.imgData["ROI_size"])


    def img_plot(self, img_dict):
        """
        design for software mode and hardware mode, choose image from image stack to display in main window
        :param img_dict:
        :return:
        """
        self.img.setImage(img_dict['img_data'])
        self.data = img_dict['img_data']
        self.data_shape = self.data.shape
        self.img_label.setText(img_dict['img_name'])
        #Set the initial axis so that the size of the image remains the same when the axis is added
        numh = range(self.data_shape[1])
        numh = list(numh)
        numhd = np.zeros(self.data_shape[1])
        numv = range(self.data_shape[0])
        numv = list(numv)
        numvd = np.zeros(self.data_shape[0])
        self.h_axesm = self.viewBox.plot()
        self.h_axesm.setPen(color='k', width=2)  # x
        self.h_axesm.setData(numh, numhd)
        self.v_axesm = self.viewBox.plot()
        self.v_axesm.setPen(color='k', width=2)
        self.v_axesm.setData(numvd, numv)

    def img_plot2(self):
        if settings.imgData["BkgImg"] !=[] and settings.imgData["Img_data"] !=[]:
            settings.imgData["Img_data"] = settings.imgData["Img_data"] - settings.imgData["BkgImg"]
            self.img.setImage(settings.imgData["Img_data"])
            self.data = settings.imgData["Img_data"]
            self.data_shape = settings.imgData["Img_data"].shape
        else:
            print('Please check again')

    def img_plot3(self):
        if settings.imgData["Img_data"] != []:
            settings.imgData["Img_photon_range"] = deepcopy(settings.imgData["Img_data"])
            for i in range(settings.imgData["Img_data"].shape[0]):
                for j in range(settings.imgData["Img_data"].shape[1]):
                    if settings.imgData["Img_data"][i,j] <= settings.widget_params["Image Display Setting"]["pfMin"]:
                        settings.imgData["Img_photon_range"][i,j] = settings.widget_params["Image Display Setting"]["pfMin"]
                    if settings.imgData["Img_data"][i,j] >= settings.widget_params["Image Display Setting"]["pfMax"]:
                        settings.imgData["Img_photon_range"][i,j] = settings.widget_params["Image Display Setting"]["pfMax"]

            self.img.setImage(settings.imgData["Img_photon_range"])
            self.data = settings.imgData["Img_photon_range"]
            self.data_shape = settings.imgData["Img_photon_range"].shape
            # print('photon filter ： finish.')
        else:
            print('No image')


    def clear_win(self):
        self.viewBox.clear()
        # add image item
        self.viewBox.addItem(self.img)
        if self.img is None:
            return
        self.img.clear()
        self.img_label.setText('')
        self.data = None
        self.data_shape = None

def func(xx, aa, bb, cc, dd):
    return aa * np.e ** (-((xx - bb) ** 2) / 2 / cc ** 2) + dd

# def logistic4(x, A, B, C, D):
#     return (A-D)/(1+(x/C)**B)+D

def residuals(p, y, x):
    [A, B, C, D] = p
    return y - func(x, A, B, C, D)

def peval(x, p):
    [A, B, C, D] = p
    return func(x, A, B, C, D)





