import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QPushButton,
    QMessageBox, QDialog, QFormLayout, QLineEdit, QDialogButtonBox,
    QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from database_manager import DatabaseManager

icon_path = "get a icon/logo to place the path in here and it will show on the top left of the Application Window"
colors = {
    "Blue": "#134B42",
    "Gold": "#EEA83B",
    "Tan": "#CA763B"
}


class UpdateClientDialog(QDialog):
    def __init__(self, database_manager, client, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Client")
        self.database_manager = database_manager
        self.client = client
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        # input fields
        self.first_name_input = QLineEdit(self.client.first_name, self)
        self.last_name_input = QLineEdit(self.client.last_name, self)
        self.email_input = QLineEdit(self.client.email, self)
        self.phone_input = QLineEdit(self.client.phone_number, self)
        self.address_input = QLineEdit(self.client.address, self)
        self.notes_input = QLineEdit(self.client.notes, self)
        self.receipts_input = QLineEdit(self.client.receipts, self)
        layout.addRow("Vorname:", self.first_name_input)
        layout.addRow("Nachname:", self.last_name_input)
        layout.addRow("E-Mail:", self.email_input)
        layout.addRow("Telefonnummer:", self.phone_input)
        layout.addRow("Adresse:", self.address_input)
        layout.addRow("Notizen:", self.notes_input)
        layout.addRow("Rechnungen:", self.receipts_input)

        # dialog buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def accept(self):
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        address = self.address_input.text().strip()
        notes = self.notes_input.text().strip()
        receipts = self.receipts_input.text().strip()

        if not first_name or not last_name or not email:
            QMessageBox.warning(self, "Input Error", "Please provide both name and email.")
            return
        try:
            self.database_manager.update_client(self.client.id, first_name, last_name, email, phone, address, notes, receipts)
            QMessageBox.information(self, "Success", "Client updated successfully!")
            super().accept()
        except RuntimeError as e:
            QMessageBox.critical(self, "Error", str(e))


class SearchClientDialog(QDialog):
    # search via client name, email, address
    def __init__(self, database_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Clienten Suchen")
        self.database_manager = database_manager
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        # input fields for search criteria
        self.name_input = QLineEdit(self)
        self.email_input = QLineEdit(self)
        self.phone_input = QLineEdit(self)
        layout.addRow("Name:", self.name_input)
        layout.addRow("E-Mail:", self.email_input)
        layout.addRow("Telefonnummer:", self.phone_input)

        # search button
        self.search_button = QPushButton("Suche", self)
        self.search_button.clicked.connect(self.perform_search)
        layout.addWidget(self.search_button)

        # table to display results
        self.results_table = QTableWidget(self)
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(["Vorname", "Nachname", "E-Mail", "Telefon", "Adresse"])
        layout.addWidget(self.results_table)

    def perform_search(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()

        try:
            results = self.database_manager.search_clients(name, email, phone)
            self.results_table.setRowCount(len(results))
            for row, client in enumerate(results):
                self.results_table.setItem(row, 0, QTableWidgetItem(client.first_name))
                self.results_table.setItem(row, 1, QTableWidgetItem(client.last_name))
                self.results_table.setItem(row, 2, QTableWidgetItem(client.email))
                self.results_table.setItem(row, 3, QTableWidgetItem(client.phone_number))
                self.results_table.setItem(row, 4, QTableWidgetItem(client.address))
        except RuntimeError as e:
            QMessageBox.critical(self, "Error", str(e))


class AddReceiptDialog(QDialog):
    def __init__(self, database_manager, client, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Add Receipt for {client.first_name} {client.last_name} Client ID: {client.id}")
        self.database_manager = database_manager
        self.client = client
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        # input fields
        self.receipt_number_input = QLineEdit(self)
        self.amount_input = QLineEdit(self)
        self.date_input = QLineEdit(self)
        layout.addRow("Receipt Number:", self.receipt_number_input)
        layout.addRow("Amount:", self.amount_input)
        layout.addRow("Date:", self.date_input)

        # dialog buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def accept(self):
        receipt_number = self.receipt_number_input.text().strip()
        amount = self.amount_input.text().strip()
        date = self.date_input.text().strip()

        if not receipt_number or not amount or not date:
            QMessageBox.warning(self, "Input Error", "All fields are required")
            return

        try:
            self.database_manager.add_receipt(self.client.id, receipt_number, amount, date)
            QMessageBox.information(self, "Success", "Receipt added successfully!")
            super().accept()
        except RuntimeError as e:
            QMessageBox.critical(self, "Error", str(e))


class NewClientDialog(QDialog):
    def __init__(self, database_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Neuen Clienten Hinzufügen")
        self.database_manager = database_manager
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        # input fields
        self.first_name_input = QLineEdit(self)
        self.last_name_input = QLineEdit(self)
        self.email_input = QLineEdit(self)
        self.phone_number = QLineEdit(self)
        self.address = QLineEdit(self)
        self.notes = QLineEdit(self)
        # requires a function to add receipts to a client.
        layout.addRow("Vorname:", self.first_name_input)
        layout.addRow("Nachname:", self.last_name_input)
        layout.addRow("E-Mail:", self.email_input)
        layout.addRow("Telefonnummer:", self.phone_number)
        layout.addRow("Wohnadresse:", self.address)
        layout.addRow("Notizen:", self.notes)

        # Dialog buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def accept(self):
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        email = self.email_input.text().strip()
        phone_number = self.phone_number.text().strip()
        address = self.address.text().strip()
        notes = self.notes.text().strip()

        if not first_name or not last_name or not email or not phone_number or not address:
            QMessageBox.warning(self, "Input Error", f"Client: {self.name} Email: {self.email} added successfully!")
            return

        try:
            self.database_manager.add_client(first_name, last_name, email, phone_number, address, notes)
            QMessageBox.information(self, "Success", "Client added successfully!")
        except RuntimeError as e:
            QMessageBox.critical(self, "Error", str(e))


class ViewClientsDialog(QDialog):
    def __init__(self, database_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("View Clients")
        self.database_manager = database_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # table widget to display clients
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Vorname", "Nachname", "E-Mail", "Adresse", "Telefonnummer", "Notizen"])
        layout.addWidget(self.table)

        # update and del buttons
        self.update_button = QPushButton("Update Selected Client", self)
        self.update_button.clicked.connect(self.update_selected_client)
        layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete Selected Client", self)
        self.delete_button.clicked.connect(self.delete_selected_client)
        layout.addWidget(self.delete_button)

        self.populate_table()

    def populate_table(self):
        try:
            clients = self.database_manager.get_all_clients()
            self.table.setRowCount(len(clients))

            for row, client in enumerate(clients):
                print(row, client.email)
                self.table.setItem(row, 0, QTableWidgetItem(client.first_name))
                self.table.setItem(row, 1, QTableWidgetItem(client.last_name))
                self.table.setItem(row, 2, QTableWidgetItem(client.email))
                self.table.setItem(row, 3, QTableWidgetItem(client.address))
                self.table.setItem(row, 4, QTableWidgetItem(client.phone_number))
                self.table.setItem(row, 5, QTableWidgetItem(client.notes or "empty"))

        except RuntimeError as e:
            QMessageBox.critical(self, "Error", str(e))

    def get_selected_client(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a client first")
            return None

        first_name = self.table.item(selected_row, 0).text()
        last_name = self.table.item(selected_row, 1).text()
        email = self.table.item(selected_row, 2).text()
        address = self.table.item(selected_row, 3).text()
        phone = self.table.item(selected_row, 4).text()
        notes = self.table.item(selected_row, 5).text()

        if not all([first_name, last_name, email, address, phone, notes]):
            QMessageBox.warning(self, "Selection Error", "One or more fields are missing for the selected client.")
            return None

        return self.database_manager.get_client_by_details(first_name, last_name, email, address, phone, notes)

    def update_selected_client(self):
        client = self.get_selected_client()
        if client:
            dialog = UpdateClientDialog(self.database_manager, client, self)
            if dialog.exec_():
                self.populate_table()

    def delete_selected_client(self):
        client = self.get_selected_client()
        if client:
            confirm = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete {client.first_name} {client.last_name}?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                try:
                    self.database_manager.delete_client(client.id)
                    QMessageBox.information(self, "Success", "Client deleted successfully!")
                    self.populate_table()
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

        # initialize db
        try:
            self.database_manager = DatabaseManager("sqlite:///PrimalArtDB.db")
            self.db_connected = True
        except Exception as e:
            self.db_connected = False
            QMessageBox.critical(self, "Database Error", f"Failed to connect to database: {e}")

        self.init_ui()

    def init_ui(self):
        # create central widget
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Heading
        self._heading_label(layout)

        # db connection status
        if self.db_connected:
            self.statusBar().setStyleSheet("color: #00ff00; font-style: italic;")
            self.statusBar().showMessage("Connected to Database")
        else:
            self.statusBar().setStyleSheet("color: #ff0000; font-style: italic;")
            self.statusBar().showMessage("Failed to Connect to Database")

        # Add client button
        self._add_client_button(layout)

        # View clients button
        self._view_clients_button(layout)

        # Search clients button
        self._search_clients_button(layout)

        self.setStyleSheet("""
            QPushButton{
                border-radius: 5px;
                background-color: #134B42;
                border: 3px solid;
                padding: 15px 50px;
         }
        """)

    def _heading_label(self, layout):
        # Heading Label
        label = QLabel("Primal Art Therapy", self)
        label.setFont(QFont("Helvetica", 100))
        label.setStyleSheet(
            f"color: {colors['Gold']};"
            "font-weight: bold;"
            "font-style: italic;"
        )
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

    def _add_client_button(self, layout):
        self.add_client_button = QPushButton("Add Client", self)
        self.add_client_button.clicked.connect(self._open_new_client_dialog)
        layout.addWidget(self.add_client_button, alignment=Qt.AlignCenter)

    def _view_clients_button(self, layout):
        self.view_clients_button = QPushButton("View Clients", self)
        self.view_clients_button.clicked.connect(self._open_view_clients_dialog)
        layout.addWidget(self.view_clients_button, alignment=Qt.AlignCenter)

    def _search_clients_button(self, layout):
        self.search_clients_button = QPushButton("Client Suchen", self)
        self.search_clients_button.clicked.connect(self._open_search_clients_dialog)
        layout.addWidget(self.search_clients_button, alignment=Qt.AlignCenter)

    def _open_new_client_dialog(self):
        dialog = NewClientDialog(self.database_manager, self)
        dialog.exec_()

    def _open_view_clients_dialog(self):
        dialog = ViewClientsDialog(self.database_manager, self)
        dialog.exec_()

    def _open_search_clients_dialog(self):
        dialog = SearchClientDialog(self.database_manager, self)
        dialog.exec_()


def main():
    app = QApplication(sys.argv)  # allows CLI args
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
