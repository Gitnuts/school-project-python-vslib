
import unittest, sys, os
from vslib.reader import Reader
from vslib.gui import GUI
from vslib.error import Error
from PyQt5.Qt import QApplication

class Plot:
    
    def __init__(self,name):
        
        if name == 'example':
            global app
            app = QApplication(sys.argv)
            
            ''' You need to change absolute path to yours! '''
            
            gui = GUI('vslib/test_examples/Example.csv', 'time', 'points', 5 ,name)
            gui.show()
            sys.exit(app.exec_())
        else:
            self.name = name


class Lineplot(Plot):
    
    def __init__(self,name, xlabel, ylabel, grid, title):
        
        super().__init__(name)
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.grid = grid
        self.title = title
        self.plot(name, xlabel, ylabel, grid, title)
    
    def plot(self, name, xlabel, ylabel, grid, title):
        
        global app
        app = QApplication(sys.argv)
        gui = GUI(name, xlabel, ylabel, grid, title)
        gui.show()
        sys.exit(app.exec_())
        
        
class Barplot(Plot):
    
    def __init__(self,name, xlabel, ylabel, grid, title):
        
        super().__init__(name)
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.grid = grid
        self.title = title
    
    pass
        
        

        
if __name__ == '__main__':
    unittest.main()