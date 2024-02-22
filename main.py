import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainMenu(QMainWindow):
    def __init__(self, file_dialog, parent=None):
        super(MainMenu, self).__init__(parent)
        self.file_dialog = file_dialog

        self.setGeometry(QDesktopWidget().screenGeometry().width()//2 - (QDesktopWidget().screenGeometry().width()//2)//2, QDesktopWidget().screenGeometry().height()//2 - (QDesktopWidget().screenGeometry().height()//2)//2, QDesktopWidget().screenGeometry().width()//2, QDesktopWidget().screenGeometry().height()//2)
        # self.showFullScreen()

        layout = QHBoxLayout()
        bar = self.menuBar()
        file = bar.addMenu("File")

        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        file.addAction(open_action)

        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        file.addAction(new_action)

        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        file.addAction(save_action)

        edit_action = file.addMenu("Edit")
        edit_action.addAction(QAction("Copy", self))
        edit_action.addAction(QAction("Paste", self))

        quit_action = QAction("Quit", self)
        file.addAction(quit_action)

        file.triggered[QAction].connect(self.process_tigger)
        self.setLayout(layout)
        self.setWindowTitle("Text Editor")

        self.current_filename = None

    def process_tigger(self, action):
        action_text = action.text()
        print(f'triggered {action_text}')

        if action_text == "Open":
            self.get_files()
        elif action_text == "Save":
            self.save_file()
        elif action_text == "New":
            self.new_file()
        elif action_text == "Copy":
            self.copy_to_clipboard()
        elif action_text == "Paste":
            self.paste_from_clipboard()
        elif action_text == "Quit":
            self.quit_program()

    def get_files(self):
        dlg = CustomDialog(self.file_dialog)
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            if filenames:
                self.file_dialog.current_filename = filenames[0]
                with open(self.file_dialog.current_filename, 'r') as file:
                    data = file.read()
                    self.file_dialog.contents.setReadOnly(False)
                    self.file_dialog.contents.setPlainText(data)

    def save_file(self):
        if self.file_dialog.current_filename:
            with open(self.file_dialog.current_filename, 'w') as file:
                file.write(self.file_dialog.contents.toPlainText())
                QMessageBox.information(self.file_dialog, "File Saved", "File has been saved.")
        else:
            QMessageBox.warning(self.file_dialog, "Save Error", "No file opened for saving.")

    def new_file(self):
        # Check if there are unsaved changes
        if self.file_dialog.contents.toPlainText() != '':
            result = QMessageBox.question(self.file_dialog, "Unsaved Changes",
                                          "Do you want to save changes before creating a new file?",
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if result == QMessageBox.Yes:
                self.save_file()
            elif result == QMessageBox.Cancel:
                return

        # Ask for a filename in a popup
        new_filename, ok = QInputDialog.getText(self.file_dialog, "New File", "Enter a filename:")

        if ok and new_filename:
            # Reset the current file information
            self.file_dialog.current_filename = new_filename
            self.file_dialog.contents.setReadOnly(False)

            # Save the new file to the file system
            with open(new_filename, 'w') as file:
                file.write(self.file_dialog.contents.toPlainText())

            # Open the new file
            with open(new_filename, 'r') as file:
                data = file.read()
                self.file_dialog.contents.setPlainText(data)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.file_dialog.contents.toPlainText())
        QMessageBox.information(self.file_dialog, "Text Copied", "Text has been copied to clipboard.")

    def paste_from_clipboard(self):
        clipboard = QApplication.clipboard()
        previous_text = self.file_dialog.contents.toPlainText()
        self.file_dialog.contents.setPlainText(previous_text + clipboard.text())

    def quit_program(self):
        # Check if there are unsaved changes
        if self.file_dialog.contents.toPlainText() != '':
            result = QMessageBox.question(self.file_dialog, "Unsaved Changes",
                                          "Do you want to save changes before quitting?",
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if result == QMessageBox.Yes:
                self.save_file()
            elif result == QMessageBox.Cancel:
                return

        sys.exit(0)


class CustomDialog(QFileDialog):
    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("HELLO!")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class FileDialog(QWidget):
    def __init__(self, parent=None):
        super(FileDialog, self).__init__(parent)

        layout = QVBoxLayout()

        self.contents = QTextEdit()
        self.contents.setReadOnly(True)
        layout.addWidget(self.contents)

        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    file_dialog = FileDialog()
    main_menu = MainMenu(file_dialog)
    main_menu.setCentralWidget(file_dialog)
    main_menu.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()