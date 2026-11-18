from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QRunnable, QThreadPool, Slot
from PySide6.QtGui import QImage, QPixmap, QTextCursor
from ui_lander import Ui_MainWindow
import os, subprocess
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg


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
        self.ui.stopButton.clicked.connect(lambda: self.onStop())
        self.threadpool = QThreadPool()
        self.vs = []
        self.hs = []
        self.show()

    def updateCharts(self, line):
        newData = line.split(" ")
        if newData[0] == "Ladownik":
            return
        self.hs.append(float(newData[1]))
        self.vs.append(float(newData[4]))
        fig = Figure((450, 250, "px"))
        canvas = FigureCanvasAgg(fig)
        plot = fig.add_subplot(111)
        plot.plot(self.hs)
        plot.set_title("Wysokość po czasie")
        fig.savefig("hwykres.png")
        canvas.draw()
        self.img = QImage(
            canvas.buffer_rgba(),
            450,
            250,
            QImage.Format.Format_ARGB32,
        )
        pixmap = QPixmap(self.img)
        self.ui.hWykres.setPixmap(pixmap)
        fig = Figure((450, 250, "px"))
        canvas = FigureCanvasAgg(fig)
        plot = fig.add_subplot(111)
        plot.plot(self.vs)
        plot.set_title("Prędkość po czasie")
        fig.savefig("vwykres.png")
        canvas.draw()
        self.img = QImage(
            canvas.buffer_rgba(),
            450,
            250,
            QImage.Format.Format_ARGB32,
        )
        pixmap = QPixmap(self.img)
        self.ui.vWykres.setPixmap(pixmap)

    def display(self):
        print(
            self.ui.mEdit.text()
            + " "
            + self.ui.hEdit.text()
            + " "
            + self.ui.vEdit.text()
            + " "
            + self.ui.fEdit.text()
            + " "
            + self.ui.fileEdit.text()
            + " "
            + self.ui.timeEdit.text()
        )
        self.process = subprocess.Popen(
            [
                os.path.abspath("../sim/sim.exe"),
                self.ui.mEdit.text(),
                self.ui.hEdit.text(),
                self.ui.vEdit.text(),
                self.ui.fEdit.text(),
                self.ui.fileEdit.text(),
                self.ui.timeEdit.text(),
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        )
        for line in self.process.stdout:
            self.ui.textBrowser.append(line)
            self.ui.textBrowser.moveCursor(QTextCursor.MoveOperation.End)
            self.ui.textBrowser.update()
            self.updateCharts(line)

    def onStart(self):
        displayWorker = DisplayWorker(self.display)
        self.threadpool.start(displayWorker)

    def onSilnik(self):
        # self.process.stdin.seek(0, 2)
        self.process.stdin.write("\n")
        # self.process.stdin.flush()
        # self.process.stdin.close()

    def onStop(self):
        self.process.kill()


app = QApplication()
window = MainWindow()
app.exec()
