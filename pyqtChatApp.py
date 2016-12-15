#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-08 10:56:55
# @Author  : He Liang (helianghit@foxmail.com)
# @Link    : https://github.com/HeLiangHIT

import os,sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from groupUserList import GroupUserList
from msgList import MsgList
from flowlayout import FlowLayout

DEFAULT_HEAD = 'icons/qq.png'


class TextEdit(QTextEdit,QObject):
    '''支持ctrl+return信号发射的QTextEdit'''
    entered = pyqtSignal()
    def __init__(self, parent = None):
        super(TextEdit, self).__init__(parent)
    
    def keyPressEvent(self,e):
        # print e.key() == Qt.Key_Return,e.key() == Qt.Key_Enter, e.modifiers() == Qt.ControlModifier
        if (e.key() == Qt.Key_Return) and (e.modifiers() == Qt.ControlModifier):
            self.entered.emit()# ctrl+return 输入
            self.clear()
        super(TextEdit,self).keyPressEvent(e)


'''
"QPushButton{background-color:black;color: white;border-radius: 10px;border: 2px groove gray;border-style: outset;}"
"QPushButton:hover{background-color:white; color: black;}"
"QPushButton:pressed{background-color:rgb(85, 170, 255);border-style: inset;}"
'''
class MsgInput(QWidget,QObject):
    '''自定义的内容输入控件，支持图像和文字的输入，文字输入按回车确认。'''
    textEntered = pyqtSignal(str)
    imgEntered = pyqtSignal(str)

    btnSize = 35
    teditHeight = 200
    def __init__(self,parent = None):
        super(MsgInput, self).__init__(parent)
        self.setContentsMargins(3,3,3,3)

        self.textEdit = TextEdit()
        self.textEdit.setMaximumHeight(self.teditHeight)
        self.setMaximumHeight(self.teditHeight+self.btnSize)
        self.textEdit.setFont(QFont("Times",20,QFont.Normal))
        self.textEdit.entered.connect(self.sendText)

        sendImg = QPushButton()
        sendImg.setStyleSheet("QPushButton{border-image:url(icons/img.png);}"#这个参数可以让图片随大小缩放
             "QPushButton:hover{border: 2px groove blue;}"
             "QPushButton:pressed{border-style: inset;}")
        sendImg.setFixedSize(self.btnSize,self.btnSize)
        sendImg.clicked.connect(self.sendImage)

        sendTxt = QPushButton(u'发送')
        sendTxt.setFont(QFont("Microsoft YaHei",15,QFont.Bold))
        sendTxt.setFixedHeight(self.btnSize)
        sendTxt.clicked.connect(self.sendText)

        hl = FlowLayout()
        hl.addWidget(sendImg)
        hl.addWidget(sendTxt)
        hl.setMargin(0)

        vl = QVBoxLayout()
        vl.addLayout(hl)
        vl.addWidget(self.textEdit)
        vl.setMargin(0)
        self.setLayout(vl)
    def sendImage(self):#选择图像发送
        dialog = QFileDialog(self,u'请选择图像文件...')
        dialog.setDirectory(os.getcwd() + '/ref') #设置默认路径
        dialog.setNameFilter(u"图片文件(*.png *.jpg *.bmp *.ico);;")#中间一定要用两个分号才行！
        if dialog.exec_():
            selectFileName = unicode(dialog.selectedFiles()[0])
            self.imgEntered.emit(selectFileName)
        else:#放弃选择
            pass
    def sendText(self):
        txt = self.textEdit.toPlainText()
        if len(txt)>0:
            self.textEntered.emit(txt)


class PyqtChatApp(QSplitter):
    """聊天界面，QSplitter用于让界面可以鼠标拖动调节"""
    curUser = {'id':None,'name':None,'head':DEFAULT_HEAD}
    selfHead = DEFAULT_HEAD
    def __init__(self):
        super(PyqtChatApp, self).__init__(Qt.Horizontal)

        self.setWindowTitle('pyChat') # window标题
        self.setWindowIcon(QIcon('icons/chat.png')) #ICON
        self.setMinimumSize(500,500) # 窗口最小大小

        self.ursList = GroupUserList()
        self.ursList.setMaximumWidth(250)
        self.ursList.setMinimumWidth(180)
        self.ursList.itemDoubleClicked.connect(self.setChatUser)
        self.msgList = MsgList()
        self.msgList.setDisabled(True) #刚打开时没有聊天显示内容才对
        self.msgInput = MsgInput()
        self.msgInput.textEntered.connect(self.sendTextMsg)
        self.msgInput.imgEntered.connect(self.sengImgMsg)
        
        self.ursList.setParent(self)
        rSpliter = QSplitter(Qt.Vertical, self)
        self.msgList.setParent(rSpliter)
        self.msgInput.setParent(rSpliter)

        self.setDemoUser() #模拟添加用户

    def setDemoMsg(self):
        self.msgList.clear()
        self.msgList.addTextMsg("Hello",True,self.curUser['head'])
        self.msgList.addTextMsg("World!",False,self.selfHead)
        self.msgList.addTextMsg(u"昨夜小楼又东风，春心泛秋意上心头，恰似故人远来载乡愁，今夜月稀掩朦胧，低声叹呢喃望星空，恰似回首终究一场梦，轻轻叹哀怨...",True,self.curUser['head'])
        self.msgList.addTextMsg(u"With a gentle look on her face, she paused and said,她脸上带着温柔的表情，稍稍停顿了一下，便开始讲话",False,self.selfHead)
        self.msgList.addImageMsg('ref/bq.gif',True,self.curUser['head'])
        self.msgList.addImageMsg('ref/mt.gif',False,self.selfHead)
    def setDemoUser(self):
        self.ursList.clear()
        self.ursList.addUser('hello')
        self.ursList.addUser('world')
        self.ursList.addGroup('group')
        self.ursList.addUser('HeLiang',group = 'group')
        self.ursList.addGroup(u'中文')
        self.ursList.addUser(u'何亮',group = u'中文',head = 'icons/hd_1.png')

    @pyqtSlot(str)
    def sendTextMsg(self,txt):
        txt = unicode(txt)
        self.msgList.addTextMsg(txt,False)
    @pyqtSlot(str)
    def sengImgMsg(self,img):
        img = unicode(img)
        self.msgList.addImageMsg(img,False)
    @pyqtSlot(QListWidgetItem)
    def setChatUser(self,item):
        (self.curUser['id'],self.curUser['name'],self.curUser['head']) = (item.getId(),item.getName(),item.getHead())
        self.msgList.setDisabled(False)
        self.setWindowTitle('pyChat: chating with %s...'% self.curUser['name'])
        self.setDemoMsg()


if __name__=='__main__':
    app = QApplication(sys.argv)
    pchat = PyqtChatApp()
    pchat.show()
    sys.exit(app.exec_())