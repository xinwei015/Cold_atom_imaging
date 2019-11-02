import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
from Utilities.IO import IOHelper
from pathlib import Path


class print_redirect(QObject):
    """
    replace stdout that both prints and emits the text as a signal

    """
    print_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.old_stdout = sys.stdout

    def write(self, stri):
        self.old_stdout.write(stri)
        # emit the stdout statements
        # print('1')
        self.print_signal.emit(stri)

    def flush(self):
        self.old_stdout.flush()


def create_action(parent, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False):
    action = QAction(text, parent)
    if icon is not None:
        icpath = IOHelper.get_configt_setting('DATA_PATH')
        # icpath = Path(icpath)
        icpath = str(icpath).replace('\\','/')
        action.setIcon(QIcon(icpath + "/%s.png" % icon))
    if shortcut is not None:
        action.setShortcut(shortcut)
    if tip is not None:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    if slot is not None:
        action.triggered.connect(slot)
    if checkable:
        action.setCheckable(True)
    return action


def split_list(image):
    """
    design for Chameleon camera, take the  image to array
    :param image: list
    :return:
    """
    alist = []
    img_rows = image.getRows()
    img_cols = image.getCols()
    img_data = image.getData()
    # print(img_data)
    # print(img_rows)
    # print(img_cols)
    for i in range(img_rows):
        alist.append(img_data[i*img_cols:(i+1)*img_cols])
    # print(np.array(alist))

    return np.array(alist)

