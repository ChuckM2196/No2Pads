from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

import os, sys

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()
        self.editor = QPlainTextEdit() # Could also be QTextEdit, set self.editor.setAcceptRichText(False)
        self.setCentralWidget(self.editor)

        # Setup the QTextEdit editor configuration
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

        # self.path holds the path of the currently open file
        # If none, we haven't got a file open yet or creating new
        self.path = None

        layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # File Menu and ToolBar
        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&File")

        # Saving, Loading, and Print options on file menu
        open_file_action = QAction(QIcon(os.path.join('../icons/bonus/icons-24/mail-open.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('../icons/bonus/icons-24/disc-blue.png')), "Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(QIcon(os.path.join('../icons/bonus/icons-24/disk.png')), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction(QIcon(os.path.join('../icons/bonus/icons-24/printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        # Edit Menu and ToolBar
        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(edit_toolbar)
        edit_menu = self.menuBar().addMenu("&Edit")

        # Edit Commands

        # Cut
        cut_action = QAction(QIcon(os.path.join('../icons/bonus/icons-24/scissors.png')), "Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        # Copy
        copy_action = QAction(QIcon(os.path.join('../icons/bonus/icons-32/document.png')), "Copy", self)
        copy_action.setStatusTip("copy selected text")
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        # Paste
        paste_action = QAction(QIcon(os.path.join('../icons/bonus/icons-24/stamp.png')), 'Paste', self)
        paste_action.setStatusTip("Paste selected text")
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        # Select
        select_action = QAction(QIcon(os.path.join('../icons/bonus/icons-24/blue-document-text-image.png')), 'Select', self)
        select_action.setStatusTip("Select all text")
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)


        # File Operations

        # Open
    def file_open(self):
            path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text documents (*.txt);All files (*.*) ")

            if path:
                try:
                    with open(path, 'rU') as f:
                        text = f.read()

                except Exception as e:
                    self.dialog_critical(str(e))


                else:
                    self.path = path
                    self.editor.setPlainText(text)
                    self.update_title()

         # Save
    def file_save(self):
        if self.path is None:
          # If we do not have a path, we need to use save as
            return self.file_saveas()

        self._save_to_path(self.path)

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Documents (*.txt);All files (*.*)")
        if not path:
            # The dialog is cancelled will return ''
            return ''

        self._save_to_path(self.path)

        def _save_to_path(self, path):
            text = self.editor.toPlainText()
            try:
                with open(path, 'w') as f:
                    f.write(text)

            except Exception as e:
                self.dialog_critical(str(e))

            else: self.path = path
            self.update_title()

        # Printing
    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('No2Pads')

    window = MainWindow()
    window.show()
    app.exec_()