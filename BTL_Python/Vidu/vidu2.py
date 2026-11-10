import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, \
    QTableWidgetItem, QLineEdit, QLabel, QMessageBox, QHeaderView, QFrame
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt


class StudentManagementApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Quản lý sinh viên - Phiên bản chuyên nghiệp')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #F8F9FA;
                font-family: Arial;
                font-size: 14px;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLabel {
                color: #343A40;
                font-weight: bold;
            }
            QTableWidget {
                background-color: white;
                border-radius: 5px;
                padding: 5px;
                border: 1px solid #CED4DA;
            }
        """)

        self.initUI()
        self.createDatabase()

    def initUI(self):
        layout = QVBoxLayout()

        # Tiêu đề ứng dụng
        title_label = QLabel("Quản lý Sinh viên")
        title_label.setFont(QFont('Arial', 24))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Tạo bảng hiển thị sinh viên
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Mã SV', 'Họ tên', 'Lớp', 'Ngày sinh'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setFrameShape(QFrame.NoFrame)
        layout.addWidget(self.table)

        # Form nhập thông tin sinh viên
        form_layout = QHBoxLayout()
        self.student_id_input = QLineEdit()
        self.student_id_input.setPlaceholderText("Mã SV")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Họ tên")
        self.class_input = QLineEdit()
        self.class_input.setPlaceholderText("Lớp")
        self.dob_input = QLineEdit()
        self.dob_input.setPlaceholderText("Ngày sinh (dd/mm/yyyy)")

        form_layout.addWidget(QLabel("Mã SV:"))
        form_layout.addWidget(self.student_id_input)
        form_layout.addWidget(QLabel("Họ tên:"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel("Lớp:"))
        form_layout.addWidget(self.class_input)
        form_layout.addWidget(QLabel("Ngày sinh:"))
        form_layout.addWidget(self.dob_input)

        layout.addLayout(form_layout)

        # Các nút chức năng với icon
        button_layout = QHBoxLayout()

        self.add_button = QPushButton('Thêm')
        self.add_button.setIcon(QIcon("add_icon.png"))  # Thêm icon
        self.update_button = QPushButton('Sửa')
        self.update_button.setIcon(QIcon("edit_icon.png"))  # Thêm icon
        self.delete_button = QPushButton('Xóa')
        self.delete_button.setIcon(QIcon("delete_icon.png"))  # Thêm icon
        self.load_button = QPushButton('Tải lại')
        self.load_button.setIcon(QIcon("refresh_icon.png"))  # Thêm icon

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.load_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Kết nối sự kiện các nút
        self.add_button.clicked.connect(self.addStudent)
        self.update_button.clicked.connect(self.updateStudent)
        self.delete_button.clicked.connect(self.deleteStudent)
        self.load_button.clicked.connect(self.loadStudents)

    def createDatabase(self):
        self.conn = sqlite3.connect('students.db')
        self.c = self.conn.cursor()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT,
                class TEXT,
                dob TEXT
            )
        ''')
        self.conn.commit()
        self.loadStudents()

    def loadStudents(self):
        self.c.execute('SELECT * FROM students')
        rows = self.c.fetchall()

        self.table.setRowCount(0)
        for row in rows:
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)
            for col, data in enumerate(row):
                self.table.setItem(rowPosition, col, QTableWidgetItem(str(data)))

    def addStudent(self):
        student_id = self.student_id_input.text()
        name = self.name_input.text()
        student_class = self.class_input.text()
        dob = self.dob_input.text()

        try:
            self.c.execute('INSERT INTO students (student_id, name, class, dob) VALUES (?, ?, ?, ?)',
                           (student_id, name, student_class, dob))
            self.conn.commit()
            QMessageBox.information(self, 'Thông báo', 'Thêm sinh viên thành công!')
            self.loadStudents()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, 'Lỗi', 'Mã sinh viên đã tồn tại!')

    def updateStudent(self):
        student_id = self.student_id_input.text()
        name = self.name_input.text()
        student_class = self.class_input.text()
        dob = self.dob_input.text()

        self.c.execute('UPDATE students SET name = ?, class = ?, dob = ? WHERE student_id = ?',
                       (name, student_class, dob, student_id))
        self.conn.commit()
        QMessageBox.information(self, 'Thông báo', 'Sửa thông tin sinh viên thành công!')
        self.loadStudents()

    def deleteStudent(self):
        student_id = self.student_id_input.text()

        self.c.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
        self.conn.commit()
        QMessageBox.information(self, 'Thông báo', 'Xóa sinh viên thành công!')
        self.loadStudents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StudentManagementApp()
    window.show()
    sys.exit(app.exec_())
