from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from ..classes import ConfigurableObject
from . import main_ui
import sys
from typing import Dict


class SettingsTab(object):
    def __init__(self, parent, tab_name, types_list, obj_list: Dict[str, ConfigurableObject]):
        self.parent = parent
        self.tab_name = tab_name
        self.types_list = types_list
        self.obj_list = obj_list

        self.activated = None
        self.currentTree = None
        self.currentParams = None
        self.currentParamsTree = None
        # self.activated = []

    def _on_item_clicked(self, item):
        t = item.text()
        if self.activated is not None:
            self.gridLayout_2.removeWidget(self.currentTree)
            self.currentTree.deleteLater()
            self.currentTree = None
            self.currentParams = None
            self.currentParamsTree = None
            self.activated = None

        if t != self.activated:
            var = self.obj_list[t]

            self.currentParamsTree = []
            for i, v in var.config_vars.items():
                self.currentParamsTree.append({
                    'name': i,
                    'type': v.__class__.__name__,
                    'value': v
                })

            self.currentParams = Parameter.create(name='params', type='group', children=self.currentParamsTree)
            self.currentTree = ParameterTree(self.tab)
            self.currentTree.setParameters(self.currentParams, showTop=False)
            self.gridLayout_2.addWidget(self.currentTree, 0, 1, 1, 1)

            self.activated = t
            print(f"Activating {t}")

    def setupData(self):
        for i in self.obj_list.values():
            self.listWidget.addItem(i.short())

    def setupUi(self):
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName(f"tab_{self.tab_name}")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName(f"gridLayout_{self.tab_name}")

        self.listWidget = QtWidgets.QListWidget(self.tab)
        self.listWidget.setObjectName(f"listWidget_{self.tab_name}")
        self.listWidget.itemClicked.connect(self._on_item_clicked)

        self.gridLayout_2.addWidget(self.listWidget, 0, 0, 1, 1)

        self.parent.tabWidget.addTab(self.tab, "")
        self.retranslateUi()
        print(f"{self.tab_name} tab created")

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.parent.tabWidget.setTabText(self.parent.tabWidget.indexOf(self.tab), _translate("MainWindow", f"Tab {self.tab_name}"))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = main_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.tabs = []

    def load_tab(self, tab_name, types_list, obj_list):
        tab = SettingsTab(self.ui, tab_name, types_list, obj_list)
        tab.setupUi()
        tab.setupData()
        self.tabs.append(tab)
        # self.tabWidget.setCurrentIndex(1)
