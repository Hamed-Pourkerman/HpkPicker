"""Qt picker UI shared by Autodesk Maya and 3ds Max.

The original viewer was host-specific at import time.  This copy keeps its
layout JSON format and editing behavior, while all DCC operations are routed
through :mod:`hpkpicker.hosts`.
"""

from PySide2.QtGui import QColor, QPen, QPolygon, QTransform
from PySide2 import QtWidgets, QtCore, QtGui
import json
import math
import os
from pathlib import Path

from .hosts import current_host

'''
import logging
#temp = filename= ((os.path.dirname(__file__))+'\\Picker.log'
logging.basicConfig(filename='Picker.log', 
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

logging.info('This is an info message')
logging.debug('This is a debug message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
'''




#ptr = OpenMayaUI.MQtUtil.mainWindow()
#MayaWindow = shiboken2.wrapInstance(int(ptr), QtWidgets.QMainWindow)
#print(__path__)
#print(os.path.dirname(__file__))


def maya_main_window():
    """Backward-compatible name used by the legacy UI code."""
    return current_host().main_window()


MayaWindow = None

__MODULE_PATH__ = str(Path(__file__).resolve().parents[1] / "resources")
__DEFAULT_IMAGE__ = os.path.join(__MODULE_PATH__, "Images", "Default_Image.png")
__DEBUG__ = False
#__MAIN_DIALOG_POS__= (1055, 300)


class CustomICO():
    '''
        A container class to manage the Icons per software
    '''
    SOFTWARE = {'Maya':1,
                '3dsmax':0,
                'houdini':0,
                'blender':0}
    
    @classmethod
    def __init__(self):
        if self.SOFTWARE['Maya'] == 1:
            self.fileNewICO = ':fileNew.png'
            self.fileOpenICO = ':fileOpen.png'
            self.fileSaveICO = ':fileSave.png'
            
            self.ScaleUpICO = ':UVTBAdd.png'
            self.ScaleDownICO = ':UVTBRemove.png'
            self.DeleteICO = ':deleteActive.png'
            self.DiamondICO = ':plane.png'

            self.PlusICO = ':addClip.png'
            self.InfoICO = ':info.png'
            
            
            self.TextButtonICO = __MODULE_PATH__ + '\\icons\\TextButton_lightgreen.png'
            if not self.iconExist(self.TextButtonICO): 
                self.TextButtonICO = ':text.png'
            

            self.CircleICO = __MODULE_PATH__ + '\\icons\\circle_lightgreen.png'
            if not self.iconExist(self.CircleICO): 
                self.CircleICO = ':circleSolid.png'

            self.RectICO = __MODULE_PATH__ + '\\icons\\Square_lightgreen.png'
            if not self.iconExist(self.RectICO): 
                self.RectICO = ':square.png'
            

            self.lightGreenICO = __MODULE_PATH__ + '\\icons\\Square_lightgreen.png'
            self.lightOrangeICO = __MODULE_PATH__ + '\\icons\\Square_lightorange.png'
            self.lightPinkICO = __MODULE_PATH__ + '\\icons\\Square_lightpink.png'
            self.lightRedICO = __MODULE_PATH__ + '\\icons\\Square_lightred.png'
            self.lightBlueICO = __MODULE_PATH__ + '\\icons\\Square_lightblue.png'
            self.darkBlueICO = __MODULE_PATH__ + '\\icons\\Square_darkblue.png'
            self.yellowICO = __MODULE_PATH__ + '\\icons\\Square_Yellow.png'
            self.purpleICO = __MODULE_PATH__ + '\\icons\\Square_Purple.png'
            
            self.RainbowICO = __MODULE_PATH__  + '\\icons\\rainbow.png'


    @classmethod
    def iconExist(self,filepath):
        if os.path.isfile(filepath):
            return True
        else:
            return False

class DccCommands:
    """Compatibility facade for the viewer's historical method names."""

    @staticmethod
    def MAYA_selectObjects(selected_items, prefix=""):
        return current_host().select_items(selected_items, prefix)

    @staticmethod
    def MAYA_update_item_object_list(item_dict):
        item_dict["object_list"] = current_host().capture_selection()

    @staticmethod
    def MAYA_EvalScript(script=""):
        return current_host().run_script(script)

    @staticmethod
    def Max_selectObjects(selected_items):
        return current_host().select_items(selected_items)

class Custom_Dialog(QtWidgets.QDialog): 
    """ 
        New Tab Custom Dialog Box
        A custom dialog to get a Tab name 
    """ 
    def __init__(self, parent= MayaWindow, multiLineEdit=False , LastText=''): 
        super(Custom_Dialog, self).__init__(parent) 
        self.title = "New Tab Dialog"
        self.labelText = "Tab Name: "
        self.multiLineEdit = multiLineEdit
        self.LastText = LastText

        self.label = QtWidgets.QLabel()
        self.setWindowTitle(self.title) 
        self.label.setText(self.labelText)

        self.setWindowFlags(self.windowFlags()) 
        self.create_widgets() 
        self.create_layout() 
        self.create_connections() 

    def create_widgets(self): 
        if self.multiLineEdit:
            scriptExample =  'from maya import cmds \n'
            scriptExample += 'print(cmds.ls(sl=1))'
            self.lineedit = QtWidgets.QTextEdit(scriptExample) 
            #self.lineedit.setAcceptRichText(True)
            #self.lineedit.setTextFormat(PlainText)
            if self.LastText != '':
                self.lineedit.setText(self.LastText)
            #self.lineedit = QtWidgets.QPlainTextEdit('from maya import cmds \n print(cmds.ls(sl=1))') 
        else:
            self.lineedit = QtWidgets.QLineEdit('Biped') 
        self.ok_btn = QtWidgets.QPushButton("OK") 
        self.cancel_btn = QtWidgets.QPushButton("Cancel") 

    def setTitle(self,title):
        self.setWindowTitle(title) 
    
    def setLabel(self,label):
        self.label.setText(label)

    def create_layout(self): 
        wdg_layout = QtWidgets.QHBoxLayout() 
        wdg_layout.addWidget(self.label) 
        wdg_layout.addWidget(self.lineedit) 
        btn_layout = QtWidgets.QHBoxLayout() 
        btn_layout.addStretch() 
        btn_layout.addWidget(self.ok_btn) 
        btn_layout.addWidget(self.cancel_btn) 
        main_layout = QtWidgets.QVBoxLayout(self) 
        main_layout.addLayout(wdg_layout) 
        main_layout.addLayout(btn_layout) 
    
    def create_connections(self): 
        self.ok_btn.clicked.connect(self.accept) 
        self.cancel_btn.clicked.connect(self.close) 
    
    def get_text(self): 
        if self.multiLineEdit == False:
            return(self.lineedit.text())
        else:
            return(self.lineedit.toPlainText())

    
    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Enter,QtCore.Qt.Key_Return):
            self.accept()

class EditableTabBar(QtWidgets.QTabBar):
    def __init__(self, parent):
        QtWidgets.QTabBar.__init__(self, parent)
        self._editor = QtWidgets.QLineEdit(self)
        self._editor.setWindowFlags(QtCore.Qt.Popup)
        self._editor.setFocusProxy(self)
        self._editor.editingFinished.connect(self.handleEditingFinished)
        self._editor.installEventFilter(self)
        self.setMovable(True)

    def eventFilter(self, widget, event):
        if ((event.type() == QtCore.QEvent.MouseButtonPress and not self._editor.geometry().contains(event.globalPos())) or (event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Escape)):
            self._editor.hide()
            return True
        return QtWidgets.QTabBar.eventFilter(self, widget, event)

    def mouseDoubleClickEvent(self, event):
        index = self.tabAt(event.pos())
        if index >= 0:
            self.editTab(index)

    def editTab(self, index):
        rect = self.tabRect(index)
        self._editor.setFixedSize(rect.size())
        self._editor.move(self.parent().mapToGlobal(rect.topLeft()))
        self._editor.setText(self.tabText(index))
        if not self._editor.isVisible():
            self._editor.show()

    def handleEditingFinished(self):
        index = self.currentIndex()
        if index >= 0:
            self._editor.hide()
            self.setTabText(index, self._editor.text())

class Custom_LineEdit (QtWidgets.QLineEdit):
    def __init__(self, parent):
        QtWidgets.QLineEdit.__init__(self, parent)
        
    def focusOutEvent(self,event): # QFocusEvent
        super(Custom_LineEdit,self).focusOutEvent(event)

        if self.hasAcceptableInput():
            #self.setFocus()
            self.setVisible(False)
        
# Custom SHAPES --- QGraphicsItems

class Custom_Ellipse(QtWidgets.QGraphicsEllipseItem):
    '''
        Custom Ellipse Item to add to the Viewer
    '''
    def __init__(self,*args):
        super().__init__(*args)
        self.Parent = None
        self.setAcceptHoverEvents(True)
        
        self._baseBrush = QtGui.QBrush(QtGui.QColor(0,230, 0,a=255))
        self._basePen = QtGui.QPen(QtGui.QColor(0, 230, 0,a=255))
        self._basePen.setCosmetic(True)
        self._basePen.setWidth(0)

        self.itemDict={
            'object_list': [],
            'type' : '',
            'bounding_rect':[],
            'pos':[],
            'color' :[],
            'scale' : 1,
            'script':'',
            'scriptEnabled':False,

            #Elipse and rectabgle specific values
            'rect':[],
        } # just the dictionary construction, haven't used it yet

    def update_Position_Rect_In_ItemDict(self):
        self.itemDict['rect'] = [self.x(),self.y(),self.rect().width(),self.rect().height()]
        self.itemDict['pos'] = [self.x(),self.y()]

    def mouseReleaseEvent(self, event):
        super(Custom_Ellipse, self).mouseReleaseEvent(event)

        self.update_Position_Rect_In_ItemDict()

        # Script Handelind and evaluation
        if self.itemDict['script'] !='' or self.itemDict['script'] != None:
            try:
                DccCommands.MAYA_EvalScript(self.itemDict['script'])
            except Exception as e:
                print('The Script has an Error : ',e)
        
        if __DEBUG__:
            print(json.dumps(self.itemDict,indent=4)) #sort_keys=True
        #print(self.itemDict['script']) #sort_keys=True
  
    def hoverEnterEvent(self, event):
        # Do your stuff here.
        self._baseBrush = self.brush()
        self._basePen = self.pen()
        
        R = abs(self.brush().color().red()-50.0)
        G = abs(self.brush().color().green()-50.0)
        B = abs(self.brush().color().blue()-50.0)
        A = abs(self.brush().color().alpha())
        hoverBrushColor = QtGui.QColor(R, G, B, a=A)
        hoverBrush = QtGui.QBrush(hoverBrushColor)
        
        hoverPen = QtGui.QPen(QtGui.QColor(200, 200, 200,a=200))
        hoverPen.setCosmetic(True)
        hoverPen.setWidth(3)
        self.setPen(hoverPen)
        self.setBrush(hoverBrush)
    
    def hoverLeaveEvent(self, event):
        self.setPen(self._basePen)
        self.setBrush(self._baseBrush)

class Custom_Rect(QtWidgets.QGraphicsRectItem):
    '''
        Custom Rectangle Item to add to the Viewer
    '''
    def __init__(self,*args):
        super().__init__(*args)
        self.Parent = None
        self.setAcceptHoverEvents(True)
        self._baseBrush = QtGui.QBrush(QtGui.QColor(0,230, 0,a=255))
        self._basePen = QtGui.QPen(QtGui.QColor(0,230, 0,a=255))
        self._basePen.setCosmetic(True)
        self._basePen.setWidth(0)
        
        self.setPen(self._basePen)
        self.setBrush(self._baseBrush)
        
        self.itemDict={
            'object_list': [],
            'type' : '',
            'bounding_rect':[],
            'pos':[],
            'color' : [],
            'scale' : 1,
            'script':'',
            'scriptEnabled':False,

            #rect specific values            
            'rect':[],
        } # just the dictionary construction, haven't used it yet

    def update_Position_Rect_In_ItemDict(self):
        self.itemDict['rect'] = [self.x(),self.y(),self.rect().width(),self.rect().height()]
        self.itemDict['pos'] = [self.x(),self.y()]

    def mouseReleaseEvent(self, event):
        super(Custom_Rect, self).mouseReleaseEvent(event)

        self.update_Position_Rect_In_ItemDict()

        # Script Handelind and evaluation
        if self.itemDict['script'] !='':
            try:
                DccCommands.MAYA_EvalScript(self.itemDict['script'])
            except Exception as e:
                print('The Script has an Error : ',e)
        
        if __DEBUG__:
            print(json.dumps(self.itemDict,indent=4)) #sort_keys=True
    
    def hoverEnterEvent(self, event):
        # Do your stuff here.
        self._baseBrush = self.brush()
        self._basePen = self.pen()
        
        R = abs(self.brush().color().red()-50.0)
        G = abs(self.brush().color().green()-50.0)
        B = abs(self.brush().color().blue()-50.0)
        A = abs(self.brush().color().alpha())
        hoverBrushColor = QtGui.QColor(R, G, B, a=A)
        hoverBrush = QtGui.QBrush(hoverBrushColor)
        
        hoverPen = QtGui.QPen(QtGui.QColor(200, 200, 200,a=200))
        hoverPen.setCosmetic(True)
        hoverPen.setWidth(3)
        self.setPen(hoverPen)
        self.setBrush(hoverBrush)
    
    def hoverLeaveEvent(self, event):
        self.setPen(self._basePen)
        self.setBrush(self._baseBrush)

    """
    #Attempt to Draw Rounded Rectangle #01 - Woking / 
    # ISSUE 1 : removing the select dotted recangle
    # ISSUE 2 : Trail / slow redraw problem
    def paint(self,painter,option,widget):
        super(Custom_Rect, self).paint(painter,option,widget)
        #painter = QtGui.QPainter()
        #option = QtWidgets.QStyleOptionGraphicsItem()
        #size = QtCore.Qt.AbsoluteSize
        '''
        painter.setPen(self._basePen)
        painter.setBrush(self._baseBrush)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        #painter.drawRect(option.rect)
        #painter.drawRect(self.boundingRect())
        
        painter.drawRoundedRect(self.boundingRect().x()-1,
                                self.boundingRect().y()-1,
                                self.boundingRect().width()+2,
                                self.boundingRect().height()+2,
                                5.0,5.0,QtCore.Qt.AbsoluteSize)
        '''
        #Bring the parent class paint back
        
        #return QtGui.QPainter(painter,option,widget)
        #return QtWidgets.QGraphicsTextItem.paint(painter, option, widget)
    """
    
    """
    #Attempt to Draw Rounded Rectangle #02
    # ISSUE 1 : removing the select dotted recangle
    def paint(self, painter, option, widget):
        #super(Custom_Rect, self).paint(painter, option, widget)
        self.setBrush(self._baseBrush)
        self.setPen(self._basePen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        path = QtGui.QPainterPath()
        path.addRoundedRect(self.boundingRect(), 5, 5)
        painter.setPen(self._basePen)
        painter.fillPath(path,self._baseBrush)
        painter.drawPath(path)

        #painter.drawRoundedRect(-10, -10, 20, 20, 5, 5)
        #painter = QtGui.QPainter()
        #painter.drawRoundedRect()
        #painter.drawRoundRect(-10, -10, 20, 20, 5, 5)
    """

class Custom_Polygon(QtWidgets.QGraphicsPolygonItem):
    '''
        Custom Polygon Item to add to the Viewer
    '''
    def __init__(self,*args):
        super().__init__(*args)
        self.Parent = None
        self.setAcceptHoverEvents(True)
        
        self._baseBrush = QtGui.QBrush(QtGui.QColor(0,230, 0,a=255))
        self._basePen = QtGui.QPen(QtGui.QColor(0, 230, 0,a=255))
        self._basePen.setCosmetic(True)
        self._basePen.setWidth(0)

        self.itemDict={
            'object_list': [],
            'type' : '',
            'bounding_rect':[],
            'pos':[],
            'color' : [],
            'scale' : 1,
            'script':'',
            'scriptEnabled':False,
            
            #Polygon Specific values
            'args' :[], 
        } # just the dictionary construction, haven't used it yet

    def update_Position_Rect_In_ItemDict(self):
        self.itemDict['rect'] = [self.x(),self.y(),self.boundingRect().width(),self.boundingRect().height()]
        self.itemDict['pos'] = [self.x(),self.y()]

    def mouseReleaseEvent(self, event):
        super(Custom_Polygon, self).mouseReleaseEvent(event)

        self.update_Position_Rect_In_ItemDict()

        # Script Handelind and evaluation
        if self.itemDict['script'] !='':
            try:
                DccCommands.MAYA_EvalScript(self.itemDict['script'])
            except Exception as e:
                print('The Script has an Error : ',e)

        if __DEBUG__:
            print(json.dumps(self.itemDict,indent=4)) #sort_keys=True

    def hoverEnterEvent(self, event):
        # Do your stuff here.
        self._baseBrush = self.brush()
        self._basePen = self.pen()
        
        R = abs(self.brush().color().red()-50.0)
        G = abs(self.brush().color().green()-50.0)
        B = abs(self.brush().color().blue()-50.0)
        A = abs(self.brush().color().alpha())
        hoverBrushColor = QtGui.QColor(R, G, B, a=A)
        hoverBrush = QtGui.QBrush(hoverBrushColor)
        
        hoverPen = QtGui.QPen(QtGui.QColor(200, 200, 200,a=200))
        hoverPen.setCosmetic(True)
        hoverPen.setWidth(3)
        self.setPen(hoverPen)
        self.setBrush(hoverBrush)
    
    def hoverLeaveEvent(self, event):
        self.setPen(self._basePen)
        self.setBrush(self._baseBrush)

class Custom_TextButton(QtWidgets.QGraphicsTextItem):
    
    def __init__(self, text,parent=None):
        super(Custom_TextButton, self).__init__(text,parent)
        
        self.Parent = None
        
        self.setAcceptHoverEvents(True)

        self.Text = text

        #set Background text Color
        self._baseBrush = QtGui.QBrush(QtGui.QColor(0, 100, 0, 255))
        self._basePen = QtGui.QPen(QtGui.QColor(0, 100, 0,a=255))
        self._basePen.setCosmetic(True)
        
        self._tempBrush = QtGui.QBrush(QtGui.QColor(0, 100, 0, 255))
        self._tempPen = QtGui.QPen(QtGui.QColor(0, 100, 0,a=255))
        self._tempPen.setCosmetic(True)

        self._basePen.setWidth(0)
        
        #Set text Color:
        self._baseTextColor = QtGui.QColor(255,255,255)
        self.setDefaultTextColor(self._baseTextColor)
        self.font = QtGui.QFont('Calibri', 12, QtGui.QFont.Bold)
        self.setFont(self.font)
        self.setPos(0,0)

        #self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)

        #self.font = QtGui.QBrush(QtGui.QColor(0,230, 0,a=255))
        #self._basePen = QtGui.QPen(QtGui.QColor(20, 20, 20,a=255))
        self.itemDict={
            'object_list': [],
            'type' : '',
            'bounding_rect':[], 
            'pos':[],           
            'color' : [],
            'scale' : 1,
            'script':'',

            #Text Specific values            
            'text' : '',
            'textcolor' : [],
        } # just the dictionary construction, haven't used it yet

        self.update()

    def update_Position_Rect_In_ItemDict(self):
        self.itemDict['rect'] = [self.x(),
                                self.y(),
                                self.boundingRect().width(),
                                self.boundingRect().height()]
        
        self.itemDict['pos'] = [self.x(),self.y()]


    def mouseReleaseEvent(self, event):
        super(Custom_TextButton, self).mouseReleaseEvent(event)

        self.update_Position_Rect_In_ItemDict()
        
        # Script Handelind and evaluation
        if self.itemDict['script'] !='':
            try:
                DccCommands.MAYA_EvalScript(self.itemDict['script'])
            except Exception as e:
                print('The Script has an Error : ',e)
        
        if __DEBUG__:
            print(json.dumps(self.itemDict,indent=4)) #sort_keys=True
        #print(self.itemDict['script']) #sort_keys=True
        
     # contextMenuEvent --------------------Begin-------------------------------
    
    def hoverEnterEvent(self, event):
        # Do your stuff here.
        self.tempBrush = self.brush()
        self.tempPen = self.pen()
        
        R = abs(self.brush().color().red()-50.0)
        G = abs(self.brush().color().green()-50.0)
        B = abs(self.brush().color().blue()-50.0)
        A = abs(self.brush().color().alpha())
        hoverBrushColor = QtGui.QColor(R, G, B, a=A)
        hoverBrush = QtGui.QBrush(hoverBrushColor)
        
        hoverPen = QtGui.QPen(QtGui.QColor(200, 200, 200,a=200))
        hoverPen.setWidth(3)
        hoverPen.setCosmetic(True)

        self.setPen(hoverPen)
        self.setBrush(hoverBrush)
    
    def hoverLeaveEvent(self, event):
        self.setPen(self.tempPen)
        self.setBrush(self.tempBrush)    
   
    def mouseDoubleClickEvent(self,event):
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)

    def focusOutEvent(self,event):
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.itemDict['text'] = self.toPlainText()
        #print(self.toPlainText())
        super(Custom_TextButton,self).focusOutEvent(event)
        
        self.update()
        self.Parent.update()


    def brush(self):
        return self._baseBrush
    
    def pen(self):
        return self._basePen

    def setBrush(self,QBrush):
        self._baseBrush = QBrush
        self.update()

    def setPen(self,QPen):
        self._basePen = QPen
        self.update()

    def paint(self,painter,option,widget):
        
        #painter = QtGui.QPainter()
        #option = QtWidgets.QStyleOptionGraphicsItem()
        #size = QtCore.Qt.AbsoluteSize

        painter.setPen(self._basePen)
        painter.setBrush(self._baseBrush)
        
        #painter.drawRect(option.rect)
        #painter.drawRect(self.boundingRect())
        painter.drawRoundedRect(self.boundingRect(),5.0,5.0,QtCore.Qt.AbsoluteSize)
        
        #Bring the Text On top of the Rect
        super(Custom_TextButton, self).paint(painter,option,widget)
        #return QtWidgets.QGraphicsTextItem.paint(painter, option, widget)

class Custom_DrawPolygon(QtWidgets.QGraphicsPolygonItem):
    '''
        Custom Draw Polygon Item 
    '''
    def __init__(self,*args):
        super().__init__(*args)
        self.Parent = None
        self.setAcceptHoverEvents(True)
        
        self._baseBrush = QtGui.QBrush(QtGui.QColor(128,0, 0,a=128))
        self._basePen = QtGui.QPen(QtGui.QColor(128, 0, 0,a=128))
        self._basePen.setCosmetic(True)
        self._basePen.setWidth(0)

        self.itemDict={
            'object_list': [],
            'type' : '',
            'bounding_rect':[],
            'pos':[],
            'color' : [],
            'scale' : 1,
            'script':'',
            'scriptEnabled':False,
            
            #Polygon Specific values
            'args' :[],
            'polygonPointsInOrder' : []
        } # just the dictionary construction, haven't used it yet

    def update_Position_Rect_In_ItemDict(self):
        self.itemDict['rect'] = [self.x(),self.y(),self.boundingRect().width(),self.boundingRect().height()]
        self.itemDict['pos'] = [self.x(),self.y()]

    def mouseReleaseEvent(self, event):
        super(Custom_DrawPolygon, self).mouseReleaseEvent(event)

        self.update_Position_Rect_In_ItemDict()

        # Script Handelind and evaluation
        if self.itemDict['script'] !='':
            try:
                DccCommands.MAYA_EvalScript(self.itemDict['script'])
            except Exception as e:
                print('The Script has an Error : ',e)
        
        if __DEBUG__:
            print(json.dumps(self.itemDict,indent=4)) #sort_keys=True

    def hoverEnterEvent(self, event):
        # Do your stuff here.
        self._baseBrush = self.brush()
        self._basePen = self.pen()
        
        R = abs(self.brush().color().red()-50.0)
        G = abs(self.brush().color().green()-50.0)
        B = abs(self.brush().color().blue()-50.0)
        A = abs(self.brush().color().alpha())
        hoverBrushColor = QtGui.QColor(R, G, B, a=A)
        hoverBrush = QtGui.QBrush(hoverBrushColor)
        
        hoverPen = QtGui.QPen(QtGui.QColor(200, 200, 200,a=200))
        hoverPen.setCosmetic(True)
        hoverPen.setWidth(3)
        self.setPen(hoverPen)
        self.setBrush(hoverBrush)
    
    def hoverLeaveEvent(self, event):
        self.setPen(self._basePen)
        self.setBrush(self._baseBrush)


# Custom SHAPES --- END

#NEW  Viewer Class----------------------------Begin
class Custom_GraphicViewer(QtWidgets.QGraphicsView): # NEW 
    
    def __init__(self, parent=None):
        super(Custom_GraphicViewer, self).__init__(parent)
        self.__LOCK_MODE__ = True
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self._isPanning = False
        self._mousePressed = False

        # Draw Polygon Buffer Variables -- Begin
        self._Create_Polygon_Tool_MODE = False
        self._Key_Return_Pressed = False
        self._vertex_EllipseItems = []
        self._vertex_PositionsList = []
        self.tempPoly = QtGui.QPolygonF()
        self.tempPolyItem = None

        # Draw Polygon Buffer Variables -- End

        self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        self.setHorizontalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOff )
        self.setVerticalScrollBarPolicy( QtCore.Qt.ScrollBarAlwaysOff )

        self._scene = MyGraphicsScene(self,self)
        self.setScene(self._scene)
        self.scene().selectionChanged.connect(self.selection_changed)
        self._current_selection = []

        #Antialiasing
        self.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.BoundingRectViewportUpdate)

        self._empty = True        
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self._zoom = 0
        self.ZoomOption1 = True
        self.ZoomOption2 = False

        self.chrPrefix = ''


        #self.setScene(self._scene)

    def select_items(self, items, on):
        #pen = QtGui.QPen(QColor(255, 255, 255) if on else QColor(255, 128, 0),
        #           0.5, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        for item in items:
            if on: # If item is Selected
                pen = QtGui.QPen(QColor(255, 255, 255,a=255),0.5, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
                pen.setWidth(3)
                pen.setCosmetic(True)
            else:
                #pen = QtGui.QPen(QColor(0, 0, 0),0.5, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
                
                if item.itemDict['type'] == 'TextButton':
                    pen = QtGui.QPen(item.brush().color())
                    pen.setWidth(0)
                    pen.setCosmetic(True)
                else:
                    pen = QtGui.QPen(item.brush().color())
                    pen.setWidth(0)
                    pen.setCosmetic(True)

                #pen.setWidth(0)


            item.setPen(pen)

    def selection_changed(self):
        try:
            self.select_items(self._current_selection, False)
            self._current_selection = self.scene().selectedItems()
            self.select_items(self._current_selection, True)
        except RuntimeError:
            pass

    def mousePressEvent(self,  event):

        if event.button() == QtCore.Qt.LeftButton:
            # Panning and Set cursor
            self._mousePressed = True
            if self._isPanning:
                self.setCursor(QtCore.Qt.ClosedHandCursor)
                self._dragPos = event.pos()
                event.accept()
            else:
                super(Custom_GraphicViewer, self).mousePressEvent(event)
            

        elif event.button() == QtCore.Qt.MiddleButton:
            self._mousePressed = True
            self._isPanning = True
            self.setCursor(QtCore.Qt.ClosedHandCursor)
            self._dragPos = event.pos()
            event.accept()        


    def mouseMoveEvent(self, event):
        #Force Repapint to fix the text Button move trail Issue
        self.viewport().repaint()
        #print(f'screenPos =    x:{event.screenPos().x()}   y:{event.screenPos().y()}')
        #print(f'pos =    x:{event.pos().x()}   y:{event.pos().y()}')
        #print(f'Globalpos =    x:{event.globalPos().x()}   y:{event.globalPos().y()}')
        if self._mousePressed and self._isPanning:
            newPos = event.pos()
            diff = newPos - self._dragPos
            self._dragPos = newPos
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - diff.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - diff.y())
            event.accept()
        else:
            super(Custom_GraphicViewer, self).mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:

            #Create Draw polygon tool -----------------------------------------BEGIN
            if self._Create_Polygon_Tool_MODE:
                x = self._scene.mouseScenePosX #event.pos().x()# 
                y = self._scene.mouseScenePosY #event.pos().y()# 
                
                if __DEBUG__:
                    print(f'Create a vertex at ({x},{y})')
                vItem = self._scene.addEllipse(x-1.5,y-1.5,3,3)
                vItem.setBrush(QtGui.QBrush(QtGui.QColor(255,0,0,255)))
                vItem.setPen(QtGui.QPen(vItem.brush().color()))
                self._vertex_EllipseItems.append(vItem)
                self._vertex_PositionsList.append([x,y])
            
                self.tempPoly.append(QtCore.QPointF(x,y))
            
            
            # preview polygon 
            #delete the last preview draw
            if self.tempPolyItem :
                self._scene.removeItem(self.tempPolyItem)
            
            #print(self.tempPoly)
            # Create a new preview polygon
            if len(self._vertex_PositionsList)>2:
                self.tempPolyItem = self._scene.addPolygon(self.tempPoly, 
                QPen(QColor(255,128,0), 0.5, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin), 
                QtGui.QBrush(QColor(255,0,0,128)))
            #Create Draw polygon tool ----------------------------------------- END
            
            
            if self._isPanning:
                self.setCursor(QtCore.Qt.OpenHandCursor)
            else:
                self._isPanning = False
                self.setCursor(QtCore.Qt.ArrowCursor)
                
                try:
                    #print('selectedItems counts: ',len(self._scene.selectedItems()))
                    DccCommands.MAYA_selectObjects(self._scene.selectedItems(),self.chrPrefix)
                except:pass
                
                # UPDATE Every Item's Position and rect Dictionary
                for item in self._scene.selectedItems():
                    if item.itemDict:
                        try: 
                            item.update_Position_Rect_In_ItemDict()
                        except:pass
                
            self._mousePressed = False
        elif event.button() == QtCore.Qt.MiddleButton:
            self._isPanning = False
            self.setCursor(QtCore.Qt.ArrowCursor)
            self._mousePressed = False

        super(Custom_GraphicViewer, self).mouseReleaseEvent(event)

    
    def mouseDoubleClickEvent(self, event):
        #self.fitInView(self.sceneRect(), QtCore.Qt.KeepAspectRatio)
        if event.button() == QtCore.Qt.MiddleButton:
            self.fitInView()

        super(Custom_GraphicViewer, self).mouseDoubleClickEvent(event)

    def scaleDown_SelectedItems(self):
            #print('Key_BracketLeft pressed')
            for item in self._scene.selectedItems():
                if item.itemDict:
                    if item.scale() > 0.1:
                        if self.get_key_modifiers() == ['control']:
                            #increaseScale = item.scale() - 0.5
                            #print(item.rect())
                            if item.itemDict['type'] == 'TextButton' or \
                                item.itemDict['type'] == 'Polygon' or \
                                item.itemDict['type'] == 'DrawPolygon':

                                increaseScale = item.scale() - 0.1
                                item.setScale(increaseScale)
                                item.itemDict['scale'] = increaseScale
                            else:
                                item.setScale(1)
                                if item.rect().width() > 5:
                                    NewRect = QtCore.QRectF(item.rect().x(),
                                                            item.rect().y(),
                                                            item.rect().width() - 2.5,
                                                            item.rect().height())
                                    item.setRect(NewRect)
                                    item.update_Position_Rect_In_ItemDict()

                        elif self.get_key_modifiers() == ['alt']:    
                            #increaseScale = item.scale() - 0.1
                            if item.itemDict['type'] == 'TextButton' or \
                                item.itemDict['type'] == 'Polygon' or \
                                item.itemDict['type'] == 'DrawPolygon':

                                increaseScale = item.scale() - 0.1
                                item.setScale(increaseScale)
                                item.itemDict['scale'] = increaseScale
                                
                            else:
                                item.setScale(1)
                                if item.rect().height() > 5:
                                    NewRect = QtCore.QRectF(item.rect().x(),
                                                            item.rect().y(),
                                                            item.rect().width() ,
                                                            item.rect().height() -2.5)
                                    item.setRect(NewRect)
                                    item.update_Position_Rect_In_ItemDict()
                        else:     
                            #increaseScale = item.scale() - 0.1
                            if item.itemDict['type'] == 'TextButton' or \
                                item.itemDict['type'] == 'Polygon' or \
                                item.itemDict['type'] == 'DrawPolygon':

                                increaseScale = item.scale() - 0.1
                                item.setScale(increaseScale)
                                item.itemDict['scale'] = increaseScale
                            else:
                                item.setScale(1)
                                if item.rect().width() > 5 and item.rect().height() > 5:
                                    NewRect = QtCore.QRectF(item.rect().x(),
                                                            item.rect().y(),
                                                            item.rect().width() -2.5 ,
                                                            item.rect().height() -2.5)
                                    item.setRect(NewRect)
                                    item.update_Position_Rect_In_ItemDict()

                        #item.setScale(increaseScale)
                        #item.itemDict['scale'] = increaseScale        
    
    def scaleUp_SelectedItems(self):
        '''
        ellipse = Custom_Ellipse()
        rectangle = Custom_Rect()
        Polygon = Custom_Polygon()
        TextButton = Custom_TextButton()
        '''
        for item in self._scene.selectedItems():
            if item.itemDict:
                if self.get_key_modifiers() == ['control']:
                    #increaseScale = item.scale() + 0.5
                    #QtCore.QRectF.x() ; #QtCore.QRectF.y();  #QtCore.QRectF.width(); #QtCore.QRectF.height()
                    #print(item.rect())
                    if item.itemDict['type'] == 'TextButton' or \
                        item.itemDict['type'] == 'Polygon' or \
                        item.itemDict['type'] == 'DrawPolygon':

                        increaseScale = item.scale() + 0.1
                        item.setScale(increaseScale)
                        item.itemDict['scale'] = increaseScale
                    else:
                        item.setScale(1)
                        NewRect = QtCore.QRectF(item.rect().x(),
                                                item.rect().y(),
                                                item.rect().width() + 2.5,
                                                item.rect().height())
                        item.setRect(NewRect)
                        #Update Dict
                        item.update_Position_Rect_In_ItemDict()
                
                elif self.get_key_modifiers() == ['alt']:    
                    #print(item.rect())
                    if item.itemDict['type'] == 'TextButton' or \
                        item.itemDict['type'] == 'Polygon' or \
                        item.itemDict['type'] == 'DrawPolygon':

                        increaseScale = item.scale() + 0.1
                        item.setScale(increaseScale)
                        item.itemDict['scale'] = increaseScale
                    else:
                        item.setScale(1)
                        NewRect = QtCore.QRectF(item.rect().x(),
                                                item.rect().y(),
                                                item.rect().width(),
                                                item.rect().height() + 2.5)
                        item.setRect(NewRect) 
                        item.update_Position_Rect_In_ItemDict()                      
                else:     
                    #increaseScale = item.scale() - 0.1
                    if item.itemDict['type'] == 'TextButton' or \
                        item.itemDict['type'] == 'Polygon' or \
                        item.itemDict['type'] == 'DrawPolygon':

                        increaseScale = item.scale() + 0.1
                        item.setScale(increaseScale)
                        item.itemDict['scale'] = increaseScale
                    else:
                        item.setScale(1)
                        NewRect = QtCore.QRectF(item.rect().x(),
                                                item.rect().y(),
                                                item.rect().width() + 2.5 ,
                                                item.rect().height() + 2.5 )
                        item.setRect(NewRect) 
                        item.update_Position_Rect_In_ItemDict()                             
                #item.setScale(increaseScale)
                #item.itemDict['scale'] = increaseScale

    def moveUp_SelectedItems(self):
        for item in self._scene.selectedItems():
            if self.get_key_modifiers() == ['control']:
                x = item.pos().x()
                y = item.pos().y() - 10
            else:
                x = item.pos().x()
                y = item.pos().y() - 1
            item.setPos(x,y)
            item.itemDict['pos'] = [x,y]

    def moveDown_SelectedItems(self):
        for item in self._scene.selectedItems():
            if self.get_key_modifiers() == ['control']:
                x = item.pos().x()
                y = item.pos().y() + 10
            else:
                x = item.pos().x()
                y = item.pos().y() + 1
            item.setPos(x,y)   
            item.itemDict['pos'] = [x,y]

    def moveLeft_SelectedItems(self):
        for item in self._scene.selectedItems():
            if self.get_key_modifiers() == ['control']:
                x = item.pos().x() - 10
                y = item.pos().y()
            else:
                x = item.pos().x() - 1
                y = item.pos().y() 
            item.setPos(x,y) 
            item.itemDict['pos'] = [x,y]

    def moveRight_SelectedItems(self):
        for item in self._scene.selectedItems():
            if self.get_key_modifiers() == ['control']:
                x = item.pos().x() + 10
                y = item.pos().y() 
            else:
                x = item.pos().x() + 1
                y = item.pos().y()
            item.setPos(x,y)
            item.itemDict['pos'] = [x,y]

    def keyPressEvent(self, event):
        #Create polygon tool -----------------------------------------BEGIN
        if event.key() == (QtCore.Qt.Key_Return):
            self._Key_Return_Pressed = True
            
            if self._Create_Polygon_Tool_MODE:
                print('Draw Polygon Ended')
            
            if self.tempPolyItem :
                self._scene.removeItem(self.tempPolyItem)

            self.endDrawPolygon()

            #Create polygon tool -----------------------------------------END

        #Zoom Extense all
        if event.key() == (QtCore.Qt.Key_F):
            self.fitInView()

        #SCALE UP ---------------------
        if event.key() == (QtCore.Qt.Key_Equal):
            if not self.__LOCK_MODE__:
                self.scaleUp_SelectedItems()
            else:
                print("Can't Scale UP \t  [ LOCK MODE IS ON ]")
        #SCALE DOWN ---------------------
        if event.key() == (QtCore.Qt.Key_Minus):
            if not self.__LOCK_MODE__:
                self.scaleDown_SelectedItems()
            else:
                print("Can't Scale Down \t  [ LOCK MODE IS ON ]")                

        # Move items Up Down Left Right
        if event.key() == (QtCore.Qt.Key_W):
            if not self.__LOCK_MODE__:
                self.moveUp_SelectedItems()
            else:
                print("Can't Move UP \t  [ LOCK MODE IS ON ]")                
        
        if event.key() == (QtCore.Qt.Key_S):
            if not self.__LOCK_MODE__:
                self.moveDown_SelectedItems()
            else:
                print("Can't Move DOWN \t  [ LOCK MODE IS ON ]")                                
        
        if event.key() == (QtCore.Qt.Key_A):
            if not self.__LOCK_MODE__:
                self.moveLeft_SelectedItems()                    
            else:
                print("Can't Move LEFT \t  [ LOCK MODE IS ON ]")                                

        if event.key() == (QtCore.Qt.Key_D):
            if not self.__LOCK_MODE__:
                self.moveRight_SelectedItems()                  
            else:
                print("Can't Move RIGHT \t  [ LOCK MODE IS ON ]")                                

        if event.key() == (QtCore.Qt.Key_Delete):
            if not self.__LOCK_MODE__:
                self.deleteSelectedItems()
            else:
                print("Can't Delete Item \t  [ LOCK MODE IS ON ]")                                

        if event.key() == QtCore.Qt.Key_Space and not self._mousePressed:
            self._isPanning = True
            self.setCursor(QtCore.Qt.OpenHandCursor)
        else:
            super(Custom_GraphicViewer, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == (QtCore.Qt.Key_Return):
            self._Key_Return_Pressed = False

        if event.key() == QtCore.Qt.Key_Space:
            if not self._mousePressed:
                self._isPanning = False
                self.setCursor(QtCore.Qt.ArrowCursor)
        else:
            super(Custom_GraphicViewer, self).keyPressEvent(event)

    def wheelEvent(self,  event):
       
        if self.ZoomOption1:
            # zoom factor
            factor = 1.25
            # Set Anchors
            self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
            self.setResizeAnchor(QtWidgets.QGraphicsView.NoAnchor)

            # Save the scene pos
            oldPos = self.mapToScene(event.pos())

            # Zoom
            if event.delta() < 0:
                factor = 1.0 / factor
            self.scale(factor, factor)

            # Get the new position
            newPos = self.mapToScene(event.pos())

            # Move scene to old position
            delta = newPos - oldPos
            self.translate(delta.x(), delta.y())


        elif self.ZoomOption2:

            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 0.5
            else:
                factor = 0.8
                self._zoom -= 0.5
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    #---------------------------------------------------------------------
    # -------------- Combine Methods -------------------------------------
    #---------------------------------------------------------------------
    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                                viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0
    
    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            #self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            #self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()
        
    #Add Shapes to Viewer methods
    def addEllipse( self,x=10,y=10,w=30,h=30,
                    item_color=QtGui.QColor(0,230, 0,a=255),
                    pos = None,
                    scale = 1,
                    ):

        brush = QtGui.QBrush(item_color)
        #pen = QtGui.QPen(QtGui.QColor(0, 0, 0,a=255))
        pen = QtGui.QPen(item_color)
        pen.setCosmetic(True)
        pen.setWidth (0)
        
        #x = 10;y=10;w=200;h=200
        item = Custom_Ellipse(x, y, w, h)
        if pos:
            item.setPos(pos[0],pos[1])
        item.setScale(scale)
        item.Parent = self #Set Parent

        #item.setAcceptHoverEvents(True)

        item._baseBrush = brush
        item._basePen = pen
        
        item.setPen(pen)
        item.setBrush(brush)
        
        item_type = 'ellipse'
        #IdString = "{:04d}".format(item_ID)
        #item_name = f'{item_type}_{item_ID}'
       
        item_object_list = cmds.ls(sl=1)
        item_rect = [x, y, w, h]
        item_color_liststr =[item_color.red(), item_color.green(), item_color.blue(), item_color.alpha()]
        item_boundingRect =[item.boundingRect().x(), item.boundingRect().y(), item.boundingRect().width(), item.boundingRect().height()]

        item.itemDict={
            'object_list': item_object_list,
            'type' : item_type,
            'bounding_rect':item_boundingRect,
            'pos':[item.pos().x(),item.pos().y()],
            'color' : item_color_liststr,
            'scale' : scale,
            'script':'',
            'scriptEnabled':False,

            #Elipse and rectabgle specific values
            'rect':item_rect,
        }
        #print(self.__LOCK_MODE__)
        if self.__LOCK_MODE__ == True:
            item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,False)
        elif self.__LOCK_MODE__ == False:            
            item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,True)
        item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

        self._scene.addItem(item)
        
        return item

    def addRect( self,x=10,y=10,w=30,h=30,
                    item_color=QtGui.QColor(0,230, 0,a=255),
                    pos = None,
                    scale = 1,
                    ):

        brush = QtGui.QBrush(item_color)
        pen = QtGui.QPen(item_color)
        pen.setCosmetic(True)
        pen.setWidth (0)
        
        #x = 10;y=10;w=200;h=200
        item = Custom_Rect(x, y, w, h)
        if pos:
            item.setPos(pos[0],pos[1])
        item.setScale(scale)             
        item.Parent = self #Set Parent

        #item.setAcceptHoverEvents(True)

        item._baseBrush = brush
        item._basePen = pen

        item.setPen(pen)
        item.setBrush(brush)
        
       
        item_type = 'rectangle'
        #IdString = "{:04d}".format(item_ID)
        #item_name = f'{item_type}_{item_ID}'
       
        item_object_list = cmds.ls(sl=1)
        item_rect=[x, y, w, h]
        item_color_liststr =[item_color.red(), item_color.green(), item_color.blue(), item_color.alpha()]
        item_boundingRect =[item.boundingRect().x(), item.boundingRect().y(), item.boundingRect().width(), item.boundingRect().height()]
        
        item.itemDict= {
            'object_list': item_object_list,
            'type' : item_type,
            'bounding_rect':item_boundingRect,
            'pos':[item.pos().x(),item.pos().y()],
            'color' : item_color_liststr,
            'scale' : scale,
            'script':'',
            'scriptEnabled':False,

            #rect specific values            
            'rect':item_rect,
        }
        #print(self.__LOCK_MODE__)
        if self.__LOCK_MODE__ == True:
            item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,False)
        elif self.__LOCK_MODE__ == False:            
            item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,True)
        item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        
        self._scene.addItem(item)
        
        return item


    def createCircularPolygonF(self, n, r, s):      
        Qpolygon = QtGui.QPolygonF() 
        w = 360/n                                                       # angle per step
        for i in range(n):                                              # add the points of polygon
            t = w*i + s
            x = r*math.cos(math.radians(t))
            y = r*math.sin(math.radians(t))
            Qpolygon.append(QtCore.QPointF(self.width()/2 + x, self.height()/2 + y))        
        return(Qpolygon)

    def addPolygon_Diamond_Shape( self,n=4,r=20,s=4,
                    item_color=QtGui.QColor(0,230, 0,a=255),
                    pos = None,
                    scale = 1
                    ):

        brush = QtGui.QBrush(item_color)
        pen = QtGui.QPen(item_color)
        pen.setCosmetic(True)
        pen.setWidth (0)
        
        polygonF = self.createCircularPolygonF(n,r,s)
        item = Custom_Polygon(QtGui.QPolygonF(polygonF))
        
        item.setScale(scale)
        if pos:
            item.setPos(pos[0],pos[1])
        item.Parent = self #Set Parent
        
        #item.setAcceptHoverEvents(True)
        item._baseBrush = brush
        item._basePen = pen

        item.setPen(pen)
        item.setBrush(brush)
        
        item_type = 'Polygon'
        #IdString = "{:04d}".format(item_ID)
        #item_name = f'{item_type}_{item_ID}'
       
        item_object_list = cmds.ls(sl=1)
        item_args=[n, r, s]
        
        x = item.boundingRect().x()
        y = item.boundingRect().y()
        w = item.boundingRect().width()
        h = item.boundingRect().height()
        item_bounding_rect=[x, y, w, h]
        item_color_liststr =[item_color.red(), item_color.green(), item_color.blue(), item_color.alpha()]
        #item_border = 2
        
        item.itemDict={
            'object_list': item_object_list,
            'type' : item_type,
            'bounding_rect':item_bounding_rect,
            'pos':[item.pos().x(),item.pos().y()],
            'color' : item_color_liststr,
            'scale' : scale,
            'script':'',
            'scriptEnabled':False,
            
            #Polygon Specific values
            'args' :item_args, 
        }
        #print(self.__LOCK_MODE__)
        if self.__LOCK_MODE__ == True:
            item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,False)
        elif self.__LOCK_MODE__ == False:            
            item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,True)
        item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

        self._scene.addItem(item)
        
        return item

    # Draw Polygon on Viewer  --- Begin    
    def start_Draw_Polygon( self):
        self.setFocus()
        self._Create_Polygon_Tool_MODE = True

    def endDrawPolygon( self,
                        polygonPoints=[],
                        item_color = QtGui.QColor(255,0,0,128),
                        pos = None,
                        scale = 1):
        #Remove all the temp vertex ellipse
        if self._vertex_EllipseItems!= [] and self._vertex_EllipseItems != None:
            for ellipse in self._vertex_EllipseItems:
                self._scene.removeItem(ellipse)   
        
        item_color.setAlpha(128)
        brush = QtGui.QBrush(item_color)
        #pen = QtGui.QPen(item_color)
        pen = QtGui.QPen(item_color, 0.5,  QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        pen.setCosmetic(True)
        pen.setWidth (0)

        if self._vertex_PositionsList != []:
            polygonPoints = self._vertex_PositionsList
        
        # Convert Points List to QPolygonF
        Qpolygon = QtGui.QPolygonF() 
        for point in polygonPoints:
            x = point[0]
            y = point[1]
            Qpolygon.append(QtCore.QPointF(x,y))

        item = Custom_DrawPolygon(QtGui.QPolygonF(Qpolygon))

        item.setScale(scale)
        if pos:
            item.setPos(pos[0],pos[1])
        item.Parent = self #Set Parent
        
        #item.setAcceptHoverEvents(True)
        item._baseBrush = brush
        item._basePen = pen

        item.setPen(pen)
        item.setBrush(brush)
        
        item_type = 'DrawPolygon'
        #IdString = "{:04d}".format(item_ID)
        #item_name = f'{item_type}_{item_ID}'
       
        item_object_list = cmds.ls(sl=1)
        item_args=[]
        
        x = item.boundingRect().x()
        y = item.boundingRect().y()
        w = item.boundingRect().width()
        h = item.boundingRect().height()
        item_bounding_rect=[x, y, w, h]
        item_color_liststr =[item_color.red(), item_color.green(), item_color.blue(), item_color.alpha()]
        
        
        item.itemDict={
            'object_list': item_object_list,
            'type' : item_type,
            'bounding_rect':item_bounding_rect,
            'pos':[item.pos().x(),item.pos().y()],
            'color' : item_color_liststr,
            'scale' : scale,
            'script':'',
            'scriptEnabled':False,
            
            #Polygon Specific values
            'polygonPointsInOrder' : polygonPoints,
            'args' :item_args,
             
        }
        #print(self.__LOCK_MODE__)
        if self.__LOCK_MODE__ == True:
            item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,False)
        elif self.__LOCK_MODE__ == False:            
            item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,True)
        
        item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        
        self._scene.addItem(item)
        

        #Clear Draw Polygon Buffer Variables
        self._Create_Polygon_Tool_MODE = False
        self._Key_Return_Pressed = False
        self._vertex_EllipseItems = []
        self._vertex_PositionsList = [] 
        self.tempPoly = QtGui.QPolygonF()
        self.tempPolyItem = None                   

        return item
    # Draw Polygon on Viewer  --- END


    def getTextDialog(self,inText):
        _Name = ''
        custom_dialog = Custom_Dialog()
        custom_dialog.move(QtGui.QCursor.pos().x(),QtGui.QCursor.pos().y())
        custom_dialog.title = 'Text Lable'
        custom_dialog.labelText = 'Lable'
        
        custom_dialog.setTitle(custom_dialog.title)
        custom_dialog.setLabel(custom_dialog.labelText)

        custom_dialog.lineedit.setText(inText)
        result = custom_dialog.exec_() 
        if result == QtWidgets.QDialog.Accepted: 
            if custom_dialog.get_text() == '':
                return None
            else:
                _Name = custom_dialog.get_text()
                return _Name
        else:
            return None

    def addTextItem(self,
                    text ='Text',
                    textColor = QtGui.QColor(255,255,255,255),
                    BgColor = QtGui.QColor(21, 155, 210, 255),
                    pos = None,
                    scale = 1,
                    ):
        '''
        _Name = None
        if text == 'Text':
            #get Text modal Dialog -------------------------
            _Name = self.getTextDialog(text)
            if _Name == '' or _Name == None:
                return
        '''

        #CREATE Text Button Item    
        #item = QtWidgets.QGraphicsTextItem('text',None)
        item = Custom_TextButton('text',None)
        if pos:
            item.setPos(pos[0],pos[1])
        item.setScale(scale)
        item.Parent = self #Set Parent

        #Set text and text Color
        item.setPlainText(text)
        item.Text = text
        self._baseTextColor = textColor #QtGui.QColor(255,255,255)
        item.setDefaultTextColor(self._baseTextColor)
        
        # Set text Background Color and pen
        
        brush = QtGui.QBrush(BgColor)
        pen = QtGui.QPen(BgColor)#,0.5, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        pen.setCosmetic(True)
        pen.setWidth (0)

        item._baseBrush = brush
        item._basePen = pen
        
        item.setBrush(item._baseBrush)
        item.setPen(item._basePen)

        item_type = 'TextButton'
        #IdString = "{:04d}".format(item_ID)
        #item_name = f'{item_type}_{item_ID}'
       
        item_object_list = str(cmds.ls(sl=1))
        
        #QtCore.QRectF.x(); QtCore.QRectF.y(); QtCore.QRectF.width(); QtCore.QRectF.height()
        x = item.boundingRect().x()
        y = item.boundingRect().y()
        w = item.boundingRect().width()
        h = item.boundingRect().height()
        item_bounding_rect=[x, y, w, h]

        item_BgColor_to_list =  [BgColor.red(),BgColor.green(),BgColor.blue(),BgColor.alpha()]
        item_textColor_to_list =[textColor.red(),textColor.green(),textColor.blue(),textColor.alpha()]
                                                              
        
        item.itemDict={
            'object_list': item_object_list,
            'type' : item_type,
            'bounding_rect':item_bounding_rect, 
            'pos':[item.scenePos().x(),item.scenePos().y()],           
            'color' : item_BgColor_to_list,
            'scale' : scale,
            'script':'',
            'scriptEnabled':False,

            #Text Specific values            
            'text' : text,
            'textcolor' : item_textColor_to_list,
        }
        #------------------------------------------------------
        #print(self.__LOCK_MODE__)
        if self.__LOCK_MODE__ == True:
            item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,False)
        elif self.__LOCK_MODE__ == False:            
            item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,True)
        item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

        self._scene.addItem(item)
        return item
    
    def get_key_modifiers(self):
        QModifiers = QtWidgets.QApplication.keyboardModifiers()
        modifiers = []
        if (QModifiers & QtCore.Qt.ShiftModifier) == QtCore.Qt.ShiftModifier:
            modifiers.append('shift')
        if (QModifiers & QtCore.Qt.ControlModifier) == QtCore.Qt.ControlModifier:
            modifiers.append('control')
        if (QModifiers & QtCore.Qt.AltModifier) == QtCore.Qt.AltModifier:
            modifiers.append('alt')
        return modifiers

    def deleteSelectedItems(self):
        button_pressed = QtWidgets.QMessageBox.question(self, "Delete Items", "Do you really want to remove Shapes?") 
        if button_pressed == QtWidgets.QMessageBox.Yes: 
            pass            
        else: 
            return
        for item in self._scene.selectedItems():
            if item.itemDict:
                self._scene.removeItem(item)        

class MyGraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self,  parent,Viewer):
        super(MyGraphicsScene,  self).__init__()
        self.setBackgroundBrush(QtGui.QBrush(QColor(50,50,50)))
        self.itemUnderMouse = None
        self.Viewer = Viewer
        # self.setSceneRect(50,50,0,0)
        self.mouseScenePosX = 0
        self.mouseScenePosY = 0
    
    def mousePressEvent(self, event):
        self.mouseScenePosX = event.scenePos().x()
        self.mouseScenePosY = event.scenePos().y()
        if __DEBUG__:
            print(f"self.mouseScenePosX : {self.mouseScenePosX} \t self.mouseScenePosY :{self.mouseScenePosY}")
        super(MyGraphicsScene, self).mousePressEvent(event)

    # contextMenuEvent --------------------Begin-------------------------------
    
    def contextMenuEvent(self, event):
        super(MyGraphicsScene, self).contextMenuEvent(event)

        #event = QtWidgets.QGraphicsSceneContextMenuEvent()

        menu = QtWidgets.QMenu()
        #menu.addAction("Get Objects")

        menu.addSection('Get/Clear an item object list')

        Get_Objects = QtWidgets.QAction("Get Objects", None)
        Get_Objects.triggered.connect(self.get_objects)
        menu.addAction(Get_Objects)

        Clear_Objects_List = QtWidgets.QAction("Clear Objects List", None)
        Clear_Objects_List.triggered.connect(self.clear_Objects_List)
        menu.addAction(Clear_Objects_List)

        menu.addSection('Align Items')

        Align_X = QtWidgets.QAction("Align X", None)
        Align_X.triggered.connect(self.align_X)
        menu.addAction(Align_X)

        Align_Y = QtWidgets.QAction("Align Y", None)
        Align_Y.triggered.connect(self.align_Y)
        menu.addAction(Align_Y)
        
        menu.addSeparator()
        
        EvenDistance_X = QtWidgets.QAction("Even Distance X", None)
        EvenDistance_X.triggered.connect(self.evenDistance_X)
        menu.addAction(EvenDistance_X)

        EvenDistance_Y = QtWidgets.QAction("Even Distance Y", None)
        EvenDistance_Y.triggered.connect(self.evenDistance_Y)
        menu.addAction(EvenDistance_Y)
        
        menu.addSeparator()
        
        Copy_Style = QtWidgets.QAction("Copy Style", None)
        Copy_Style.triggered.connect(self.copy_style)
        menu.addAction(Copy_Style)

        Paste_Style = QtWidgets.QAction("Paste Style", None)
        Paste_Style.triggered.connect(self.paste_style)
        menu.addAction(Paste_Style)
        
        menu.addSeparator()
        
        Duplicate_Items_X = QtWidgets.QAction("Duplicate Items to X+", None)
        Duplicate_Items_X.triggered.connect(self.duplicate_Items_X)
        menu.addAction(Duplicate_Items_X)

        Duplicate_Items_Y = QtWidgets.QAction("Duplicate Items to Y+", None)
        Duplicate_Items_Y.triggered.connect(self.duplicate_Items_Y)
        menu.addAction(Duplicate_Items_Y)

        menu.addSeparator()

        DuplicateMirror_X = QtWidgets.QAction("Duplicate Mirror X", None)
        DuplicateMirror_X.triggered.connect(self.duplicateMirror_X)
        menu.addAction(DuplicateMirror_X)
        
   
        DuplicateMirror_Y = QtWidgets.QAction("Duplicate Mirror Y", None)
        DuplicateMirror_Y.triggered.connect(self.duplicateMirror_Y)
        menu.addAction(DuplicateMirror_Y)

        menu.addSeparator()

        Add_Script = QtWidgets.QAction("Add Script", None)
        Add_Script.triggered.connect(self.add_Script)
        menu.addAction(Add_Script)     
        
        menu.addSeparator()
        Set_Scale = QtWidgets.QAction("Set Scale Value", None)
        Set_Scale.triggered.connect(self.set_Scale)
        menu.addAction(Set_Scale)             


        transform = QtGui.QTransform()
        self.itemUnderMouse = self.itemAt(event.scenePos(),transform)
        if __DEBUG__:
            print(type(self.itemUnderMouse))
        
        #if type(self.itemUnderMouse) == QtWidgets.QGraphicsPixmapItem:
        menu.exec_(event.screenPos())

    def get_objects(self):
        
        if self.itemUnderMouse:
            item = self.itemUnderMouse
            DccCommands.MAYA_update_item_object_list(item.itemDict)
            if __DEBUG__:
                print(json.dumps(item.itemDict['object_list']))

    def clear_Objects_List(self):
        item = self.itemUnderMouse
        item.itemDict['object_list'] = []

        if len(self.selectedItems())>1:
            for item in self.selectedItems():
                item.itemDict['object_list'] = []
                
                if __DEBUG__:
                    print("all Items [object_list]'s are cleared")

    def add_Script(self):
        _Text = ''
        item = self.itemUnderMouse
        LastText = item.itemDict['script']
        custom_dialog = Custom_Dialog(multiLineEdit=True,LastText=LastText)
        
        custom_dialog.move(QtGui.QCursor.pos().x()-100,QtGui.QCursor.pos().y()-100)
        
        custom_dialog.title = 'Add a Piece Of Script to the Button'
        custom_dialog.labelText = 'Python Script'
        custom_dialog.setTitle(custom_dialog.title)
        custom_dialog.setLabel(custom_dialog.labelText)

        #custom_dialog.lineedit.setText(item.Text)
        result = custom_dialog.exec_() 
        
        if result == QtWidgets.QDialog.Accepted: 
            if custom_dialog.get_text() == '':
                return
            _Text = custom_dialog.get_text()
            if __DEBUG__:
                print("Script: {0}".format(custom_dialog.get_text()))
        else:
            return        
        #item.Text = _Text
        #item.setPlainText(item.Text)
        item.itemDict['script'] = _Text
  
    def align_X(self):
        #print(self.itemUnderMouse.boundingRect().width())
        #print(self.itemUnderMouse.scale())
        
        if len(self.selectedItems())>1:
            sumX = 0
            for item in self.selectedItems():
                sumX += item.pos().x()
            averageX = sumX / len(self.selectedItems())
            
            for item in self.selectedItems():
                item.setPos(averageX,item.pos().y())
                item.update_Position_Rect_In_ItemDict()

    def align_Y(self):
        sumY = 0
        for item in self.selectedItems():
            sumY += item.pos().y()
        averageY = sumY / len(self.selectedItems())
        
        for item in self.selectedItems():
            item.setPos(item.pos().x(),averageY)
            item.update_Position_Rect_In_ItemDict()

    def evenDistance_X(self):
        if len(self.selectedItems())>1:
            minX = 2000
            maxX = 0
            sumX = 0
            for item in self.selectedItems():
                sumX += item.pos().x()
                #Get Minimum X
                if item.pos().x()<minX:
                    minX = item.pos().x()
                
                #Get Maximum X
                if item.pos().x()>maxX:
                    maxX = item.pos().x()

            averageX = sumX / len(self.selectedItems())
            deltaX = maxX - minX
            distAve = deltaX / len(self.selectedItems())
            
            if __DEBUG__:
                print(f'minX:{minX} maxX:{maxX} deltaX : {deltaX}')
            
            i  = 1
            for item in self.selectedItems():
                x = minX + distAve*i
                y = item.pos().y()
                item.setPos(x,y)   
                item.update_Position_Rect_In_ItemDict()
                i+=1


    def evenDistance_Y(self):
        if len(self.selectedItems())>1:
            
            list_y = []
            selectedItems = []
            for item in self.selectedItems():
                list_y.append(item.pos().y())
                selectedItems.append(item)


            minY = min(list_y)
            maxY = max(list_y)

            deltaY = abs(maxY - minY)
            distAve = deltaY / len(selectedItems)
            
            #print(f'minX:{minY} \nmaxX:{maxY} \ndeltaX : {deltaY} \ndistAverage:{distAve}')
            #print('_'*30)

            i  = 0
            for item in selectedItems:
                x = item.pos().x()
                y = minY + distAve*i
                item.setPos(x,y)   
                item.update_Position_Rect_In_ItemDict()                
                i+=1

    def copy_style(self):
        #transform = QtGui.QTransform()
        #item = self.itemAt(event.scenePos(),transform)
        self.CopiedStyleBrush = None
        self.CopiedStylePen = None
        
        self.CopiedStyleBrush = self.itemUnderMouse.brush()
        self.CopiedStylePen = self.itemUnderMouse.pen()
    
    def QColorToList(self,QColor):
        item_color_liststr = [QColor.red(), QColor.green(), QColor.blue(), QColor.alpha()]
        return (item_color_liststr)            

    def paste_style(self):
                
        if self.CopiedStyleBrush:
            self.itemUnderMouse.setBrush(self.CopiedStyleBrush)
            self.itemUnderMouse.setPen(self.CopiedStylePen)
            #Update color in the Item Dictionary
            self.itemUnderMouse.itemDict['color'] = self.QColorToList(self.CopiedStyleBrush.color())
            
            for item in self.selectedItems():
                try:
                    item.setBrush(self.CopiedStyleBrush)
                    item.setPen(self.CopiedStylePen)
                    #Update color in the Item Dictionary
                    item.itemDict['color'] = self.QColorToList(self.CopiedStyleBrush.color())                    
                except:pass

    def Duplicate_Selected_Items(self,offsetX=0,offsetY=0):
        for item in self.selectedItems():
        #Item Dictionary to objects and variables
            object_list = item.itemDict['object_list']
            type = item.itemDict['type']
            boundingRect = item.itemDict['bounding_rect']
            color = QtGui.QColor(item.itemDict['color'][0], item.itemDict['color'][1], item.itemDict['color'][2], item.itemDict['color'][3])
            scale = item.itemDict['scale']

            pos = [item.itemDict['pos'][0] + offsetX, item.itemDict['pos'][1] + offsetY]
            
            script = item.itemDict['script']
            

            if type == 'ellipse' or type == 'rectangle':
                rect = item.itemDict['rect']

            if type == 'TextButton':
                text = item.itemDict['text']
                textcolor = QtGui.QColor(item.itemDict['textcolor'][0], item.itemDict['textcolor'][1], item.itemDict['textcolor'][2], item.itemDict['textcolor'][3])
            
            if type == 'Polygon':
                args = item.itemDict['args']

            if type == 'DrawPolygon':
                polygonPoints = item.itemDict['polygonPointsInOrder']

            # Add the Items 
            #LoadedTabPage.viewer.addEllipse()
            if type == 'ellipse':
                new_item = self.Viewer.addEllipse(x=10,y=10,w=rect[2],h=rect[3],
                                                        item_color= color,
                                                        scale = scale,
                                                        pos = pos)

                #item.setPos
                

            if type == 'rectangle':
                new_item = self.Viewer.addRect(x=10,y=10,w=rect[2],h=rect[3],
                                                        item_color= color,
                                                        scale = scale,
                                                        pos = pos)

            if type == 'Polygon':
                new_item = self.addPolygon_Diamond_Shape(n=args[0],r=args[1],s=args[2],
                                                        item_color=color,
                                                        scale = scale,
                                                        pos = pos)             

            if type == 'DrawPolygon':
                new_item = self.Viewer.endDrawPolygon( polygonPoints=polygonPoints,
                                                                item_color = color,
                                                                pos = pos,
                                                                scale = scale)      


            if type == 'TextButton':
                new_item = self.Viewer.addTextItem(text = text,
                                                        textColor = textcolor,
                                                        BgColor = color,
                                                        scale = scale,
                                                        pos = pos )
                new_item.setPlainText(text)
                new_item.setBrush(QtGui.QBrush(color))  


            new_item.itemDict['script'] = script
            new_item.itemDict['object_list'] = object_list  

    def Duplicate_Selected_Item(self,item,offsetX=0,offsetY=0):
        object_list = item.itemDict['object_list']
        type = item.itemDict['type']
        boundingRect = item.itemDict['bounding_rect']
        color = QtGui.QColor(item.itemDict['color'][0], item.itemDict['color'][1], item.itemDict['color'][2], item.itemDict['color'][3])
        scale = item.itemDict['scale']

        pos = [item.itemDict['pos'][0] + offsetX, item.itemDict['pos'][1] + offsetY]
        
        script = item.itemDict['script']
        

        if type == 'ellipse' or type == 'rectangle':
            rect = item.itemDict['rect']

        if type == 'TextButton':
            text = item.itemDict['text']
            textcolor = QtGui.QColor(item.itemDict['textcolor'][0], item.itemDict['textcolor'][1], item.itemDict['textcolor'][2], item.itemDict['textcolor'][3])
        
        if type == 'Polygon':
            args = item.itemDict['args']

        if type == 'DrawPolygon':
            polygonPoints = item.itemDict['polygonPointsInOrder']

        # Add the Items 
        #LoadedTabPage.viewer.addEllipse()
        if type == 'ellipse':
            new_item = self.Viewer.addEllipse(x=10,y=10,w=rect[2],h=rect[3],
                                                    item_color= color,
                                                    scale = scale,
                                                    pos = pos)

            #item.setPos
            

        if type == 'rectangle':
            new_item = self.Viewer.addRect(x=10,y=10,w=rect[2],h=rect[3],
                                                    item_color= color,
                                                    scale = scale,
                                                    pos = pos)

        if type == 'Polygon':
            new_item = self.addPolygon_Diamond_Shape(n=args[0],r=args[1],s=args[2],
                                                    item_color=color,
                                                    scale = scale,
                                                    pos = pos)             

        if type == 'DrawPolygon':
            new_item = self.Viewer.endDrawPolygon( polygonPoints=polygonPoints,
                                                            item_color = color,
                                                            pos = pos,
                                                            scale = scale)      


        if type == 'TextButton':
            new_item = self.Viewer.addTextItem(text = text,
                                                    textColor = textcolor,
                                                    BgColor = color,
                                                    scale = scale,
                                                    pos = pos )
            new_item.setPlainText(text)
            new_item.setBrush(QtGui.QBrush(color))  


        new_item.itemDict['script'] = script
        new_item.itemDict['object_list'] = object_list  

    def Get_Distance(self, X=True,Y=False):
        if X:
            #return Distance X
            pass
        if Y:
            #return Distance Y
            pass

    def duplicate_Items_X(self):
        
        #Distance X axis between the first selected item to the last selected item
        list_X = []
        for item in self.selectedItems():
            list_X.append(item.pos().x()+item.boundingRect().width())
        minX = min(list_X)
        maxX = max(list_X)
        delta = abs(maxX-minX)
        offset = delta + 50
        
        if len(self.selectedItems())<2:
            delta = item.boundingRect().width()
        
        #Duplicate
        self.Duplicate_Selected_Items(offsetX = offset)

    def duplicate_Items_Y(self):
        
        #Distance Y axis between the first selected item to the last selected item
        list_Y = []
        for item in self.selectedItems():
            list_Y.append(item.pos().y()+item.boundingRect().height())
        minY = min(list_Y)
        maxY = max(list_Y)
        delta = abs(maxY-minY)
        offset = delta + 50
        
        if len(self.selectedItems())<2:
            delta = item.boundingRect().height()

        #Duplicate
        self.Duplicate_Selected_Items(offsetY = offset)

    def duplicateMirror_X(self):
        for item in self.selectedItems():
            centerX = self.width()/2
            DistToCenter = centerX - item.pos().x()
            NewX = (DistToCenter *2)
            self.Duplicate_Selected_Item(item,offsetX=NewX)
        
        if __DEBUG__:
            print(self.width())
        
    def duplicateMirror_Y(self):
        for item in self.selectedItems():
            centerY = self.height()/2
            DistToCenter = centerY - item.pos().y()
            NewY = (DistToCenter *2)
            self.Duplicate_Selected_Item(item,offsetY=NewY)
        
        if __DEBUG__:
            print(self.height())

    def set_Scale(self):
        custom_dialog = Custom_Dialog()
        ScaleNum = ''
        custom_dialog = Custom_Dialog()
        custom_dialog.LastText = '1'
        custom_dialog.move(QtGui.QCursor.pos().x(),QtGui.QCursor.pos().y()) 
        result = custom_dialog.exec_() 
        if result == QtWidgets.QDialog.Accepted: 
            if custom_dialog.get_text() == '':
                return
            ScaleNum = int(custom_dialog.get_text())
        else:
            ScaleNum = ''

        if ScaleNum != '':
            self.itemUnderMouse.setScale(ScaleNum)
            self.itemUnderMouse['scale'] = ScaleNum
            for item in self.selectedItems():
                item.setScale(ScaleNum)
                item.itemDict['scale'] = ScaleNum

    # contextMenuEvent -------------------END -----------------------------            
#NEW ---------------------------- End

class PickerWidget(QtWidgets.QTabWidget): #PickerWidget(QtWidgets.QWidget) - A tab Page
    """
        Create a Tab Page
        Combination of Custom_GraphicViewer() + Custom_Ellipse() + Custom_Rect() + Custom_Polygon() 
        to make a widget to be able to add it to the main TabWidget
    """

    def __init__(self, parent=None):
        super(PickerWidget, self).__init__(parent)
        
        self.Parent = None
        self.preferedDir = None
        self.PhotoPath = __DEFAULT_IMAGE__
        self.Photo = QtGui.QPixmap(self.PhotoPath)
        self.PrefixList=['','Jonar','Karma','Hedda','...']

        self.makeTabPageUI()
        self.createConnections()
        
        
    # Our Functions for the new tab
    def makeTabPageUI(self):
       
        #ICONs
        RainbowICO = CustomICO().RainbowICO
        lightGreenICO = CustomICO().lightGreenICO
        lightOrangeICO = CustomICO().lightOrangeICO
        lightPinkICO = CustomICO().lightPinkICO
        lightRedICO = CustomICO().lightRedICO
        lightBlueICO = CustomICO().lightBlueICO
        darkBlueICO = CustomICO().darkBlueICO
        yellowICO = CustomICO().yellowICO
        purpleICO = CustomICO().purpleICO

                
        fileOpenICO = CustomICO().fileOpenICO
        CircleICO = CustomICO().CircleICO
        RectICO = CustomICO().RectICO

        DiamondICO = CustomICO().DiamondICO
        ScaleUpICO = CustomICO().ScaleUpICO
        ScaleDownICO = CustomICO().ScaleDownICO
        DeleteICO = CustomICO().DeleteICO
        TextButtonICO = CustomICO().TextButtonICO

        InfoICO = CustomICO().InfoICO
        
        # Making a TAB to add to the tabwidget
        self.tabName = "tab_1"
        #self.setObjectName(self.tabName)
        
        #Add the viewer to the this new Tab
        InTabVBlayout = QtWidgets.QVBoxLayout(self) # whole in tab verical layout
        InTabHBlayoutTop = QtWidgets.QHBoxLayout(self)
        InTabVBlayout.addLayout(InTabHBlayoutTop) #Top bar inside the tab Horizental Layout

        self.btnAddPrefix = QtWidgets.QToolButton(self)
        self.btnAddPrefix.setIcon(QtGui.QIcon(CustomICO().PlusICO))
        InTabHBlayoutTop.addWidget(self.btnAddPrefix)

        self.LE_Prefix = Custom_LineEdit('Karma')
        InTabHBlayoutTop.addWidget(self.LE_Prefix)
        self.LE_Prefix.setVisible(False)


        self.btnRemovePrefix = QtWidgets.QToolButton(self)
        self.btnRemovePrefix.setIcon(QtGui.QIcon(CustomICO().DeleteICO))
        InTabHBlayoutTop.addWidget(self.btnRemovePrefix)


        self.CB_charatersPrefixList = QtWidgets.QComboBox()
        self.CB_charatersPrefixList.addItems(self.PrefixList)
        InTabHBlayoutTop.addWidget(self.CB_charatersPrefixList)
        

        self.btnLockUnlock = QtWidgets.QPushButton(self)
        self.btnLockUnlock.setText('Lock/Unlock')
        InTabHBlayoutTop.addWidget(self.btnLockUnlock)
        self.btnLockUnlock.setCheckable(True)
        self.btnLockUnlock.setChecked(True)
        
        
        self.viewer = Custom_GraphicViewer(self)
        InTabVBlayout.addWidget(self.viewer)
        


        # Bottom bar buttons
        self.btnLoad = QtWidgets.QToolButton(self)
        #self.btnLoad.setText('Load image')
        self.btnLoad.setIcon(QtGui.QIcon(fileOpenICO)) 
        self.btnLoad.setToolTip('Load Image') 

        #LIST OF ICONS IN MAYA
        #for item in cmds.resourceManager(nameFilter="*png"): 
            #print(item)

        self.btnAddEllipse = QtWidgets.QToolButton(self)
        #self.btnAddEllipse.setText('Add Circle')
        self.btnAddEllipse.setIcon(QtGui.QIcon(CircleICO)) 
        self.btnAddEllipse.setToolTip('Add Circle') 

        self.btnAddRect = QtWidgets.QToolButton(self)
        #self.btnAddRect.setText('Add Rect')
        self.btnAddRect.setIcon(QtGui.QIcon(RectICO))  #self.btnAddRect.setIcon(QtGui.QIcon(":square.png")) 
        self.btnAddRect.setToolTip('Add Rect')

        
        self.btnAddDrawPolygon = QtWidgets.QToolButton(self)
        #self.btnAddDrawPolygon.setText('Add polygon')
        self.btnAddDrawPolygon.setIcon(QtGui.QIcon(DiamondICO))  
        self.btnAddDrawPolygon.setToolTip('Draw Polygon Shape')
        

        self.btnText = QtWidgets.QToolButton(self)
        #self.btnText.setText('Text')
        self.btnText.setIcon(QtGui.QIcon(TextButtonICO))  #self.btnAddRect.setIcon(QtGui.QIcon(":square.png")) 
        self.btnText.setToolTip('Add Text')
       
        #Color Buttons ------

        self.btnSetColorDialog = QtWidgets.QToolButton(self)
        #self.btnSetColorDialog.setText('Green')
        self.btnSetColorDialog.setIcon(QtGui.QIcon(RainbowICO)) 
        self.btnSetColorDialog.setToolTip('Green') 

        self.btnScaleUp = QtWidgets.QToolButton(self)
        #self.btnScaleUp.setText('+')
        self.btnScaleUp.setIcon(QtGui.QIcon(ScaleUpICO)) 
        self.btnScaleUp.setToolTip('Scale Up') 

        self.btnScaleDown = QtWidgets.QToolButton(self)
        #self.btnScaleDown.setText('-')
        self.btnScaleDown.setIcon(QtGui.QIcon(ScaleDownICO)) 
        self.btnScaleDown.setToolTip('Scale Down') 

        self.btnDeleteItem = QtWidgets.QToolButton(self)
        #self.btnDeleteItem.setText('Delete Item')
        self.btnDeleteItem.setIcon(QtGui.QIcon(DeleteICO)) 
        self.btnDeleteItem.setToolTip('Delete Item')         

        self.btnInfo = QtWidgets.QToolButton(self)
        #self.btnInfo.setText('Info Item')
        self.btnInfo.setIcon(QtGui.QIcon(InfoICO)) 
        Info = '______________Keyboard Shortcuts________________\n\n'
        Info +=' F             : Zoom fit View\n'
        Info +=' Ctrl + LMB     : Add to selection\n'
        Info +='_________________________________________________\n'
        Info +=' +             : Scale Up\n'
        Info +=' -             : Scale Down\n'
        Info +=' Ctrl +        : Scale Up Width [X]\n'
        Info +=' Ctrl -        : Scale Down Width [X]\n'
        Info +=' Alt +         : Scale Up Height [Y]\n'
        Info +=' Alt -         : Scale Down Height [Y]\n'
        Info +='_________________________________________________\n'
        Info +=' W/A/S/D        : Move Up/Down/Left/Right\n'
        Info +=' Ctrl + W/A/S/D : Move Faster Up/Down/Left/Right\n'
        Info +='_________________________________________________\n'
        Info +=' Space + LMB    : Pan '
        Info +=' MidleMouse     : Pan '
        Info +=' Double MidleMouse : Zoom fit View '

        self.btnInfo.setToolTip(Info)   

        InTabHBlayoutBottom = QtWidgets.QHBoxLayout()
        InTabHBlayoutBottom.setAlignment(QtCore.Qt.AlignLeft)
        InTabHBlayoutBottom.addWidget(self.btnLoad)

        InTabHBlayoutBottom.addWidget(self.btnAddEllipse)
        InTabHBlayoutBottom.addWidget(self.btnAddRect)
        
        
        InTabHBlayoutBottom.addWidget(self.btnAddDrawPolygon)
        

        InTabHBlayoutBottom.addWidget(self.btnText)
        InTabHBlayoutBottom.addWidget(self.btnScaleUp)
        InTabHBlayoutBottom.addWidget(self.btnScaleDown)
        InTabHBlayoutBottom.addWidget(self.btnSetColorDialog)
        InTabHBlayoutBottom.addWidget(self.btnDeleteItem)
        InTabHBlayoutBottom.addWidget(self.btnInfo)

        InTabVBlayout.addLayout(InTabHBlayoutBottom)


    def createConnections(self):
        self.btnLoad.clicked.connect(self.btnLoadImage_clicked)
        self.btnAddEllipse.clicked.connect(self.btnAddEllipse_clicked)
        self.btnAddRect.clicked.connect(self.btnAddRect_clicked)
        
        self.btnAddDrawPolygon.clicked.connect(self.btnAddDrawPolygon_clicked)
        
        self.btnText.clicked.connect(self.btnText_clicked)
        self.btnLockUnlock.clicked.connect(self.btnLockUnlock_clicked)

        #Add/Remove Prefix 
        self.btnAddPrefix.clicked.connect(self.btnAddPrefix_clicked)
        self.btnRemovePrefix.clicked.connect(self.btnRemovePrefix_clicked)
        
        self.LE_Prefix.returnPressed.connect(self.LE_Prefix_returnPressed)
        self.CB_charatersPrefixList.currentIndexChanged.connect(self.CB_charatersPrefixList_currentIndexChanged)

        self.btnScaleUp.clicked.connect(self.btnScaleUp_clicked)
        self.btnScaleDown.clicked.connect(self.btnScaleDown_clicked)
        #self.viewer.photoClicked.connect(self.photoClicked)
        self.btnDeleteItem.clicked.connect(self.btnDeleteItem_clicked)
        
        #---- Color Buttons ---- Begin
        self.btnSetColorDialog.clicked.connect(self.btnSetColorDialog_clicked)
        #----------------------- End

    #---- Color Buttons ---- QColor to str([List]) / List to QColor 
    def QColorToList(self,QColor):
        
        item_color_liststr = [QColor.red(), QColor.green(), QColor.blue(), QColor.alpha()]
                        
        return (item_color_liststr)

    def colorListStringToQColor(self,ColorList=[255,0,255,255]):
        QColor = QtGui.QColor(ColorList[0],ColorList[1],ColorList[2],ColorList[3])
        return QColor

    def updateDictionary_color(self,item):
        item.itemDict['color'] = self.QColorToList(item.brush().color())

    def updatePrefixList(self):
        self.CB_charatersPrefixList.clear()
        for item in self.PrefixList:
            self.CB_charatersPrefixList.addItem(item)

    #---- Color Buttons ---- Events
    def show_color_select(self): 
        """ 
        Display Qt's color select dialog 
        Return 
        """ 
        self.initial_color = QtGui.QColor(0,255,0,128)

        self.colorDialog = QtWidgets.QColorDialog()
        self.colorDialog.setOption(QtWidgets.QColorDialog.ShowAlphaChannel, on=True)
        if self.colorDialog.exec_() == QtWidgets.QDialog.Accepted:
            outColor = self.colorDialog.selectedColor()
            if outColor.isValid():
                self.initial_color = outColor
                return self.initial_color
        
        #self.initial_color = self.colorDialog.getColor(self.initial_color, self) 
        '''
        print("Red:{0} Green:{1} Blue:{2}".format(self.initial_color.red(), 
												  self.initial_color.green(), 
												  self.initial_color.blue()))
        print ('self.colorDialog:',self.colorDialog)
        print ('self.initial_color:',self.initial_color)
        '''
        #if self.initial_color.isValid():
        #    return self.initial_color
        #else:
        #    return None
    
    def btnSetColorDialog_clicked(self):
        QColor = self.show_color_select()
        if QColor:
            #print (QColor)
            brush = QtGui.QBrush(QColor)
            pen = QtGui.QPen(QColor)
            pen.setCosmetic(True)
            pen.setWidth(0)

            for item in self.viewer.scene().selectedItems():
                if item.itemDict:
                    item._baseBrush = brush
                    item._basePen = pen
                    #item._basePen = QtGui.QPen(QtGui.QColor(20, 20, 20,a=255))
                    item.setBrush(brush)
                    item.setPen(pen)
                    self.updateDictionary_color(item)
                    item.update()

    def btnDeleteItem_clicked(self):
        self.viewer.deleteSelectedItems()

    def btnScaleUp_clicked(self):
        self.viewer.scaleUp_SelectedItems()

    def btnScaleDown_clicked(self):
        self.viewer.scaleDown_SelectedItems()

    # Button Add shapes Events
    def btnAddEllipse_clicked(self):
        ellipse = self.viewer.addEllipse(x=10,y=10,w=30,h=30,                    
                                        item_color=QtGui.QColor(0,230, 0,a=255))
        
        #print(f'Ellipse : {ellipse}')

    def btnAddRect_clicked(self):
        Rect = self.viewer.addRect(x=10,y=10,w=30,h=30,                    
                                        item_color=QtGui.QColor(0,230, 0,a=255))
        #print(f'Rect : {Rect}')

    def btnAddDrawPolygon_clicked(self):
        # Polygon = self.viewer.addPolygon_Diamond_Shape(n=4,r=20,s=0,
                                        # item_color=QtGui.QColor(0,230, 0,a=255))
        Polygon = self.viewer.start_Draw_Polygon() 
        #print(f'Polygon : {Polygon}')

    def btnText_clicked(self):
        #self.viewer.addTextItem()

        self.viewer.addTextItem(text ='Text',
                                textColor = QtGui.QColor(255,255,255,255),
                                BgColor = QtGui.QColor(128,0,128,255),
                                scale = 1,
                                )

        
                       
        
        #self.viewer._scene.addItem(self.viewer.addTextItem())
        #print('Text')
        #self.toggle = not self.toggle
        '''
        for item in self.viewer.items():
            #item = QtWidgets.QGraphicsEllipseItem()
            #print(type(item))
            #Print Dictionary
            
            try:
                if item.itemDict:
                    print(json.dumps(item.itemDict,indent=4)) #sort_keys=True
                    pass
            except Exception as e:
                print(e)
            '''
        
        '''
        if self.toggle:
            self.viewer.setPhoto(QtGui.QPixmap(__DEFAULT_IMAGE__)) 
        else:
            self.viewer.setPhoto(QtGui.QPixmap(__DEFAULT_IMAGE__))            
        '''
    
    #Top Buttons Events
    def btnLockUnlock_clicked(self,check):
        self.viewer.__LOCK_MODE__ = check
        if __DEBUG__:
            print(check)
        for item in self.viewer._scene.items():
            if check:
                if type(item) != QtWidgets.QGraphicsPixmapItem:
                    item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable,enabled=False)
                    #item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable,enabled=False)
            else:
                if type(item) != QtWidgets.QGraphicsPixmapItem:
                    item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
                    item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

    def btnLoadImage_clicked(self):
        FILE_FILTERS = 'Image (*.png *.Jpg *.Jpeg );;All Files (*.*)' 
        selected_filter = 'Image (*.png *.Jpg *.Jpeg )' 
        try:
            if not self.preferedDir:
                self.preferedDir = __MODULE_PATH__
        except:
                self.preferedDir = __MODULE_PATH__
        file_path, selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, "Select Image File",self.preferedDir,FILE_FILTERS,selected_filter) 
        if file_path:
            self.PhotoPath = file_path
            #self.filepath_le.setText(file_path)
            self.viewer.setPhoto(QtGui.QPixmap(file_path))
            self.preferedDir = os.path.dirname(file_path)

    #Add/Remove Prefix Events -----------
    def btnAddPrefix_clicked(self):
        self.LE_Prefix.setVisible(True)
        self.LE_Prefix.setFocus()
        #self.PrefixList.sort()

    def btnRemovePrefix_clicked(self):
        currentText = self.CB_charatersPrefixList.currentText()
        currentIndex = self.CB_charatersPrefixList.currentIndex()
        button_pressed = QtWidgets.QMessageBox.question(self, "Remove Prefix Dialog", 
                                                              f"Do you really want to Remove [{currentText}] ?") 
        if button_pressed == QtWidgets.QMessageBox.Yes: 

            self.PrefixList.pop(currentIndex)
            self.updatePrefixList()
        else: 
            print("I knew you didn't mean to delete an Item!") 

    def LE_Prefix_returnPressed(self):
        
        if self.LE_Prefix.text() in self.PrefixList:
            return

        #add to the prefix list and sorts the list
        self.PrefixList.append(self.LE_Prefix.text())
        self.PrefixList.sort()
        self.updatePrefixList() # clears the combo box and adds the items again with the new item added

        #Set combo index base on the new text
        index = self.CB_charatersPrefixList.findText(self.LE_Prefix.text(), QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.CB_charatersPrefixList.setCurrentIndex(index)
        #self.CB_charatersPrefixList.addItem(self.LE_Prefix.text())
        #self.CB_charatersPrefixList.setCurrentIndex(self.CB_charatersPrefixList.count()-1)
        #print(self.CB_charatersPrefixList.currentIndex())
        #print(self.CB_charatersPrefixList.count())
        #self.LE_Prefix.setText('')
        self.LE_Prefix.setVisible(False)

    def CB_charatersPrefixList_currentIndexChanged(self,index):
        #set the viewer chrPrefix to the current prefix on the combo box
        self.viewer.chrPrefix = self.CB_charatersPrefixList.currentText()


# ------------------------------------ Main Program UI -----------------------------------

class PickerUI(QtWidgets.QDialog):
    
    def __init__(self,parent=None):
        super(PickerUI, self).__init__(parent)
        #self.parent = MayaWindow
        self.setGeometry(500, 300, 450, 800)
        self.setWindowTitle('HPK Picker 1.8.0 [New Year Edition 2022]')

        self.createUI()
        self.createConnections()
        #self.loadImage()

        self.toggle = True
        self.backgroundImage = QtGui.QPixmap(__DEFAULT_IMAGE__)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)              
        
        self.centerWidgetOnScreen(self)
        if __DEBUG__:
            print('Dialog Pos : ', self.pos())
            print('Dialog Size : ', self.size())

    def centerWidgetOnScreen(self,widget):
        centerPoint = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
        fg = widget.frameGeometry()
        fg.moveCenter(centerPoint)
        widget.move(fg.topLeft())

    def createUI(self):

        # Arrange layout
        self.MainVBlayout = QtWidgets.QVBoxLayout(self)
        self.MainVBlayout.setObjectName("MainVBlayout")

        self.TopHlayout = QtWidgets.QHBoxLayout()
        self.TopHlayout.setAlignment(QtCore.Qt.AlignLeft)
        self.MainVBlayout.addLayout(self.TopHlayout)

        #Icons
        fileNewICO = CustomICO().fileNewICO
        fileOpenICO = CustomICO().fileOpenICO
        fileSaveICO = CustomICO().fileSaveICO
        
        # Main Buttons
        self.btnNewTab = QtWidgets.QToolButton(self)
        #self.btnNewTab.setText('New Layout Tab')
        self.btnNewTab.setIcon(QtGui.QIcon(fileNewICO)) 
        self.btnNewTab.setToolTip('New Tab') 
        self.TopHlayout.addWidget(self.btnNewTab)

        self.btnOpenTab = QtWidgets.QToolButton(self)
        #self.btnOpen.setText('Open Layout')
        self.TopHlayout.addWidget(self.btnOpenTab)
        self.btnOpenTab.setIcon(QtGui.QIcon(fileOpenICO)) 
        self.btnOpenTab.setToolTip('Open Tab') 

        self.btnSaveTab = QtWidgets.QToolButton(self)
        #self.btnSaveTab.setText('Save Layout')
        self.TopHlayout.addWidget(self.btnSaveTab)
        self.btnSaveTab.setIcon(QtGui.QIcon(fileSaveICO)) 
        self.btnSaveTab.setToolTip('Save Tab')        

        #Tab widget
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.MainVBlayout.addWidget(self.tabWidget)
        self.tabWidget.setCurrentIndex(0)

        # Make the Tab bar Text Editable by Double Click
        #self.tabWidget.tabBarDoubleClicked.connect(self.On_tabBar_DoubleClicked)
        self.tabWidget.setTabBar(EditableTabBar(self))
        self.tabWidget.setTabsClosable(True)

    def closeTab (self, currentIndex): # Remove a tab page
        currentQWidget = self.tabWidget.widget(currentIndex)
        #currentQWidget.deleteLater()
        #self.tabWidget.removeTab(currentIndex)

        # Ask a question to be more polit before closing the Tab        
        button_pressed = QtWidgets.QMessageBox.question(self, "closing the Tab", "Do you really want to close this tab?") 
        if button_pressed == QtWidgets.QMessageBox.Yes: 
            currentQWidget.deleteLater()
            self.tabWidget.removeTab(currentIndex)
        else: 
            print("I knew you didn't mean it!") 
            pass

    def createConnections(self):
        self.btnNewTab.clicked.connect(self.btnNewTab_clicked)
        self.btnSaveTab.clicked.connect(self.btnSaveTab_clicked)
        self.btnOpenTab.clicked.connect(self.btnOpenTab_clicked)
        
    def btnNewTab_clicked(self,args):
        """
            Custom Modal Dialog to ask the New tab inputs
        """
        _Name = ''
        custom_dialog = Custom_Dialog()
        custom_dialog.move(QtGui.QCursor.pos().x(),QtGui.QCursor.pos().y()) 
        result = custom_dialog.exec_() 
        if result == QtWidgets.QDialog.Accepted: 
            if custom_dialog.get_text() == '':
                return
            _Name = custom_dialog.get_text()
            #print("Name: {0}".format(custom_dialog.get_text()))
        else:
            return

        """
            Add a PickerWidget() as a Tab page
        """
        self.newPickerWidget = PickerWidget()
        self.newPickerWidget.Parent = self.tabWidget
        self.tabWidget.addTab(self.newPickerWidget,_Name) # CREATE A TAB IN THE MAIN TAB WIDGET
        self.tabWidget.setCurrentIndex(self.tabWidget.count()-1)
        
        #Set Tab Photo
        self.newPickerWidget.Photo = QtGui.QPixmap(__DEFAULT_IMAGE__)
        self.newPickerWidget.PhotoPath = __DEFAULT_IMAGE__
        self.newPickerWidget.viewer.setPhoto(self.newPickerWidget.Photo)
        
        if __DEBUG__:
            print('count:',self.tabWidget.count())
        
    def save_file_dialog(self):
        self.FILE_FILTERS = "Picker (*.json);;All Files (*.*)" 
        self.selected_filter = "Picker (*.json)"
        file_path, self.selected_filter = QtWidgets.QFileDialog.getSaveFileName(self, "Save File As", "", self.FILE_FILTERS, self.selected_filter) 
        if file_path:
            if __DEBUG__: 
                print("File path: {0}".format(file_path))
            return file_path
        else:
            return None
    
    def open_file_dialog(self):
        self.FILE_FILTERS = "Picker (*.json);;All Files (*.*)" 
        self.selected_filter = "Picker (*.json)"
        initialDir = os.path.join(__MODULE_PATH__,'UiLayouts')
        file_path, self.selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, "Select a File", initialDir, self.FILE_FILTERS, self.selected_filter) 
        if file_path: 
            if __DEBUG__:
                print("File path: {0}".format(file_path)) 
            return file_path

    def btnSaveTab_clicked(self,args):
        '''
        Note:
            current Tab is from  'PickerWidget'
            Main tab is from  'QTabWidget'
        '''
        if self.tabWidget.count()<1: #(If there is no tab page in the tabWidget)
            return
        currentTab_Index = self.tabWidget.currentIndex()
        currentTab_Widget = self.tabWidget.currentWidget()
        currentTab_Name = self.tabWidget.tabText(currentTab_Index)
        currentTab_itemsCount = len(self.tabWidget.currentWidget().viewer._scene.items())
        currentTab_items = self.tabWidget.currentWidget().viewer._scene.items() #(getting the current tab items) 
        currentTab_Photo = self.tabWidget.currentWidget().PhotoPath 
        currentTab_PrefixList =self.tabWidget.currentWidget().PrefixList

        currentTabInfo = {
            'TabName':currentTab_Name,
            'TabPhoto':currentTab_Photo,
            'PrefixList':currentTab_PrefixList
        }
        #PickerWidget.tabText() 
        if __DEBUG__:
            print('currentIndex  : ',currentTab_Index)
            print('currentWidget : ',currentTab_Widget)
            print('currentWidget Item Count : ',currentTab_itemsCount)
            print('currentWidget tab name : ',currentTab_Name)
            print('currentWidget tab Photo : ',currentTab_Photo)
       
        
        filePath = self.save_file_dialog()
        if not filePath: return
        filePath = os.path.normpath(filePath)
        
        listOfItemDicts = []
        listOfItemDicts.append(currentTabInfo)

        try:
            for item in currentTab_items:
                if type(item) != QtWidgets.QGraphicsPixmapItem: # if the item is not the background image
                    #print(json.dumps(item.itemDict,indent=4))
                    listOfItemDicts.append(item.itemDict)
            
            with open(filePath, 'w') as outfile:
                json.dump(listOfItemDicts,outfile,indent=4)

        except: 
            print('There is not tab added yet')
        
    def btnOpenTab_clicked(self):
        filePath = self.open_file_dialog()
        
        if filePath:
            with open(filePath) as json_file:
                data = json.load(json_file)
        else:
            return                
        
        if data:
            if __DEBUG__:
                print(data)
            #print(data[1:])
       
        # Construct the tab page
        _TabName = data[0]["TabName"]
        _TabPhoto = data[0]["TabPhoto"]
        PrefixList = data[0]["PrefixList"]
        _ShapesDict = data[1:]
        _ItemCount = len(_ShapesDict)
        


        LoadedTabPage = PickerWidget()
        LoadedTabPage.PrefixList = PrefixList
        LoadedTabPage.updatePrefixList()
        LoadedTabPage.Parent = self.tabWidget
        self.tabWidget.addTab(LoadedTabPage,_TabName) # CREATE A TAB IN THE MAIN TAB WIDGET
        self.tabWidget.setCurrentIndex(self.tabWidget.count()-1)
        LoadedTabPage.PhotoPath = _TabPhoto
        LoadedTabPage.Photo = QtGui.QPixmap(LoadedTabPage.PhotoPath)
        LoadedTabPage.viewer.setPhoto(LoadedTabPage.Photo)
        
        #Item Dictionary to objects and variables
        for item in _ShapesDict:
            object_list = item['object_list']
            type = item['type']
            boundingRect = item['bounding_rect']
            color = QtGui.QColor(item['color'][0], item['color'][1], item['color'][2], item['color'][3])
            scale = item['scale']
            pos = item['pos']
            script = item['script']
            


            if type == 'ellipse' or type == 'rectangle':
                rect = item['rect']

            if type == 'TextButton':
                text = item['text']
                textcolor = QtGui.QColor(item['textcolor'][0], item['textcolor'][1], item['textcolor'][2], item['textcolor'][3])
            
            if type == 'Polygon':
                args = item['args']

            if type == 'DrawPolygon':
                polygonPoints = item['polygonPointsInOrder']

            # Add the Items 
            #LoadedTabPage.viewer.addEllipse()
            if type == 'ellipse':
                new_item = LoadedTabPage.viewer.addEllipse(x=10,y=10,w=rect[2],h=rect[3],
                                                        item_color= color,
                                                        scale = scale,
                                                        pos = pos)

                #item.setPos
                

            if type == 'rectangle':
                new_item = LoadedTabPage.viewer.addRect(x=10,y=10,w=rect[2],h=rect[3],
                                                        item_color= color,
                                                        scale = scale,
                                                        pos = pos)

            if type == 'Polygon':
                new_item = LoadedTabPage.viewer.addPolygon_Diamond_Shape(n=args[0],r=args[1],s=args[2],
                                                        item_color=color,
                                                        scale = scale,
                                                        pos = pos)             

            if type == 'DrawPolygon':
                new_item = LoadedTabPage.viewer.endDrawPolygon( polygonPoints=polygonPoints,
                                                                item_color = color,
                                                                pos = pos,
                                                                scale = scale)      


            if type == 'TextButton':
                new_item = LoadedTabPage.viewer.addTextItem(text = text,
                                                        textColor = textcolor,
                                                        BgColor = color,
                                                        scale = scale,
                                                        pos = pos )
                new_item.setPlainText(text)
                new_item.setBrush(QtGui.QBrush(color))  


            new_item.itemDict['script'] = script
            new_item.itemDict['object_list'] = object_list  

                                                      
                

    def keyPressEvent(self,event):
        #super(PickerUI,self).keyPressEvent(event)
        if(event.key() != QtCore.Qt.Key_Escape):
            try:
                QtWidgets.QDialog.keyPressEvent(event)
            except:pass
        else:
            pass
       

def run():
    """Open the picker and replace the previous instance."""
    global _picker_dialog
    try:
        _picker_dialog.close()
        _picker_dialog.deleteLater()
    except (NameError, RuntimeError):
        pass
    _picker_dialog = PickerUI(parent=maya_main_window())
    _picker_dialog.show()
    return _picker_dialog


