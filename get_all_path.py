# _*_ coding:<utf-8> _*_

import os
import re
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QTreeWidget, QTreeWidgetItem, QLabel, QHBoxLayout


def get_son_path_list():
    path = os.path.abspath('.') #获取当前工作目录路径
    path_list = []              #初始化一个list
    for home, dirs, files in os.walk(path):
        path_list.append(home)
        path_list.append(files)
    return path_list

class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.resize(500, 300)                     # 1
        self.tree = QTreeWidget(self)                           # 2
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['Item', 'Path'])
        #self.tree.itemClicked.connect(self.change_func)#点击触发槽函数

        self._1stlevel = []
        self._2stlevel = []
        self._3stlevel = []
        self._4stlevel = []
        self._5stlevel = []
        self._6stlevel = []


        self.tree.expandAll()
        self.h_layout = QHBoxLayout()#页面布局
        self.h_layout.addWidget(self.tree)
#        self.h_layout.addWidget(self.label)
        self.setLayout(self.h_layout)

    def tree_process(self, path_list):
        path_root = path_list[0]
        self._1stlevel = QTreeWidgetItem(self.tree)
        first_item = path_root.split('\\')               # 3
        self._1stlevel.setText(0, first_item[-1])
        self._1stlevel.setCheckState(0, Qt.Unchecked)
        self._1stlevel.setText(1, path_root)
        #显示根目录下文件
        if path_list[1] != []:
            for files in path_list[1]:
                item = QTreeWidgetItem(self._1stlevel)
                item.setText(0, files)

        for item_tmp in path_list[2::2]:
            folder = item_tmp.split('\\')               
            if folder.__len__ > first_item.__len__:
                self._2stlevel = QTreeWidgetItem()
                self._2stlevel.setText(0, folder[-1])
                self._2stlevel.setText(1, item_tmp)
                self._2stlevel.setCheckState(0, Qt.Unchecked)
                self._1stlevel.addChild(self._2stlevel)


 #               QTreeWidgetItem().setText(0, item - path_list[0])
 #               QTreeWidgetItem().setText(1, item)







if __name__ =="__main__":
    dislist = ['macOS', 'Android x86', 'Android ARMv7', 'Sources', 'iOS']
    app = QApplication(sys.argv)
    AaaAa = get_son_path_list()
    for ite in AaaAa:
        print(ite)
    demo = Demo()
    demo.tree_process(AaaAa)
    demo.show()
    sys.exit(app.exec_())


 











