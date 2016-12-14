[TOC]


# 需求
1. 实现类似PC端微信的聊天消息界面。
2. 为了学习使用只需要显示图片和文本，支持GIF图像显示，支持消息右键的复制和删除。图片双击可以在expleror中显示。
3. 消息框需要模拟气泡效果，消息列表需要包含头像。

> 由于头像控件的操作和消息内容显示控件的操作差不多相似，因此就不再增加头像控件的右键和双击操作了。


# 实现思路
1. 参考[groupUserList](https://github.com/HeLiangHIT/pyqtChat)的实现方式，主要是在一个QListWidget上显示多个消息控件，主要区别是：
2. 消息不需要可以拖放、不需要右键增删改查，只需要列举显示即可，因此这里继承的QListWidget只编写了两个方法就是addImageMsg和addTextMsg，分别实现文本和图像消息的添加。
> 由于这里不需要增删改查功能，而只需要右键删除（和复制）因此直接把List实例和创建的QListWidgetItem实例传递保存到TextItem>BubbleText和ImageItem>BubbleImage自定义控件的实例里面---以便在消息的删除直接在里面调用List和ListItem实现删除`self.listView.takeItem(self.listView.indexFromItem(self.listItem).row())`。
3. 由于QListWidget默认鼠标滑过各个Item或者点击是都会产生不同的UI效果，而消息界面不需要这样的效果故参考[乌托邦大神的博客](http://blog.csdn.net/taiyang1987912/article/details/40979309)设置item的样式如下（为了让item不可选在addItem之后将其设置为不可选择状态it.setFlags(Qt.ItemIsEnabled)）：
```
setStyleSheet(
    "QListWidget::item{border:0px solid gray;background-color:transparent;padding:0px;color:transparent}"  
    "QListView::item:!enabled{background-color:transparent;color:transparent;border:0px solid gray;padding:0px 0px 0px 0px;}"  
    "QListWidget::item:hover{background-color:transparent;color:transparent;border:0px solid gray;padding:0px 0px 0px 0px;}"  
    "QListWidget::item:selected{background-color:transparent;color:transparent;border:0px solid gray;padding:0px 0px 0px 0px;}")
```
4. 在消息和图像显示的自定义控件Item中使用一个QHBoxLayout显示消息，主要就是根据消息的左右来调整不同的添加控件顺序，采用QSpacerItem控制空白区域的自动缩放，该方案主要参考[stackoverflow](http://stackoverflow.com/questions/18047427/pyqt-sms-bubble-widget)上的方案。
5. 绘制气泡消息图像的控件BubbleImage为了支持GIF显示，采用一个QMovie类，将其frameChanged信号连接到自定义槽animate里面通过`self.setPixmap(self.movie.currentPixmap())`实现图片的动态更新。
6. **气泡的绘制**主要是限制其绘制区域，使用QPainter的drawPolygon绘制，drawPolygon的输入采用QPolygonF添加气泡的边角点路径，详细实现参考其paintEvent方法。为了保证鼠标在内部和在外部时有不同的颜色（主要是鼠标移入时颜色加深），需要在enterEvent和leaveEvent中设置不同的绘图颜色然后调用update刷新绘图。
> 为了让实现显示的图片不会在super(BubbleImage, self).paintEvent(e)时和绘制的背景气泡冲突，设置控件的setContentsMargins绘图范围保证图像的绘图区域。
7. **文字的显示**主要是控件的大小调节，起初准备用QTextEdit后来发现实现起来很难控制大小和混动条！只能舍弃次用QLabel继承实现了，关于控件的水平大小采用控制字符数量的方法(ヘ(_ _ヘ))，考虑到一个中文字符的宽度大概是3倍英文字符因此出现了checkContainChinese和splitStringByLen函数（我也不记得哪儿抄来的方法了）。在输入调用super(BubbleText, self).__init__(myText)前就把字符用\n分割好来显示。


# msgList 使用方法
<span id="UsingGuide"></span>
1. GroupUserList 控件继承到 QListWidget ，可以当作 QWidget 添加到界面布局，也可以被作为主界面操作。
2. 文字消息和图像消息的添加调用addTextMsg和addImageMsg即可。删除在界面上操作，查找暂未实现---估计这里也不会实现了。
3. 添加其它消息类型...等什么时候闲得没妹子约了再说吧...

项目地址：https://github.com/HeLiangHIT/pyqtChat
博客地址：http://blog.csdn.net/u010151698/article/details/53585124

