import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtGui import QFont
from PyQt5 import QtGui


class ResultWidget(QtWidgets.QWidget):

    """
    This class is a TextEdit with a few extra features,
    can be integrated into LabGui as a message box,which
    can be use for warning and display calculate result
    """

    def __init__(self, parent=None):
        super(ResultWidget, self).__init__(parent)

        self.atom_num_label = QtWidgets.QLabel('Atom#')
        self.atom_num_label.setFont(QFont("Roman times", 18))
        self.atom_num = QtWidgets.QLabel(str(0))
        self.atom_num.setFont(QFont("Roman times", 24))
        self.hLayout1 = QtWidgets.QHBoxLayout()
        self.hLayout1.addWidget(self.atom_num_label)
        self.hLayout1.addWidget(self.atom_num)

        self.atom_numpx_label = QtWidgets.QLabel('Atom#/px')
        self.atom_numpx_label.setFont(QFont("Roman times", 14))
        self.atom_numpx = QtWidgets.QLabel(str(0))
        self.atom_numpx.setFont(QFont("Roman times", 20))
        self.hLayout2 = QtWidgets.QHBoxLayout()
        self.hLayout2.addWidget(self.atom_numpx_label)
        self.hLayout2.addWidget(self.atom_numpx)

        self.wLayout = QtWidgets.QVBoxLayout()
        self.wLayout.addLayout(self.hLayout1)
        self.wLayout.addLayout(self.hLayout2)
        self.setLayout(self.wLayout)

        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setFixedSize(screen.width()*34/100,screen.height()*19/100)

    def change_atom_num(self, atom_num):

        self.atom_num.setText(str(atom_num))

    def change_Pxatom_num(self, Pxatom_num):

        self.atom_numpx.setText(str(Pxatom_num))


