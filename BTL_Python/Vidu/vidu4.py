import sys
import random
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QLabel, QVBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer, QBasicTimer

class Plant(QGraphicsPixmapItem):
    def __init__(self):
        super().__init__()
        self.setPixmap(QPixmap('plant.png').scaled(60, 60))  # Hình ảnh của cây

    def shoot(self):
        bullet = Bullet(self.x() + 50, self.y() + 15)  # Đạn bắn ra từ cây
        return bullet

class Bullet(QGraphicsPixmapItem):
    def __init__(self, x, y):
        super().__init__()
        self.setPixmap(QPixmap('bullet.png').scaled(20, 20))  # Hình ảnh của đạn
        self.setPos(x, y)

    def move(self):
        self.setX(self.x() + 10)  # Đạn di chuyển từ trái sang phải

class Zombie(QGraphicsPixmapItem):
    def __init__(self):
        super().__init__()
        self.setPixmap(QPixmap('zombie.png').scaled(60, 60))  # Hình ảnh zombie
        self.setPos(800, random.randint(100, 500))  # Zombie xuất hiện ở mép phải của màn hình
        self.health = 100  # Máu của zombie

    def move(self):
        self.setX(self.x() - 2)  # Zombie di chuyển từ phải sang trái

    def is_dead(self):
        return self.health <= 0

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

        # Thêm cây
        self.plant = Plant()
        self.plant.setPos(50, 250)
        self.scene.addItem(self.plant)

        # Thêm zombies
        self.zombies = []
        self.spawn_zombie()

        # Danh sách đạn bắn ra
        self.bullets = []

        # Timer để cập nhật trò chơi
        self.timer = QBasicTimer()
        self.timer.start(16, self)  # Cập nhật trò chơi mỗi 16ms (60fps)

        # Điểm số
        self.score = 0
        self.score_label = QLabel(f"Điểm: {self.score}")
        self.score_label.setFont(QFont('Arial', 16))
        self.scene.addWidget(self.score_label)

        # Nút bắn
        self.shoot_button = QPushButton("Shoot")
        self.shoot_button.clicked.connect(self.shoot_bullet)
        self.scene.addWidget(self.shoot_button)

        # Giao diện chính
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self)
        self.layout.addWidget(self.shoot_button)
        self.layout.addWidget(self.score_label)
        self.widget.setLayout(self.layout)
        self.widget.setWindowTitle("Plants vs. Zombies Simple")
        self.widget.setGeometry(100, 100, 800, 600)
        self.widget.show()

    def timerEvent(self, event):
        # Di chuyển đạn
        for bullet in self.bullets:
            bullet.move()
            if bullet.x() > 800:
                self.scene.removeItem(bullet)
                self.bullets.remove(bullet)
            else:
                for zombie in self.zombies:
                    if bullet.collidesWithItem(zombie):
                        zombie.health -= 50
                        self.scene.removeItem(bullet)
                        self.bullets.remove(bullet)
                        if zombie.is_dead():
                            self.scene.removeItem(zombie)
                            self.zombies.remove(zombie)
                            self.score += 1
                            self.score_label.setText(f"Điểm: {self.score}")
                        break

        # Di chuyển zombie
        for zombie in self.zombies:
            zombie.move()
            if zombie.x() < 0:
                QMessageBox.information(self, "Game Over", "Zombie đã tới nơi!")
                self.close()

        # Sinh zombie mới
        if len(self.zombies) == 0:
            self.spawn_zombie()

    def shoot_bullet(self):
        bullet = self.plant.shoot()
        self.scene.addItem(bullet)
        self.bullets.append(bullet)

    def spawn_zombie(self):
        for _ in range(3):  # Tạo ra 3 zombie
            zombie = Zombie()
            self.scene.addItem(zombie)
            self.zombies.append(zombie)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()
    sys.exit(app.exec_())
