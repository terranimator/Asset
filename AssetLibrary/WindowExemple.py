from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as om

def maya_main_window():
    main_window_ptr = om.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class TestDialog(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(TestDialog, self).__init__(parent)
        
        self.setWindowTitle("teste")
        self.setMinimumWidth(200)     
        self.setWindowFlags(self.windowFlags()^QtCore.Qt.WindowContextHelpButtonHint)
        
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        
    def create_widgets(self):
        self.lineedit = QtWidgets.QLineEdit()
        self.checkBox1 = QtWidgets.QCheckBox("check 0w")
        self.checkBox2 = QtWidgets.QCheckBox("check 02")
        self.bnt_ok = QtWidgets.QPushButton("ok")
        self.bnt_cancel = QtWidgets.QPushButton("cancel")
        
    def create_layout(self):
        bnt_layout = QtWidgets.QHBoxLayout()
        bnt_layout.addStretch()
        bnt_layout.addWidget(self.bnt_ok)
        bnt_layout.addWidget(self.bnt_cancel)
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Name:", self.lineedit)
        form_layout.addRow("Hidden:", self.checkBox1)
        form_layout.addRow("Locked:", self.checkBox2)
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(bnt_layout)

    def create_connections(self):
        self.bnt_cancel.clicked.connect(self.close)
        self.lineedit.textChanged.connect(self.print_name)
        self.checkBox1.toggled.connect(self.print_is_hidden)   

    def print_name(self, name):
        #name = self.lineedit.text()
        print name

    def print_is_hidden(self):
        hidden = self.checkBox1.isChecked()
        if hidden:
            print "Hidden"
        else:
            print "Visible"         


if __name__ == "__main__":
    
    
    try:
        test_dialog.close()
        test_dialog.deleteLater()
    except:
        pass
        
    test_dialog  = TestDialog()
    test_dialog.show()
