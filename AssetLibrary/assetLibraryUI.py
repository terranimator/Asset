from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from PySide2 import QtGui
import json
import os

import maya.OpenMayaUI as omui
import maya.cmds as cmds

def maya_main_window():
    """
    Return the Maya main window widget as python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)
    
class OpenImportDialog(QtWidgets.QWidget):

    TEST_DIC =["a", "b", "c"]
    DEFAULT_DIRECTORY = r"C:\Users\terra\Documents"
    list =  {'vehicle': [], 'tree': ['icon01.ma', 'icon02.ma', 'icon03.ma'], 'rock': []}
    library_path = r"C:\Users\terra\Documents\library"

    def __init__(self, parent=maya_main_window()):
        super(OpenImportDialog, self).__init__(parent)
        self.library_path = None
        self.folders = None
        self.folders_number = None
        self.totalAssets = None
        self.index = {}
        self.search_filter = {}

        self.setWindowTitle("Asset Library")
        self.setMinimumSize(500, 300)
        self.setWindowFlags(QtCore.Qt.WindowType.Window)
        # call methods to create UI
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        # Library path Set
        self.library_path_lbl = QtWidgets.QLabel("NO PATH SET")
        self.directory_path_btn = QtWidgets.QPushButton()
        self.directory_path_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.directory_path_btn.setToolTip("Select File")

        self.filter_lbl = QtWidgets.QLabel("filter")
        self.filter_lineedit = QtWidgets.QLineEdit()
        self.filter_btn = QtWidgets.QPushButton()

    def create_layout(self):
        #Library Path Set
        self.path_layout = QtWidgets.QHBoxLayout()
        self.search_layout = QtWidgets.QHBoxLayout()
        #self.path_layout.addStretch()
        self.form_path_layout = QtWidgets.QFormLayout()
        self.form_path_layout.addRow("Library Path:", self.library_path_lbl)
        self.path_layout.addLayout(self.form_path_layout)
        self.path_layout.addWidget(self.directory_path_btn)

        self.search_layout.addWidget(self.filter_btn)
        self.form_filter_layout = QtWidgets.QFormLayout()
        self.form_filter_layout.addRow("Search Filter:", self.filter_lineedit)
        self.search_layout.addLayout(self.form_filter_layout)

        asset_list_wdg = QtWidgets.QWidget()
        self.asset_list_layout = QtWidgets.QGridLayout(asset_list_wdg)
        asset_list_scroll = QtWidgets.QScrollArea()
        asset_list_scroll.setWidgetResizable(True)
        asset_list_scroll.setWidget(asset_list_wdg)
          
        #main Layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(self.path_layout)
        main_layout.addLayout(self.search_layout)
        main_layout.addWidget(asset_list_scroll)

    def create_connections(self):
        self.directory_path_btn.clicked.connect(self.show_select_directory_dialog)
        self.filter_lineedit.textChanged.connect(self.asset_search_filter)
    
    def show_select_directory_dialog(self):
        directory_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Library Root", self.DEFAULT_DIRECTORY)
        if directory_path:
            self.library_path = directory_path
            self.library_path_lbl.setText(self.library_path)
            self.index_asset_library()

        else:
        	cmds.warning("path DOES NOT Exist!")

    def index_asset_library(self):
        dir = []
        for d in os.listdir(self.library_path):
            if os.path.isdir(self.library_path+"\\"+d):
                dir.append(d)
        self.folders  = dir
        self.folders_number = len(self.folders)
        print self.folders_number, "intems",  self.folders
        if self.library_path == None:
            cmds.warning("NO library was set, please use the - .setPath('libraryPath') - method to set a path for a library!")
            return None
        elif self.folders_number > 0:
            for folder in self.folders:
                files = []
                for f in os.listdir(self.library_path+"\\"+folder):
                    if f.lower().endswith((".ma")):
                        files.append(f)
                self.index[folder] = files
            f = open(self.library_path+"\\libraryIndex.json", "w+")
            json.dump(self.index, f,  ensure_ascii=False, indent=4)    
            f.close()
            self.add_assets_to_UI(assetList=self.index)
            return self.index
        else:
            cmds.warning("NO item to index!")
            return None

        


    def add_assets_to_UI(self, assetList=list, iconSize=75, column=3):
        for i in reversed(range(self.asset_list_layout.count())):
            self.asset_list_layout.itemAt(i).widget().deleteLater()

        row = 1
        count = 0
        self.asset_list_layout.setRowStretch(0,3)
        self.asset_list_layout.setColumnStretch(0,3)
        self.asset_list_layout.setColumnStretch(column+1,3)
        for d in assetList:
            for f in assetList[d]:
                col = count%column
                col += 1
                but = QPushButton()
                but.setFlat(True)
                lbl = QLabel(f.split(".")[0])
                lbl.setAlignment(Qt.AlignCenter)
                but.clicked.connect(lambda arg=d+"\\"+f: self.importAsset(arg))
                imagePath = self.library_path+"\\"+d+"\\"+f
                imagePath = imagePath.replace(".ma", ".png")
                imagePath = imagePath.replace("\\", "/")
                but.setIcon(QIcon(imagePath))
                but.setIconSize(QSize(iconSize,iconSize))
                self.asset_list_layout.addWidget(but, row, col)
                self.asset_list_layout.addWidget(lbl, row+1, col)
                if col == column:
                    row +=2
                count +=1
        self.asset_list_layout.setRowStretch(row,3)
        #self.asset_list_layout.addWidget(self.layout)
    
    def asset_search_filter(self, value):
        if value == "":
            self.search_filter = self.index
        else:
            self.search_filter = {}
        
            for folder in self.index:
                files = []
                for f in self.index[folder]:
                    for v in value.split(" "):
                        if v != "":
                            if v in f and f not in files:
                                files.append(f)
                    self.search_filter[folder] = files

            self.add_assets_to_UI(assetList=self.search_filter)







if __name__ == "__main__":

    try:
        openImportDialog.close()
        openImportDialog.deleteLater()
    except:
        pass

    openImportDialog = OpenImportDialog()
    openImportDialog.show()



