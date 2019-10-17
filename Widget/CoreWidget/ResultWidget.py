import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtGui import QFont
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from Utilities.Helper import settings
from PyQt5.QtCore import *



class ResultWidget(QtWidgets.QWidget):

    """
    This class is a TextEdit with a few extra features,
    can be integrated into LabGui as a message box,which
    can be use for warning and display calculate result
    """

    def __init__(self, parent=None):
        super(ResultWidget, self).__init__(parent)

        self.flurence = QCheckBox('flurence',self)
        self.flurence.stateChanged.connect(lambda: self.change_cal(self.flurence))
        self.absorbtion = QCheckBox('absorbtion',self)
        self.absorbtion.stateChanged.connect(lambda: self.change_cal(self.absorbtion))
        self.fLayout = QtWidgets.QVBoxLayout()
        # self.onelabel = QtWidgets.QLabel('calculation rule')
        # self.fLayout.addWidget(self.onelabel)
        self.fLayout.addWidget(self.flurence)
        # self.flurence.setFont(QFont("Roman times", 18))
        self.fLayout.addWidget(self.absorbtion)
        # self.fLayout.setStretchFactor(self.onelabel, 0.5)# proportion
        self.fLayout.setStretchFactor(self.flurence, 2)
        self.fLayout.setStretchFactor(self.absorbtion, 2)
        # self.fLayout.setGeometry(300, 300)
        self.flurence.setChecked(True)
        self.flurence.setEnabled(False)
        # self.absorbtion.setChecked(False)
        # self.absorbtion.setEnabled(True)

        self.atom_num_label = QtWidgets.QLabel('Atom')
        self.atom_num_label.setFont(QFont("Roman times", 18))
        self.atom_num = QtWidgets.QLabel(str('N'))
        self.atom_num.setFont(QFont("Roman times", 24))
        self.hLayout1 = QtWidgets.QHBoxLayout()
        self.hLayout1.addWidget(self.atom_num_label)
        self.hLayout1.addWidget(self.atom_num)

        self.TotalPhotons_num_label = QtWidgets.QLabel('TotalPhotons')
        self.TotalPhotons_num_label.setFont(QFont("Roman times", 18))
        self.TotalPhotons_num = QtWidgets.QLabel(str('N'))
        self.TotalPhotons_num.setFont(QFont("Roman times", 24))
        self.hLayout3 = QtWidgets.QHBoxLayout()
        self.hLayout3.addWidget(self.TotalPhotons_num_label)
        self.hLayout3.addWidget(self.TotalPhotons_num)

        self.atom_numpx_label = QtWidgets.QLabel('Atom/px')
        self.atom_numpx_label.setFont(QFont("Roman times", 18))
        self.atom_numpx = QtWidgets.QLabel(str('N'))
        self.atom_numpx.setFont(QFont("Roman times", 24))
        self.hLayout2 = QtWidgets.QHBoxLayout()
        self.hLayout2.addWidget(self.atom_numpx_label)
        self.hLayout2.addWidget(self.atom_numpx)

        self.wLayout = QtWidgets.QVBoxLayout()
        self.wLayout.addLayout(self.hLayout3)
        self.wLayout.addLayout(self.hLayout1)
        self.wLayout.addLayout(self.hLayout2)

        self.totalLayout = QtWidgets.QHBoxLayout()
        self.totalLayout.addLayout(self.fLayout)
        self.totalLayout.addLayout(self.wLayout)
        self.totalLayout.setStretchFactor(self.fLayout, 1)
        self.totalLayout.setStretchFactor(self.wLayout, 4)
        self.setLayout(self.totalLayout)

        self.prompt = QDialog()  # create a dialog
        self.consoleTextEdit = QtWidgets.QTextEdit()
        self.consoleTextEdit.setReadOnly(True)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.addWidget(self.consoleTextEdit)
        self.prompt.setLayout(self.verticalLayout)

        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setFixedHeight(screen.width()*(9/16)*20/100)
        # self.prompt.setFixedWidth(screen.width()*50/100)


    def promptset(self):
        self.prompt.setWindowTitle('prompt')
        self.prompt.setWindowModality(Qt.NonModal)
        self.prompt.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.prompt.show()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.promptset()

    def console_text(self, new_text=None):

        """get/set method for the text in the console"""

        if new_text == None:

            return str((self.consoleTextEdit.toPlainText())).rstrip()

        else:

            self.consoleTextEdit.setPlainText(new_text)

    def automatic_scroll(self):
        """
        performs an automatic scroll up
        the latest text shall always be in view
        """
        sb = self.consoleTextEdit.verticalScrollBar()
        sb.setValue(sb.maximum())

    def change_cal(self,mode):
        if mode.isChecked():
            if mode.text() == 'flurence':
                settings.widget_params["calculate Setting"]["mode"] = 0
                self.absorbtion.setEnabled(True)
                self.absorbtion.setChecked(False)
                self.flurence.setEnabled(False)
                # print(settings.widget_params["calculate Setting"]["mode"])

            elif mode.text() == 'absorbtion':
                settings.widget_params["calculate Setting"]["mode"] = 1
                self.flurence.setEnabled(True)
                self.flurence.setChecked(False)
                self.absorbtion.setEnabled(False)
                # print(settings.widget_params["calculate Setting"]["mode"])


    def change_atom_num(self, atom_num):
        self.atom_num.setText(str('%.3e' % atom_num))

    def change_TotalPhotons_num(self, TotalPhotons_num):
        self.TotalPhotons_num.setText(str('%.3e' % TotalPhotons_num))

    def change_Pxatom_num(self, Pxatom_num):
        self.atom_numpx.setText(str('%.3e' % Pxatom_num))


