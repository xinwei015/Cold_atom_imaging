"""
    Starting point for running the program.
"""


from multiprocessing import Process
from MainWindow import start_main_win
from Utilities.IO.IOHelper import create_config_file,create_configt_file

if __name__ == '__main__':
    create_config_file()
    create_configt_file()
    p = Process(target=start_main_win)
    p.start()
    p.join()
    # start_main_win()
