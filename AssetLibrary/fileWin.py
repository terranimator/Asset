from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds

def maya_main_window():
    """
    Return the Maya main window widget as python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)
    

class OpenImportDialog(QtWidgets.QDialog):

    FILE_FILTERS = "Maya(*.ma *.mb);;Maya ASCII (*.ma);; Maya Binary (*.mb);; ALL Files (*.*)"

    selected_fileter = "Maya (*.ma *.mb)"

    def __init__(self, parent=maya_main_window()):
        super(OpenImportDialog, self).__init__(parent)

        self.setWindowTitle("Open/Import/Reference")
        self.setMinimumSize(300, 80)
        self.setWindowFlags(self.windowFlags()^QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.filePath_le = QtWidgets.QLineEdit()
        self.select_file_bnt = QtWidgets.QPushButton()
        self.select_file_bnt.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.select_file_bnt.setToolTip("Select File")

        self.open_rb = QtWidgets.QRadioButton("open")
        self.open_rb.setChecked(True)
        self.import_rb = QtWidgets.QRadioButton("import")
        self.reference_rb = QtWidgets.QRadioButton("reference")
        self.force_cb = QtWidgets.QCheckBox("force")

        self.apply_btn = QtWidgets.QPushButton("Apply")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        file_path_layout = QtWidgets.QHBoxLayout()
        file_path_layout.addWidget(self.filePath_le)
        file_path_layout.addWidget(self.select_file_bnt)

        radio_btn_layout = QtWidgets.QHBoxLayout()
        radio_btn_layout.addWidget(self.open_rb)
        radio_btn_layout.addWidget(self.import_rb)
        radio_btn_layout.addWidget(self.reference_rb)

        form_path_layout = QtWidgets.QFormLayout()
        form_path_layout.addRow("File:", file_path_layout)
        form_path_layout.addRow("", radio_btn_layout)
        form_path_layout.addRow("", self.force_cb)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_path_layout)
        main_layout.addLayout(button_layout)



    def create_connections(self):
        self.select_file_bnt.clicked.connect(self.show_file_select_dialog)
        self.open_rb.toggled.connect(self.update_visibility)
        self.apply_btn.clicked.connect(self.load_file)
        self.close_btn.clicked.connect(self.close)

    def show_file_select_dialog(self):
        file_path, selected_filter = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", "", self.FILE_FILTERS, self.selected_fileter)
        if file_path:
            self.filePath_le.setText(file_path)

    def load_file(self):
        file_path = self.filePath_le.text()
        if not file_path:
            return
        file_info = QtCore.QFileInfo(file_path)
        if not file_info.exists():
            om.MGlobal.displayError("File does not existe " +file_path)
            return
            
        if self.open_rb.isChecked():
            self.open_file(file_path)
        elif self.import_rb.isChecked():
            self.import_file(file_path)
        else:
            self.reference_file(file_path)

    def open_file(self, file_path):
        force = self.force_cb.isChecked()

        if not force and cmds.file(q=True, modified=True):
             result = QtWidgets.QMessageBox.question(self, "Modified", "Current scene has unseved changes. Continue?")
             if result == QtWidgets.QMessageBox.StandardButton.Yes:
                 force = True
             else:
                return

        cmds.file(file_path, open=True, ignoreVersion=True, force=force)

    def import_file(self, file_path):
        cmds.file(file_path, i=True, ignoreVersion=True)

    def reference_file(self, file_path):
        cmds.file(file_path, reference=True, ignoreVersion=True)

    def update_visibility(self, checked):
        self.force_cb.setVisible(checked)




if __name__ == "__main__":

    try:
        openImportDialog.close()
        openImportDialog.deleteLater()
    except:
        pass

    openImportDialog = OpenImportDialog()
    openImportDialog.show()


