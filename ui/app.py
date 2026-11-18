from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QRunnable, QThreadPool, Slot
from PySide6.QtGui import QTextCursor
from ui_lander import Ui_MainWindow
import os, subprocess


class DisplayWorker(QRunnable):
    def __init__(self, display):
        super().__init__()
        self.display = display

    @Slot()
    def run(self):
        self.display()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.startButton.clicked.connect(lambda: self.onStart())
        self.ui.silnikButton.clicked.connect(lambda: self.onSilnik())
        self.threadpool = QThreadPool()
        self.show()

    def display(self):
        self.process = subprocess.Popen(
            [os.path.abspath("../sim/sim.exe"), ""],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        )
        for line in self.process.stdout:
            self.ui.textBrowser.append(line)
            self.ui.textBrowser.moveCursor(QTextCursor.MoveOperation.End)
            self.ui.textBrowser.update()

    def onStart(self):
        displayWorker = DisplayWorker(self.display)
        self.threadpool.start(displayWorker)

    def onSilnik(self):
        self.process.stdin.seek(0,2)
        self.process.stdin.write("\n")
        #self.process.stdin.flush()
        # self.process.stdin.close()


app = QApplication()
window = MainWindow()
(app.exec(),)
