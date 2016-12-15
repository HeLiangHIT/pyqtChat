#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-08 10:56:55
# @Author  : He Liang (helianghit@foxmail.com)
# @Link    : https://github.com/HeLiangHIT

import os,sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

DEFAULT_GROUP = u'undefined'
DEFAULT_HEAD = u'icons/qq.png'
DEFAULT_USER = u'new user'
DEFAULT_NOTE = u'There is nothing to say...'



class LabelHead(QLabel):
    '''LabelHead(QLabel)  类主要是为了展示用户头像，
    但是在编辑用户头像的时候单击他要可以选择头像文件。
    因此增加了一个只读属性，当只读时单击不生效，可读时单击弹出图片选择框。'''
    def __init__(self,addr = DEFAULT_HEAD):
        super(LabelHead,self).__init__()
        self.setScaledContents(True)
        self.setReadOnly(True)
        self.setPicture(addr)

    def setReadOnly(self,b):
        self._readOnly = bool(b)

    def setPicture(self,addr):
        '''设置图像：继承至QLabel以便可以setPixmap设置图片'''
        self._picAddr = unicode(addr)
        img = QPixmap(addr)
        self.setPixmap(img)
        return True

    def getPicture(self):
        return self._picAddr

    def mousePressEvent(self,e):
        '''只读时屏蔽其鼠标点击事件'''
        if self._readOnly:
            e.ignore() #忽略鼠标点击，传递到父对象中
        else:
            dialog = QFileDialog(self,u'请选择头像文件...')
            dialog.setDirectory(os.getcwd() + '/icons') #设置默认路径
            dialog.setNameFilter(u"图片文件(*.png *.jpg *.bmp *.ico);;")#中间一定要用两个分号才行！
            if dialog.exec_():
                selectFileName = unicode(dialog.selectedFiles()[0])
                self.setPicture(selectFileName)
            else:
                pass
            e.accept() #此时禁止该事件往下传递


class LineEdit(QLineEdit):
    '''用户信息显示类：主要是支持可以编辑和不可以编辑'''
    def __init__(self,sz = None):
        super(LineEdit,self).__init__(unicode(sz))#父类输入文字内容
        self.setReadOnly(True)

    def setReadOnly(self,b):
        '''LineEdit(QLineEdit) 类主要是为了显示用户和组名称，
        因此在编辑用户和组名称时需要其为可以输入，其它时候为不可输入，
        因此继承到QLineEdit。通过其setStyleSheet设置只读和可读时的状态实现。'''
        if b:
            self._readOnly = True
            self.setStyleSheet("border-width:0;border-style:outset;background-color:rgba(0,0,0,0)")
        else:
            self._readOnly = False
            self.setStyleSheet("color:#000000")
        super(LineEdit,self).setReadOnly(self._readOnly)

    def contextMenuEvent(self,e):
        '''QLineEdit默认有右键菜单，因此为了让其在只读时不影响列表右键菜单操作，
        重写其contextMenuEvent，可写时调用父类的即可'''
        if self._readOnly:
            e.ignore() #忽略右键菜单
        else:
            super(LineEdit,self).contextMenuEvent(e)

    def mousePressEvent(self,e):
        '''屏蔽其鼠标点击事件'''
        if self._readOnly:
            e.ignore() #屏蔽所有鼠标操作
        else:
            super(LineEdit,self).mousePressEvent(e)

    def mouseDoubleClickEvent(self,e):
        '''鼠标双击选择事件： 双击选中全部内容可以用于ctrl+c复制'''
        if self._readOnly:
            self.setSelection(0,self.maxLength())#双击时选中，可以ctrl+c
            e.ignore() #屏蔽所有鼠标操作
        else:
            super(LineEdit,self).mouseDoubleClickEvent(e)

    def mouseMoveEvent(self,e):
        '''鼠标移动事件'''
        if self._readOnly:
            e.ignore() #屏蔽所有鼠标操作
        else:
            super(LineEdit,self).mouseMoveEvent(e)


class UserItem(QWidget):
    '''自定义的用户信息控件'''
    def __init__(self, listWidgetItem, usrId, **args):
        super(UserItem,self).__init__()

        self._listWidgetItem = listWidgetItem
        self._id = usrId

        self._headWidget = LabelHead()
        self._headWidget.setFixedSize(40, 40)
        self.setHead(args.get('head',DEFAULT_HEAD))
        
        self._nameWidget = LineEdit()
        self._nameWidget.setFont(QFont("Microsoft YaHei",10,QFont.Bold))
        self.setName(args.get('name',DEFAULT_USER))

        self._noteWidget = LineEdit()
        self.setNote(args.get('note',DEFAULT_NOTE))

        vbox = QVBoxLayout()
        vbox.addWidget(self._nameWidget)
        vbox.addWidget(self._noteWidget)
        vbox.addStretch()

        hbox = QHBoxLayout()
        hbox.addWidget(self._headWidget)
        hbox.addLayout(vbox)

        self.setLayout(hbox)

    def getListItem(self):
        return self._listWidgetItem

    def setName(self,name):
        self._name = unicode(name)
        self._nameWidget.setText('%s (%d)' %(self._name,self._id))
        self._nameWidget.setReadOnly(True)
    def getNameInput(self):
        return self._nameWidget.text()
    def getName(self):
        return self._name

    def setNote(self,note):
        self._note = unicode(note)
        self._noteWidget.setText(self._note)
        self._noteWidget.setReadOnly(True)
    def getNoteInput(self):
        return self._noteWidget.text()
    def getNote(self):
        return self._note

    def setHead(self,head):
        self._head = unicode(head)
        self._headWidget.setPicture(self._head)
        self._headWidget.setReadOnly(True)
    def getHead(self):
        return self._headWidget.getPicture()
    def getHeadInput(self):
        return self._headWidget.getPicture()
    
    def editInfo(self):#允许编辑用户信息
        self._nameWidget.setReadOnly(False)
        self._noteWidget.setReadOnly(False)
        self._headWidget.setReadOnly(False)
        self._nameWidget.setText(self._name)
        self._nameWidget.setFocus()

    def lockInfo(self):#锁定用户信息
        self._nameWidget.setReadOnly(True)
        self._noteWidget.setReadOnly(True)
        self._headWidget.setReadOnly(True)


    '''复写的父类方法'''
    def keyPressEvent(self,e):
        '''回车键确认输入内容'''
        if e.key() == Qt.Key_Return:
            self._listWidgetItem.confirmInput()

    def contextMenuEvent(self,e): 
        '''右键菜单'''
        editUser = QAction(QIcon('icons/edit.png'),u'修改',self)#第一个参数也可以给一个QIcon图标
        editUser.triggered.connect(self.editInfo)

        delUser = QAction(QIcon('icons/delete.png'),u'删除',self)
        delUser.triggered.connect(self._listWidgetItem.delSelfFromList)#选中就会触发

        menu = QMenu()
        menu.addAction(editUser)
        menu.addAction(delUser)
        menu.exec_(QCursor.pos())#全局位置比较好，使用e.pos()还得转换

        e.accept() #禁止弹出菜单事件传递到父控件中


    def mouseMoveEvent(self, e):
        '''鼠标移动下的右键按住才有效'''
        if e.buttons() != Qt.LeftButton:#右键按住
            return e.ignore()
        mimeData = QMimeData()#生成拖动数据
        drag = QDrag(self)#拖动对象
        drag.setMimeData(mimeData)#设置拖动数据
        drag.setHotSpot(e.pos() - self.rect().topLeft())#左上角位置
        dropAction = drag.start(Qt.MoveAction)#开始拖动
        e.accept()


class UserListItem(QListWidgetItem):
    '''用户信息列表控件'''
    def __init__(self, parent, usrId, name = DEFAULT_USER, 
            head = DEFAULT_HEAD, note = DEFAULT_NOTE, 
            group = DEFAULT_GROUP):
        super(UserListItem,self).__init__(name,None,QListWidgetItem.UserType)#parent给None才能正确的insertItem而不能addItem
        
        self._id = usrId
        self._group = unicode(group) #这两个参数放在本类，其它参数放到子类
        self._parent = parent
        self._widget = UserItem(self,usrId,name = name, head = head, note = note)
        self._widget.lockInfo()

        self.setTextColor(QColor(0x00,0x00,0x00,0x00))#设置控件文字为透明色以便不干扰控件的显示
        self.setSizeHint(self._widget.sizeHint())

    def getWidget(self):
        return self._widget
    def getId(self):
        return self._id

    def getId(self):
        return self._id

    def setGroup(self,group):
        self._group = unicode(group)
        self.setText(self._group + '_' + self.getNameInput())#同步更新一下
        print 'the group of user %s should be undated!'%self.getName()
    def getGroup(self):
        return self._group

    def setName(self,name):
        self._widget.setName(name)
        self.setText(self._group + '_' + name)#同步更新一下
    def getNameInput(self):
        return self._widget.getNameInput()
    def getName(self):
        return self._widget.getName()

    def setNote(self,note):
        self._widget.setNote(note)
    def getNoteInput(self):
        return self._widget.getNoteInput()
    def getNote(self):
        return self._widget.getNote()

    def setHead(self,head):
        self._widget.setHead(head)
    def getHeadInput(self):
        return self._widget.getHeadInput()
    def getHead(self):
        return self._widget.getHead()

    def confirmInput(self):#确认输入，一定要有输入才能确认输入
        self.setName(self.getNameInput())
        self.setNote(self.getNoteInput())
        self.setHead(self.getHeadInput())
        self._widget.lockInfo()

    def giveUpInput(self):#放弃输入
        self.setName(self.getName())
        self.setNote(self.getNote())
        self.setHead(self.getHead())
        self._widget.lockInfo()

    def delSelfFromList(self):
        self._parent.removeUserItem(self)

    '''以下为复写的父控件方法'''


class GroupItem(QWidget,QObject):
    """自定义的组信息控件"""
    expended = pyqtSignal(bool) #展开与否的信号
    def __init__(self, listWidgetItem, name = DEFAULT_GROUP):
        super(GroupItem, self).__init__()
        self.setAcceptDrops(True)#允许拖入

        self._listWidgetItem = listWidgetItem
        
        self._expendWidget = QPushButton()
        self._expendWidget.clicked.connect(self.toggleGroup)
        self._expendWidget.setFixedSize(10,10)
        self._isOpen = False
        self.toggleGroup() #设置为展开

        self._nameWidget = LineEdit()
        self._nameWidget.setFont(QFont("Times",10,QFont.Normal))
        self.setName(name)

        hbox = QHBoxLayout()
        hbox.addWidget(self._expendWidget)
        hbox.addWidget(self._nameWidget)
        hbox.addStretch()

        self.setLayout(hbox)
        

    def setName(self,name):
        self._name = unicode(name)
        self._nameWidget.setText('%s (%d)'%(name, len(self._listWidgetItem.usrList)))
        self._nameWidget.setReadOnly(True)
    def getNameInput(self):
        return self._nameWidget.text()
    def getName(self):
        return self._name

    def toggleGroup(self):#点击则展开和折叠
        self._isOpen = not self._isOpen
        if self._isOpen:
            self._expendWidget.setStyleSheet("border-image: url(icons/arrow_d.png);")
        else:
            self._expendWidget.setStyleSheet("border-image: url(icons/arrow_r.png);")
        self._expendWidget.update()#刷新该控件
        self.expended.emit(not self._isOpen)#发送信号，这里展开是不hidden，因此取非

    def editInfo(self):#允许编辑用户信息
        self._nameWidget.setReadOnly(False)
        self._nameWidget.setText(self._name)
        self._nameWidget.setFocus()

    def lockInfo(self):#锁定用户信息
        self._nameWidget.setReadOnly(True)

    '''复写的父类方法'''
    def keyPressEvent(self,e):#回车键确认输入内容
        if e.key() == Qt.Key_Return:
            self._listWidgetItem.confirmInput()

    def contextMenuEvent(self,e): #右键菜单
        adusr = QAction(QIcon('icons/user.png'),u'添加用户',self)
        adusr.triggered.connect(self._listWidgetItem.addNewUser)
        
        editGroup = QAction(QIcon('icons/edit.png'),u'修改',self)
        editGroup.triggered.connect(self.editInfo)

        delGroup = QAction(QIcon('icons/delete.png'),u'删除',self)
        delGroup.triggered.connect(self._listWidgetItem.delSelfFromList)#选中就会触发

        menu = QMenu()
        menu.addAction(adusr)
        menu.addAction(editGroup)
        menu.addAction(delGroup)
        menu.exec_(QCursor.pos())#全局位置比较好，使用e.pos()还得转换

        e.accept() #禁止弹出菜单事件传递到父控件中

    def dragEnterEvent(self, e):
        '''外部拖入事件允许，必须在这里accept后才能到dropEvent中确认放入！'''
        self._listWidgetItem.setSelected()
        e.accept()

    def dropEvent(self, e):#放入事件
        src = e.source() #获取目标控件
        srcUit = src.getListItem()
        self._listWidgetItem.moveUserIn(srcUit)
        e.accept()


class GroupListItem(QListWidgetItem):
    '''用户信息列表控件'''
    
    def __init__(self, parent, name = DEFAULT_GROUP):
        super(GroupListItem,self).__init__(name,None,QListWidgetItem.UserType)#parent给None才能正确的insertItem而不能addItem

        self.usrList = []# 组里面的用户列表，用到全局会是静态的
        self._parent = parent
        self._widget = GroupItem(self,name = name)
        self._widget.lockInfo()

        self.setTextColor(QColor(0x00,0x00,0x00,0x00))#设置控件文字为透明色以便不干扰控件的显示
        self.setSizeHint(self._widget.sizeHint())


    def getWidget(self):
        return self._widget

    def setName(self,name):
        self._widget.setName(name)
        self.setText(self.getName()) #同步更新
    def getNameInput(self):
        return self._widget.getNameInput()
    def getName(self):
        return self._widget.getName()


    def confirmInput(self):#确认输入
        self._parent.groupDict.pop(self.getName())#移除之前的Group键值对
        self.setName(self._widget.getNameInput())
        self._parent.groupDict[self.getName()] = self#添加当前名字的Group键值对
        self._widget.lockInfo()

    def giveUpInput(self):#放弃输入
        self.setName(self.getName())
        self._widget.lockInfo()

    def delSelfFromList(self):
        self._parent.removeGroupItem(self)

    @pyqtSlot()
    def addNewUser(self):
        (ok,uit,git) = self._parent.addUser(group = self.getName())#调用父类的添加用户，但是添加到本组下
        self._parent.setCurrentItem(uit)#选中当前增加的用户，这一步很关键。
        # 这样的另一个好处是执行一次item切换，保证之前输入的放弃操作--输入失焦。
        uit.getWidget().editInfo()#允许可以编辑

    def addUser(self,uit):
        self.usrList.append(uit)
        self._widget.expended.connect(uit.setHidden)
        self.setName(self.getName())#为了刷新显示用户数量

    def delUser(self, uit):
        self.usrList.pop(self.usrList.index(uit))
        self.setName(self.getName())#为了刷新显示用户数量

    def moveUserIn(self,uit):#调用父类的方法移动用户
        self._parent.moveUser(uit,self.getName())
    def setSelected(self):
        self._parent.setItemSelected(self,True)

    '''以下为复写的父控件方法'''





class GroupUserList(QListWidget):
    '''实现好友分组列表的效果'''
    groupDict = {}
    def __init__(self,parent = None):
        super(GroupUserList,self).__init__(parent)
        self.currentItemChanged.connect(self.chooseItemChanged)
        self.setAcceptDrops(True)

    def addGroup(self, name = DEFAULT_GROUP): 
        '''判断是否已存在并添加组'''
        name = unicode(name)
        groupNames = self.groupDict.keys()
        # print name, groupNames
        if name not in groupNames:#不存在则创建该keys
            git = GroupListItem(self,name)
            index = self.count() + 1
            self.insertItem(index,git)
            self.groupDict[name] = git #保存GroupItem对象到全局groupDict里面用于
            return (True, git) 
        else:
            git = self.groupDict[name]
            return (False, git)

    _currentId = 1 #用户ID从1递增
    def addUser(self, name = DEFAULT_USER, head = DEFAULT_HEAD,note = DEFAULT_NOTE,group = DEFAULT_GROUP,uId = None):
        '''添加用户'''
        (isExist, git) = self.addGroup(group)#判断组是否存在并增加组
        index = self.indexFromItem(git).row()#查找组存在的index

        if uId:#指定ID
            uId = int(uId)
            uit = UserListItem(self,uId,name,head,note,group)
        else:#未指定ID
            uit = UserListItem(self,self._currentId,name,head,note,group)
            self._currentId += 1 #ID依次增加，保证每个用户有一个唯一的标志符

        self.insertItem(index+1,uit)
        git.addUser(uit)
        # print uit.getName(),uit.getGroup(),uit.getId()
        return (True,uit,git)#返回增加的用户和其组

    def removeUserItem(self,uit):
        '''移除用户Item'''
        git = self.groupDict[uit.getGroup()]
        git.delUser(uit)#用户对应的组下的uit列表需要删除该用户
        self.takeItem(uit)
        del uit

    def removeGroupItem(self,git):
        '''移除组Item，其下的用户移动到默认分组'''
        gName = git.getName()
        if gName == DEFAULT_GROUP:
            print  "Group %s can't be deleted!"%(gName)
            return False
        for uit in git.usrList:
            self.addUser(name = uit.getName(),head = uit.getHead(),
                note = uit.getNote(),uId = uit.getId())#分组为默认
            self.takeItem(uit)
            # git.delUser(uit) #这样执行后usrList改变会导致for循环出错，最终都会少出git所以这里不用移除它就好了
            del uit

        self.takeItem(git)
        self.groupDict.pop(git.getName())
        del git

    def moveUser(self, uit, group = DEFAULT_GROUP):
        '''移动用户到组，就是原组中删除该用户，然后新组中添加该用户'''
        self.addUser(name = uit.getName(),head = uit.getHead(),
            note = uit.getNote(),uId = uit.getId(),group = group)#分组指定
        self.removeUserItem(uit)

    @pyqtSlot(QListWidgetItem,QListWidgetItem)#Item选择变化
    def chooseItemChanged(self,curit,preit):
        if preit:#存在则锁住，第一个点击的选项会不存在
            preit.giveUpInput() #放弃输入，因为没有单击回车确认输入
    _gIndex = 1 #组编号递增参数
    @pyqtSlot(bool)#右键增加组菜单
    def slotAddGroup(self,b):
        group = u'%s_%d'%(DEFAULT_GROUP,self._gIndex)
        self._gIndex += 1
        (ok,git) = self.addGroup(group)
        self.setCurrentItem(git)#选中当前增加的组，这一步很关键。
        # 这样的另一个好处是执行一次item切换，保证之前输入的放弃操作--输入失焦。
        git.getWidget().editInfo()#允许可以编辑
    @pyqtSlot(bool)#右键增加用户菜单
    def slotAddUser(self,b):
        (ok,uit,git) = self.addUser()#默认用户名信息就行了
        self.setCurrentItem(uit)#选中当前增加的用户，这一步很关键。
        # 这样的另一个好处是执行一次item切换，保证之前输入的放弃操作--输入失焦。
        uit.getWidget().editInfo()#允许可以编辑

    '''复写的父类方法'''
    def insertItem(self,index,it):
        super(GroupUserList,self).insertItem(index,it)
        if isinstance(it,GroupListItem) or isinstance(it,UserListItem):
            self.setItemWidget(it,it.getWidget())

    def takeItem(self,it):
        '''父类是根据index删除，不实用'''
        if isinstance(it,int):#父类兼容
            return super(GroupUserList,self).takeItem(index)
        else: #根据item删除，增加的功能
            index = self.indexFromItem(it).row()
            return super(GroupUserList,self).takeItem(index)

    def contextMenuEvent(self,e): 
        '''右键菜单'''
        adgrp = QAction(QIcon('icons/group.png'),u'增加组',self)#第一个参数也可以给一个QIcon图标
        adgrp.triggered.connect(self.slotAddGroup)

        adusr = QAction(QIcon('icons/user.png'),u'增加用户',self)
        adusr.triggered.connect(self.slotAddUser)#选中就会触发

        menu = QMenu()
        menu.addAction(adgrp)
        menu.addAction(adusr)
        menu.exec_(QCursor.pos())#全局位置比较好，使用e.pos()还得转换

        e.accept() #禁止弹出菜单事件传递到父控件中

    def dragEnterEvent(self, e):#外部拖入事件允许
        # print e.pos()#获取鼠标位置
        e.accept()
    def dragMoveEvent(self,e): #鼠标内部拖动事件
        # print e.pos()#获取鼠标位置
        e.accept()
    def dropEvent(self, e):#放入事件
        # print e.pos()
        e.accept()


if __name__=='__main__':
    app = QApplication(sys.argv)
    ul=GroupUserList()
    ul.setMinimumSize(200,500)

    ul.addUser('hello')
    ul.addUser('world')
    ul.addGroup('group')
    ul.addUser('HeLiang',group = 'group')
    ul.addGroup(u'中文')
    ul.addUser(u'何亮',group = u'中文')

    ul.show()
    sys.exit(app.exec_())