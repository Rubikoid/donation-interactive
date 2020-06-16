import random
import sys
import string
from typing import Dict

from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

from ..classes import ConfigurableObject
from . import main_ui


class ArrayGroup(pTypes.GroupParameter):
    def __init__(self, add_type: str, **opts):
        opts['type'] = 'group'
        opts['addText'] = "Add"
        self.add_type = add_type
        pTypes.GroupParameter.__init__(self, **opts)

    def rebuildID(self):
        for i, v in enumerate(self.children()):
            v.setName(f"{i}")

    def addNew(self):
        val = {
            'str': '',
            'float': 0.0,
            'int': 0
        }[self.add_type]
        next_id = int(self.childs[-1].name()) + 1
        self.addChild(dict(name=f"{next_id}", type=self.add_type, value=val, removable=True, renamable=False))


class SettingsTab(object):
    def __init__(self, parent, tab_name: str, types_list: Dict[str, object], obj_list: Dict[str, ConfigurableObject]):
        self.parent = parent
        self.tab_name = tab_name
        self.types_list = types_list
        self.obj_list = obj_list

        self.activated = None
        self.currentTree = None
        self.currentParams = None
        self.currentParamsTree = None
        # self.activated = []

    def _on_parametr_change(self, param, changes):
        print("tree changes:")
        for param, change, data in changes:
            path = self.currentParams.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()
            print(f'  parameter: {childName}')
            print(f'  change:    {change}')
            print(f'  data:      {data}, {type(data)}')
            print('  ----------')

            conf = self.obj_list[self.activated].config_vars
            if change == "value":
                if "." not in childName:
                    conf[childName] = data
                else:
                    conf[path[0]][int(path[1])] = data
            elif change == "childAdded":
                conf[path[0]].append(data[0].value())
            elif change == "childRemoved":
                del conf[path[0]][int(data.name())]
                for i in self.currentParamsTree:
                    if isinstance(i, ArrayGroup) and i.name() == path[0]:  # WTF: crazy shit, fix this
                        i.rebuildID()
                print(f"Internal state: {conf[path[0]]}")

    def _on_item_clicked(self, item):
        t = item.text()

        if t != self.activated:
            var = self.obj_list[t]

            self.currentParamsTree = []
            for i, v in var.config_vars.items():
                if isinstance(v, list):
                    self.currentParamsTree.append(
                        ArrayGroup(add_type=v[0].__class__.__name__, name=i, children=[
                            {
                                'name': str(j),
                                'type': k.__class__.__name__,
                                'value': k,
                                'removable': True,
                                'renamable': False
                            } for j, k in enumerate(v)
                        ])
                    )
                else:
                    self.currentParamsTree.append({
                        'name': i,
                        'type': v.__class__.__name__,
                        'value': v
                    })

            self.currentParams = Parameter.create(name='params', type='group', children=self.currentParamsTree)
            self.currentParams.sigTreeStateChanged.connect(self._on_parametr_change)
            self.currentTree = ParameterTree(self.tab)
            self.currentTree.setParameters(self.currentParams, showTop=False)
            self.gridLayout.addWidget(self.currentTree, 0, 1, 4, 1)

            self.activated = t
            print(f"Activating {t}")

    def _on_new_item_create(self):
        item = self.classSelector.currentText()
        cl: ConfigurableObject = self.types_list[item](lambda x: None)
        cl.config_vars["name"] = f"{cl.config_vars['type']}.{''.join(random.sample(string.hexdigits, 8))}"
        self.obj_list[cl.short()] = cl
        self.listWidget.addItem(cl.short())
        print(f"Creating {item}")

    def _on_item_remove(self):
        self.clearActivation()
        item = self.listWidget.currentItem()
        del self.obj_list[item.text()]
        self.listWidget.takeItem(self.listWidget.currentRow())

    def clearActivation(self):
        if self.activated is not None:
            self.gridLayout.removeWidget(self.currentTree)
            self.currentTree.deleteLater()
            self.currentTree = None
            self.currentParams = None
            self.currentParamsTree = None
            self.activated = None

    def setupData(self):
        for i in self.obj_list.values():
            self.listWidget.addItem(i.short())

        for i in self.types_list:
            self.classSelector.addItem(i)

    def setupUi(self):
        # entire tab
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName(f"tab_{self.tab_name}")

        # grid
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setObjectName(f"gridLayout_{self.tab_name}")

        # list with things
        self.listWidget = QtWidgets.QListWidget(self.tab)
        self.listWidget.setObjectName(f"listWidget_{self.tab_name}")
        self.listWidget.itemClicked.connect(self._on_item_clicked)

        # class selector for adding new items
        self.classSelector = QtWidgets.QComboBox(self.tab)
        self.classSelector.setObjectName("classSelector")

        # add button
        self.addButton = QtWidgets.QPushButton(self.tab)
        self.addButton.setObjectName("addButton")
        self.addButton.clicked.connect(self._on_new_item_create)

        # remove button
        self.removeButton = QtWidgets.QPushButton(self.tab)
        self.removeButton.setObjectName("removeButton")
        self.removeButton.clicked.connect(self._on_item_remove)

        # add everything to grid
        self.gridLayout.addWidget(self.classSelector, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.addButton, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.removeButton, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.listWidget, 3, 0, 1, 1)

        # add tab to form
        self.parent.tabWidget.addTab(self.tab, "")
        self.retranslateUi()
        print(f"{self.tab_name} tab created")

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.parent.tabWidget.setTabText(self.parent.tabWidget.indexOf(self.tab), _translate("MainWindow", f"Tab {self.tab_name}"))
        self.addButton.setText(_translate("MainWindow", f"Add {self.tab_name}"))
        self.removeButton.setText(_translate("MainWindow", f"Remove {self.tab_name}"))


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
