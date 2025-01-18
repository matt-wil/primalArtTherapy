import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QPushButton, QMessageBox, QDialog, QFormLayout, QLineEdit, QDialogButtonBox
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from database_manager import DatabaseManager, Client

icon_path = "path"
colors = {
    "Blue": "#134B42",
    "Gold": "#EEA83B",
    "Tan": "#CA763B"
}


class NewClientDialog(QDialog):
    def __init__(self, database_manager, parent=None):
        super().__init__(parent)
        self.setWindownTitle("Add New Client")
        self.database_manager = database_manager
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        # input fields
        self.name_input = QLineEdit(self)
        self.email_input = QLineEdit(self)
        layout.addRow("Name:", self.name_input)
        layout.addRow("Email:", self.email_input)

        # Dialog buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def accept(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()

        if not name or not email:
            QMessageBox.warning(self, "Input Error", f"Client: {self.name} Email: {self.email} added successfully!")
            return

        try:
            self.database_manager.add_client(name, email)
            QMessageBox.information(self, "Success", "Client added successfully!")
        except RuntimeError as e:
            QMessageBox.critical(self, "Error", str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Primal Art Therapy")
        # Dimensions
        screen = QApplication.primaryScreen()
        screen_width, screen_height = screen.size().width(), screen.size().height()

        window_width = int(screen_width * 0.7)
        window_height = int(screen_height * 0.6)

        self.setGeometry(100, 100, window_width, window_height)
        self.setWindowIcon(QIcon(icon_path))

        self.database_manager = DatabaseManager("sqlite:///pat_clients.db")

        self.init_ui()

    def init_ui(self):
        # create central widget
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Heading
        self._heading_label(layout)

        # Start button
        self._start_button(layout)

    def _heading_label(self, layout):
        # Heading Label
        label = QLabel("Primal Art Therapy \nDatabase Manager", self)
        label.setFont(QFont("Helvetica", 50))
        label.setGeometry(0, 0, 600, 400)
        label.setStyleSheet(
            f"color: {colors['Gold']};"
            "font-weight: bold;"
            "font-style: italic;"
        )
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

    def _start_button(self, layout):
        self.button = QPushButton("Start", self)
        self.button.clicked.connect(self._button_on_click)
        layout.addWidget(self.button, alignment=Qt.AlignCenter)

    def _add_client_button(self, layout):
        self.add_client_button = QPushButton("Add Client", self)
        self.add_client_button.clicked.connect(self._open_new_client_dialog)
        layout.addWidget(self.add_client_button, alignment=Qt.AlignCenter)

    def _button_on_click(self):
        QMessageBox.information(self, "Button Clicked", "Database initialized and ready!")

    def _open_new_client_dialog(self):
        dialog = NewClientDialog(self.database_manager, self)
        dialog.exec_()

    def _menu(self):
        """Opens the Page to the Main Menu"""
        pass


def main():
    app = QApplication(sys.argv)  # allows CLI args
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
