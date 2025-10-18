import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QStackedWidget, QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt5.QtCore import Qt
from database import create_tables, register_user, check_login, add_medicine, get_medicines, delete_medicine


# -------- Dashboard Window --------
class Dashboard(QWidget):
    def __init__(self, user_id, username, stacked_widget):
        super().__init__()
        self.user_id = user_id
        self.username = username
        self.stacked_widget = stacked_widget

        self.setWindowTitle("Medischedular Dashboard")
        self.setGeometry(200, 100, 700, 500)

        layout = QVBoxLayout()
        title = QLabel(f"Welcome, {username} 👋")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        # --- Medicine Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Medicine", "Dosage", "Time"])
        layout.addWidget(self.table)

        # --- Form Fields ---
        form_layout = QHBoxLayout()

        self.med_name = QLineEdit()
        self.med_name.setPlaceholderText("Medicine Name")
        form_layout.addWidget(self.med_name)

        self.dosage = QLineEdit()
        self.dosage.setPlaceholderText("Dosage (e.g., 1 pill)")
        form_layout.addWidget(self.dosage)

        self.time = QLineEdit()
        self.time.setPlaceholderText("Time (e.g., 8:00 AM)")
        form_layout.addWidget(self.time)

        self.add_btn = QPushButton("➕ Add Medicine")
        self.add_btn.clicked.connect(self.add_medicine)
        form_layout.addWidget(self.add_btn)

        layout.addLayout(form_layout)

        # --- Delete button ---
        self.delete_btn = QPushButton("🗑️ Delete Selected")
        self.delete_btn.clicked.connect(self.delete_selected)
        layout.addWidget(self.delete_btn)

        self.logout_btn = QPushButton("🚪 Logout")
        self.logout_btn.clicked.connect(self.logout)
        layout.addWidget(self.logout_btn)

        self.setLayout(layout)
        self.load_medicines()

    def load_medicines(self):
        data = get_medicines(self.user_id)
        self.table.setRowCount(0)
        for row_num, row_data in enumerate(data):
            self.table.insertRow(row_num)
            for col_num, value in enumerate(row_data):
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(value)))

    def add_medicine(self):
        name = self.med_name.text().strip()
        dosage = self.dosage.text().strip()
        time = self.time.text().strip()

        if not name or not dosage or not time:
            QMessageBox.warning(self, "Error", "Please fill all fields.")
            return

        add_medicine(self.user_id, name, dosage, time)
        QMessageBox.information(self, "Added", "Medicine added successfully!")
        self.med_name.clear()
        self.dosage.clear()
        self.time.clear()
        self.load_medicines()

    def delete_selected(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Error", "Please select a medicine to delete.")
            return

        med_id = int(self.table.item(selected_row, 0).text())
        delete_medicine(med_id)
        QMessageBox.information(self, "Deleted", "Medicine deleted successfully!")
        self.load_medicines()

    def logout(self):
        self.stacked_widget.setCurrentIndex(0)


# -------- Signup Window --------
class SignupWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setWindowTitle("Signup - Medischedular")
        self.setGeometry(200, 100, 400, 400)

        layout = QVBoxLayout()
        title = QLabel("🩺 Create a Medischedular Account")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        layout.addWidget(self.username)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        layout.addWidget(self.email)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        self.signup_btn = QPushButton("Create Account")
        self.signup_btn.clicked.connect(self.signup)
        layout.addWidget(self.signup_btn)

        self.back_btn = QPushButton("⬅️ Back to Login")
        self.back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(self.back_btn)

        self.setLayout(layout)

    def signup(self):
        username = self.username.text().strip()
        email = self.email.text().strip()
        password = self.password.text().strip()

        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        if register_user(username, email, password):
            QMessageBox.information(self, "Success", "Account created successfully!")
            self.stacked_widget.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Error", "Username already exists!")


# -------- Login Window --------
class LoginWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setWindowTitle("Login - Medischedular")
        self.setGeometry(200, 100, 400, 400)

        layout = QVBoxLayout()
        title = QLabel("💊 Medischedular Login")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.login)
        layout.addWidget(self.login_btn)

        self.signup_btn = QPushButton("Create a new account")
        self.signup_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(self.signup_btn)

        self.setLayout(layout)

    def login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Enter both username and password.")
            return

        user = check_login(username, password)
        if user:
            user_id = user[0]
            QMessageBox.information(self, "Success", "Login successful!")
            dashboard = Dashboard(user_id, username, self.stacked_widget)
            self.stacked_widget.addWidget(dashboard)
            self.stacked_widget.setCurrentWidget(dashboard)
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials.")


# -------- App Entry Point --------
if __name__ == "__main__":
    create_tables()

    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()

    login_window = LoginWindow(stacked_widget)
    signup_window = SignupWindow(stacked_widget)

    stacked_widget.addWidget(login_window)
    stacked_widget.addWidget(signup_window)
    stacked_widget.setCurrentIndex(0)
    stacked_widget.resize(700, 500)
    stacked_widget.show()

    sys.exit(app.exec_())