
import unittest, sys
from vslib.reader import Reader
from vslib.gui import GUI
from vslib.error import Error
from PyQt5.Qt import QApplication


class Test(unittest.TestCase):
    
    def test_wrong_file(self):

        global app
        app = QApplication(sys.argv)
        gui = GUI('error.csv', 'time', 'points',5 ,'title_1')
        gui.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    unittest.main()