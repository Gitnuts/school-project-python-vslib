
from vslib.reader import Reader
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.Qt import QColor, QGraphicsTextItem
from PyQt5.QtGui import QPainter, QPen
import sys
from PyQt5.QtWidgets import QApplication, QGraphicsItem, QGraphicsScene, QGraphicsView, QGraphicsPolygonItem
from PyQt5.Qt import QRectF, QGraphicsLineItem, QPainter, QGraphicsScene, Qt, QColor, QGraphicsPolygonItem
from _socket import close
from vslib.error import Error

class GUI(QtWidgets.QMainWindow):
    
    
    def __init__(self,name,label_x,label_y,scale,title):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget())
        self.horizontal = QtWidgets.QHBoxLayout()
        self.centralWidget().setLayout(self.horizontal)
        self.init_window()
        self.name = name
        self.label_x = label_x
        self.label_y = label_y
        self.scale = scale
        self.title = title
        self.add_grid(scale)
        self.draw_axis(name)
        self.init_labels(label_x, label_y)
        self.init_title(title)
       
    def init_window(self):


        self.setGeometry(300, 300, 800, 800)
        self.show()

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, 400, 400)

    
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        self.horizontal.addWidget(self.view)
        
        side1 = QGraphicsLineItem(-15,0,515,0)
        side2 = QGraphicsLineItem(0,-15,0,515)
        side3 = QGraphicsLineItem(-15,500,515,500)
        side4 = QGraphicsLineItem(500,-15,500,515)
        
        side1.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        side2.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        side3.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        side4.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        
        x = 1
        while x!= 5:
            segment1 = QGraphicsLineItem(-10,500*x/5,10,500*x/5)
            segment2 = QGraphicsLineItem(500*x/5,490,500*x/5,510)
            self.scene.addItem(segment1)
            self.scene.addItem(segment2)
            
            x = x+1
            
        self.scene.addItem(side1)
        self.scene.addItem(side2)
        self.scene.addItem(side3)
        self.scene.addItem(side4)
        self.set_legend()

    def draw_axis(self,name):
        
        try:
            file = open(name)
        except FileNotFoundError:
            raise Error('wrong file')
            
        x,y,x_max,x_min,y_max,y_min = Reader(file).read_csv_file()
        
        if x_min >= 0:
            edge_x = 500
            MODE_X = 0
        if y_min >= 0:
            edge_y = 0
            MODE_Y = 0
            
        if x_min < 0 and x_max > 0:
            
            coef_x = abs(x_max)
            if abs(x_min)>=abs(x_max):
                coef_x = abs(x_max)
                edge_x = 500 - 500 * coef_x / x
            else:
                coef_x = abs(x_max)
                edge_x = 500 - 500 * coef_x / x

            MODE_X = 1
            
        if y_min < 0 and y_max > 0:
            if abs(y_min)>=abs(x_max):
                coef_y = abs(y_max)
                edge_y = 500 * coef_y / y
            else:
                
                coef_y = abs(y_min)
                edge_y = 500-500 * coef_y / y

            MODE_Y = 1
            
        if x_max <= 0:
            edge_x = 500
            MODE_X = 2
            
        if y_max <= 0:
            edge_y = 500
            MODE_Y = 2
            
        if MODE_X != 1:
            if MODE_X == 0:
                new_edge_x = 0
            elif MODE_X == 2:
                new_edge_x = 500
            
            line_y = QGraphicsLineItem(new_edge_x,0,new_edge_x,500)
        else:
            line_y = QGraphicsLineItem(edge_x,0,edge_x,500)
            
        if MODE_Y != 1:
            if MODE_Y == 0:
                new_edge_y = 500
            elif MODE_Y == 2:
                new_edge_y = 0
            line_x = QGraphicsLineItem(0,new_edge_y,500,new_edge_y)    
        else:
            line_x = QGraphicsLineItem(0,edge_y,500,edge_y)
            
      
        line_x.setPen(QtGui.QPen(QtCore.Qt.black, 4))
        line_y.setPen(QtGui.QPen(QtCore.Qt.black, 4))

        
        self.scene.addItem(line_x)
        self.scene.addItem(line_y)
        
        file.close()
        
        self.draw_line(x,y,edge_x,edge_y,x_max,x_min,y_max,y_min,MODE_X,MODE_Y,name)
        self.write_scale(x,y,x_max,x_min,y_max,y_min, MODE_X, MODE_Y)
           
        return x,y
         
    def add_grid(self, scale):
        nom = scale *5
        try:
            if scale != int(scale):
                raise Error('input is not integer')
        except ValueError:
            raise Error('wrong input for grid')
        x = 1
        if scale >= 1:
            while x != nom:
                grid_line_y = QGraphicsLineItem(x*500/nom,0,x*500/nom,500)
                grid_line_y.setPen(QColor(180,180,180))
                grid_line_x = QGraphicsLineItem(0,x*500/nom,500,x*500/nom)
                grid_line_x.setPen(QColor(180,180,180))
                self.scene.addItem(grid_line_x)
                self.scene.addItem(grid_line_y)
                x = x+1
        elif scale == 0:
            pass
        else:
            raise Error('incorrect input for grid')
            
    def draw_line(self,x,y,edge_x,edge_y,x_max,x_min,y_max,y_min, MODE_X, MODE_Y,name):
    
        try:
            file = open(name)
        except FileNotFoundError:
            raise Error('wrong file')
            
        fun = 0
        k = 0
        list = []
        while fun != '':
            fun = Reader(file).read_line()
            n = fun.rstrip().split(",")
            list.append(n)
            
            if k > 0:

                
                try:
                    float(list[k-1][0]) and float(list[k-1][1])
                except ValueError:
                    raise Error('wrong data, ValueError')
                
                if len(list[k]) > 1:
                    try:
                        float(list[k][0]) and float(list[k][1])
                    except ValueError:
                        raise Error('wrong file')
                    
                if list[k] != ['']:
                    
                    if MODE_X == 0 and MODE_Y == 0:
                        line = QGraphicsLineItem(float(list[k-1][0])*500/x_max,(1-float(list[k-1][1])/y_max)*500,float(list[k][0])*500/x_max,(1-float(list[k][1])/y_max)*500)
                        
                    if MODE_X == 1 and MODE_Y == 1:
                        line = QGraphicsLineItem(edge_x+float(list[k-1][0])*500/x,edge_y-float(list[k-1][1])*500/y,edge_x+float(list[k][0])*500/x,edge_y-float(list[k][1])*500/y)
                        
                    if MODE_X == 1 and MODE_Y == 0:
                        line = QGraphicsLineItem(edge_x+float(list[k-1][0])*500/x, (1-float(list[k-1][1])/y_max)*500, edge_x+float(list[k][0])*500/x,(1-float(list[k][1])/y_max)*500)
                        
                    if MODE_X == 0 and MODE_Y == 1:
                        line = QGraphicsLineItem(float(list[k-1][0])*500/x_max, edge_y-float(list[k-1][1])*500/y, float(list[k][0])*500/x_max, edge_y-float(list[k][1])*500/y)
                    
                    if MODE_X == 2 and MODE_Y == 2:
                        line = QGraphicsLineItem((1-float(list[k-1][0])/x_min)*500,float(list[k-1][1])*500/y_min,(1-float(list[k][0])/x_min)*500,float(list[k][1])*500/y_min)
                        
                    if MODE_X == 0 and MODE_Y == 2:
                        line = QGraphicsLineItem(float(list[k-1][0])*500/x_max,float(list[k-1][1])*500/y_min,float(list[k][0])*500/x_max,float(list[k][1])*500/y_min)
                        
                    if MODE_X == 2 and MODE_Y == 0:
                        line = QGraphicsLineItem((1-float(list[k-1][0])/x_min)*500,(1-float(list[k-1][1])/y_max)*500,(1-float(list[k][0])/x_min)*500,(1-float(list[k][1])/y_max)*500)
                        
                    if MODE_X == 1 and MODE_Y == 2:
                        line = QGraphicsLineItem(edge_x+float(list[k-1][0])*500/x,float(list[k-1][1])*500/y_min,edge_x+float(list[k][0])*500/x,float(list[k][1])*500/y_min)
                        
                    if MODE_X == 2 and MODE_Y == 1:
                        line = QGraphicsLineItem((1-float(list[k-1][0])/x_min)*500,edge_y-float(list[k-1][1])*500/y,(1-float(list[k][0])/x_min)*500,edge_y-float(list[k][1])*500/y)
                    
                    line.setPen(QtGui.QPen(QtCore.Qt.blue, 2))        
                   
                    self.scene.addItem(line)
   
            k = k+1
        file.close()
        
    def write_scale(self, x,y,x_max,x_min,y_max,y_min, MODE_X, MODE_Y):
        
        k = 0
        while k!= 6:
            
            if MODE_X == 0 and MODE_Y == 0:
                
                d1 = k * x_max/5
                d2 = k * y_max/5
                text1 = QGraphicsTextItem(str(round(d1,2)))
                text2 = QGraphicsTextItem(str(round(d2,2)))
                text1.setPos(d1/x_max*490,520)
                text2.setPos(-60,490-d2/y_max*490)
                
            if MODE_X == 1 and MODE_Y == 1:
                
                d1 = x_min + k*x/5
                d2 = y_min + k*y/5
                text1 = QGraphicsTextItem(str(round(d1,2)))
                text2 = QGraphicsTextItem(str(round(d2,2)))
                text1.setPos((d1 - x_min)/x * 490,520)
                text2.setPos(-60,490-(d2-y_min)/y*490)
                
            if MODE_X == 1 and MODE_Y == 0:
                
                d1 = x_min + k*x/5
                d2 = k * y_max/5
                text1 = QGraphicsTextItem(str(round(d1,2)))
                text2 = QGraphicsTextItem(str(round(d2,2)))
                text1.setPos((d1 - x_min)/x * 490,520)
                text2.setPos(-60,490-d2/y_max*490)
                
            if MODE_X == 0 and MODE_Y == 1:
                
                d1 = k * x_max/5
                d2 = y_min + k*y/5
                text1 = QGraphicsTextItem(str(round(d1,2)))
                text2 = QGraphicsTextItem(str(round(d2,2)))
                text1.setPos(d1/x_max*490,520)
                text2.setPos(-60,490-(d2-y_min)/y*490)
                
            if MODE_X == 2 and MODE_Y == 2:
                
                d1 = x_min - k * x_min/5
                d2 = y_min - k * y_min/5
                text1 = QGraphicsTextItem(str(round(d1,2)))
                text2 = QGraphicsTextItem(str(round(d2,2)))
                text1.setPos(abs(x_min-d1)/abs(x_min)*490,520)
                text2.setPos(-60,490-abs(y_min-d2)/abs(y_min)*490)
                
            if MODE_X == 0 and MODE_Y == 2:
                
                d1 = k * x_max/5
                d2 = y_min - k * y_min/5
                text1 = QGraphicsTextItem(str(round(d1,2)))
                text2 = QGraphicsTextItem(str(round(d2,2)))
                text1.setPos(d1/x_max*490,520)
                text2.setPos(-60,490-abs(y_min-d2)/abs(y_min)*490)
                
            if MODE_X == 2 and MODE_Y == 0:
                
                d1 = x_min - k * x_min/5
                d2 = k * y_max/5
                text1 = QGraphicsTextItem(str(round(d1,2)))
                text2 = QGraphicsTextItem(str(round(d2,2)))
                text1.setPos(abs(x_min-d1)/abs(x_min)*490,520)
                text2.setPos(-60,490-d2/y_max*490)
                
            if MODE_X == 1 and MODE_Y == 2:
                
                d1 = x_min + k*x/5
                d2 = y_min - k * y_min/5
                text1 = QGraphicsTextItem(str(round(d1,2)))
                text2 = QGraphicsTextItem(str(round(d2,2)))
                text1.setPos((d1 - x_min)/x * 490,520)
                text2.setPos(-60,490-abs(y_min-d2)/abs(y_min)*490)
                
            if MODE_X == 2 and MODE_Y == 1:
                
                d1 = x_min - k * x_min/5
                d2 = y_min + k*y/5
                text1 = QGraphicsTextItem(str(round(d1,2)))
                text2 = QGraphicsTextItem(str(round(d2,2)))
                text1.setPos(abs(x_min-d1)/abs(x_min)*490,520)
                text2.setPos(-60,490-(d2-y_min)/y*490)
                

            self.scene.addItem(text1)
            self.scene.addItem(text2)
            
            k = k+1
              
    def init_title(self,title):
        
        try:
            self.setWindowTitle(title)
        except TypeError:
            raise Error('wrong type for title')
        
    def init_labels(self,label_x,label_y):
        
        text_x = QGraphicsTextItem()
        
        try:
            if label_x == None:
                text_x.setPlainText('X-axis')
            else:
                text_x.setPlainText(label_x)
        except TypeError:
            raise Error('wrong type for x')
            
        text_x.setPos(220,560)
        text_x.setScale(1.3)

        text_y = QGraphicsTextItem()
        
        try:
            if label_y == None:
                text_y.setPlainText('Y-axis')
            else:
                text_y.setPlainText(label_y)
        except TypeError:
            raise Error('wrong type for y')
            
        text_y.setRotation(-90)
        text_y.setPos(-90,255)
        text_y.setScale(1.3)
        

        self.scene.addItem(text_x)
        self.scene.addItem(text_y)
        
    def set_legend(self):
        
        line1 = QGraphicsLineItem(20,-40,250,-40)
        line2 = QGraphicsLineItem(20,-40,20,-120)
        line3 = QGraphicsLineItem(20,-120,250,-120)
        line4 = QGraphicsLineItem(250,-40,250,-120)
        line1.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        line2.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        line3.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        line4.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        self.scene.addItem(line1)
        self.scene.addItem(line2)
        self.scene.addItem(line3)
        self.scene.addItem(line4)
        legend = QGraphicsTextItem('Legend')
        legend.setScale(1.3)
        legend.setPos(105,-115)
        self.scene.addItem(legend)
        line = QGraphicsTextItem('Line 1:')
        line.setScale(1.1)
        line.setPos(30,-80)
        self.scene.addItem(line)
        line_init = QGraphicsLineItem(100,-67,170,-67)
        line_init.setPen(QtGui.QPen(QtCore.Qt.blue, 2))
        self.scene.addItem(line_init)


