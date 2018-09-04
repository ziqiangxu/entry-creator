from PyQt5.QtWidgets import QWidget, QMessageBox
from MainWindowTemplate import UiForm
import os
import re


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = UiForm(self)
        self.signal_slot()

    def signal_slot(self):
        self.ui.generate.clicked.connect(self.on_generate_clicked)
        self.ui.executable_file.textChanged.connect(self.on_executable_file_changed)
        self.ui.icon.textChanged.connect(self.on_icon_changed)

    # slot
    def on_generate_clicked(self):
        executable_file = self.ui.executable_file.text()
        icon = self.ui.icon.text()
        name = self.ui.name.text()

        print(executable_file, icon)
        try:
            os.mkdir("/tmp/entry-creator/")
        except FileExistsError:
            pass
        desktop = os.path.expanduser("/tmp/entry-creator/%s.desktop" % name)
        f = open(desktop, "w")
        f.write("[Desktop Entry]\n"
                "Version=1.0\n"
                # "Categories=Dictionary;Application;Utility;\n"
                # "Comment=Nothing\n"
                "Encoding=UTF-8\n"
                "Exec=%s\n"
                "Icon=%s\n"
                "Name=%s\n"
                "StartupNotify=true\n"
                "Terminal=false\n"
                "Type=Application"
                % (executable_file, icon, name))
        f.close()
        if executable_file is "" or name is "":
            QMessageBox.warning(self, self.tr("警告"), self.tr("输入的数据不完整"),
                                QMessageBox.Ok, QMessageBox.Ok)
            return
        pwd = os.getcwd()
        sh = os.path.join(pwd, "move_desktop.sh")
        os.system("pkexec /bin/bash -x %s" % sh)

    # slot
    def on_executable_file_changed(self):
        line_edit = self.ui.executable_file
        text = line_edit.text()
        if re.match("file://", text):
            line_edit.setText(text[7:])
        name = os.path.basename(text)
        self.ui.name.setText(name)

    # slot
    def on_icon_changed(self):
        line_edit = self.ui.icon
        text = line_edit.text()
        if re.match("file://", text):
            line_edit.setText(text[7:])


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
