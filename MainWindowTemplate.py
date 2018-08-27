from PyQt5.QtWidgets import QFormLayout, QWidget, QLineEdit, QVBoxLayout, QPushButton
from PyQt5.QtCore import QObject


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

        self.icon = QLineEdit()
        self.icon.setPlaceholderText(self.tr("可选"))

        self.name = QLineEdit()
        self.name.setPlaceholderText(self.tr("应用名称"))

        self.layout_form.addRow(self.tr("程序"), self.executable_file)
        self.layout_form.addRow(self.tr("图标"), self.icon)
        self.layout_form.addRow(self.tr("名称"), self.name)

        self.generate = QPushButton(self.tr("生成"))
        self.layout_root.addWidget(self.generate)
