#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import re

from PySide2.QtWidgets import QFormLayout, QWidget, QLineEdit, QVBoxLayout, QPushButton, QMessageBox, QHBoxLayout
from PySide2.QtCore import QObject


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
        # sh = os.path.join(pwd, "move_desktop.sh")
        # os.system("pkexec /bin/bash -x %s" % sh)
        os.system("pkexec --user root mv /tmp/entry-creator/*.desktop /usr/share/applications/")

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


class UiForm(QObject):
    def __init__(self, parent=QWidget):
        super(UiForm, self).__init__(parent)
        parent.setWindowTitle(self.tr("Desktop文件生成器"))
        parent.setFixedSize(300, 500)

        self.layout_root = QVBoxLayout(parent)
        self.layout_form = QFormLayout()
        self.layout_root.addLayout(self.layout_form)

        self.executable_file = QLineEdit()
        self.executable_file.setPlaceholderText(self.tr("输入可执行文件路径或直接拖入"))  # 注意处理拖入多个文件的情况

        self.name = QLineEdit()
        self.name.setPlaceholderText(self.tr("应用名称"))

        self.icon = QLineEdit()
        self.icon.setPlaceholderText(self.tr("可选"))

        self.layout_form.addRow(self.tr("程序"), self.executable_file)
        self.layout_form.addRow(self.tr("图标"), self.icon)
        self.layout_form.addRow(self.tr("名称"), self.name)

        self.generate = QPushButton(self.tr("生成"))
        self.layout_root.addWidget(self.generate)


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
