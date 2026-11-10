import sys
import random
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QLabel, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

class Ball(QGraphicsPixmapItem):
    def __init__(self):
        super().__init__()
        # Sử dụng hình ảnh thay cho bóng
        self.setPixmap(QPixmap('ball.png').scaled(50, 50))  # Bóng có kích thước 50x50
        self.dx = 0
        self.dy = 0

    def move_ball(self):
        # Di chuyển bóng theo hướng và vận tốc dx, dy
        self.setPos(self.x() + self.dx, self.y() + self.dy)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.dx = -5
        elif event.key() == Qt.Key_Right:
            self.dx = 5
        elif event.key() == Qt.Key_Up:
            self.dy = -5
        elif event.key() == Qt.Key_Down:
            self.dy = 5

    def keyReleaseEvent(self, event):
        if event.key() in [Qt.Key_Left, Qt.Key_Right]:
            self.dx = 0
        if event.key() in [Qt.Key_Up, Qt.Key_Down]:
            self.dy = 0

class GameWindow(QGraphicsView):
    def __init__(self):
        super().__init__()

        # Khởi tạo Scene với nền
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setFixedSize(800, 600)

        # Thêm hình nền cho scene
        self.background = QGraphicsPixmapItem(QPixmap('background.png').scaled(800, 600))
        self.scene.addItem(self.background)

        # Thêm bóng vào scene
        self.ball = Ball()
        self.ball.setPos(50, 50)
        self.scene.addItem(self.ball)
        self.ball.setFlag(self.ball.ItemIsFocusable)
        self.ball.setFocus()

        # Thêm chướng ngại vật
        self.obstacles = []
        for _ in range(5):
            obstacle = QGraphicsPixmapItem(QPixmap('obstacle.png').scaled(50, 50))
            obstacle.setPos(random.randint(100, 700), random.randint(100, 500))
            self.obstacles.append(obstacle)
            self.scene.addItem(obstacle)

        # Thêm điểm (vật phẩm)
        self.points = []
        for _ in range(3):
            point = QGraphicsPixmapItem(QPixmap('point.png').scaled(30, 30))
            point.setPos(random.randint(100, 700), random.randint(100, 500))
            self.points.append(point)
            self.scene.addItem(point)

        # Tạo bộ đếm điểm
        self.score = 0
        self.score_label = QLabel(f"Điểm: {self.score}")
        self.score_label.setFont(QFont('Arial', 20))
        self.score_label.setStyleSheet("color: white;")
        self.scene.addWidget(self.score_label)

        # Timer để cập nhật vị trí bóng
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)  # 60 fps

        # Giao diện chính
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self)
        self.layout.addWidget(self.score_label)
        self.widget.setLayout(self.layout)
        self.widget.setWindowTitle("Game Bóng Nâng Cấp")
        self.widget.setGeometry(100, 100, 800, 600)
        self.widget.show()

    def update_game(self):
        self.ball.move_ball()

        # Kiểm tra va chạm với chướng ngại vật
        for obstacle in self.obstacles:
            if self.ball.collidesWithItem(obstacle):
                self.reset_ball()

        # Kiểm tra va chạm với điểm và tăng điểm
        for point in self.points:
            if self.ball.collidesWithItem(point):
                self.scene.removeItem(point)
                self.points.remove(point)
                self.score += 1
                self.score_label.setText(f"Điểm: {self.score}")
                break

        # Kiểm tra nếu đã ăn hết điểm thì qua màn
        if len(self.points) == 0:
            self.next_level()

    def reset_ball(self):
        # Đưa bóng về vị trí ban đầu
        self.ball.setPos(50, 50)
        self.ball.dx = 0
        self.ball.dy = 0

    def next_level(self):
        # Qua màn
        QMessageBox.information(self, 'Chúc mừng', 'Bạn đã qua màn!')
        self.scene.clear()
        self.scene.addItem(self.background)
        self.ball = Ball()
        self.ball.setPos(50, 50)
        self.scene.addItem(self.ball)
        self.ball.setFlag(self.ball.ItemIsFocusable)
        self.ball.setFocus()

        # Tạo lại chướng ngại vật và điểm mới
        self.obstacles = []
        for _ in range(7):
            obstacle = QGraphicsPixmapItem(QPixmap('obstacle.png').scaled(50, 50))
            obstacle.setPos(random.randint(100, 700), random.randint(100, 500))
            self.obstacles.append(obstacle)
            self.scene.addItem(obstacle)

        self.points = []
        for _ in range(5):
            point = QGraphicsPixmapItem(QPixmap('point.png').scaled(30, 30))
            point.setPos(random.randint(100, 700), random.randint(100, 500))
            self.points.append(point)
            self.scene.addItem(point)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()
    sys.exit(app.exec_())
