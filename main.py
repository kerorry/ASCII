import sys
import os
import colorsys
import threading
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QGraphicsDropShadowEffect)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor
import pystray
from pystray import MenuItem as item
from PIL import Image

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.ascii_art = '''
 _   __                               
| | / /                               
| |/ /  ___ _ __ ___  _ __ _ __ _   _ 
|    \ / _ \ '__/ _ \| '__| '__| | | |
| |\  \  __/ | | (_) | |  | |  | |_| |
\_| \_/\___|_|  \___/|_|  |_|   \__, |
                                 __/ |
                                |___/ 
'''
        self.hue = 0.0 # 色相

    # 初始化UI
    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setFocusPolicy(Qt.NoFocus)
        # self.setWindowOpacity(0.8)

        self.label = QLabel(self.ascii_art, self)
        font = QFont("Consolas", 8)
        self.label.setFont(font)
        self.label.setStyleSheet("color: white; background: transparent;")
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # 阴影
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(4)
        shadow.setOffset(2, 2)
        shadow.setColor(QColor(0, 0, 0, 128))
        self.label.setGraphicsEffect(shadow)

        # 计算文本尺寸
        fm = self.label.fontMetrics()
        lines = self.ascii_art.splitlines()
        max_width = max(fm.horizontalAdvance(line) for line in lines)
        total_height = fm.height() * len(lines)

        # 窗口大小
        padding = 10
        self.resize(max_width + padding*2, total_height + padding*2)
        self.label.move(padding, padding)

        # 居中
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    # 定时器
    def start_animation(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_color)
        self.timer.start(30)

    # 色相变化
    def update_color(self):
        self.hue += 0.008
        if self.hue > 1.0:
            self.hue -= 1.0
        r, g, b = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
        color = QColor(int(r*255), int(g*255), int(b*255))
        self.label.setStyleSheet(f"color: {color.name()}; background: transparent;")

    # 托盘
    def start_system_tray(self):
        image = Image.open(self.get_resource_path("icon.ico"))
        self.tray_menu = (
            item('退出', self.on_quit),
        )
        self.icon = pystray.Icon("kerorry", image, "kerorry", self.tray_menu)
        self.icon_thread = threading.Thread(target=self.icon.run, daemon=False)
        self.icon_thread.start()

    # 获取资源路径
    def get_resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # 运行
    def run(self):
        print(self.ascii_art)
        self.initUI()
        self.start_animation()
        self.start_system_tray()

    def on_quit(self):
        if hasattr(self, 'icon'):
            self.icon.stop()
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.run()
    window.show()
    sys.exit(app.exec_())
