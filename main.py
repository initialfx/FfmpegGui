from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

import sys, os

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.p = None

        self.options = QLineEdit("-vcodec libx264")
        self.select_btn = QPushButton("Source File")
        self.select_btn.clicked.connect(self.selectSource)

        self.selected_file = QLineEdit()        

        self.btn = QPushButton("Convert Movie")
        self.btn.pressed.connect(self.start_process)

        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        l = QVBoxLayout()

        #l.addWidget(self.select_btn)
        #l.addWidget(self.selected_file)
        l.addWidget(self.btn)
        l.addWidget(self.options)
        l.addWidget(self.text)

        w = QWidget()
        w.setLayout(l)

        self.setCentralWidget(w)

    def selectSource(self):
        selected = QFileDialog.getOpenFileName(None, 'Test Dialog', os.getcwd(), 'All Files(*.*)')
        filename = selected[0].split("/")[-1]
        fullpath = selected[0].split(filename)[0]

        self.selected_file.setText(filename)

        return filename, fullpath


    def message(self, s):
        self.text.appendPlainText(s)

    def start_process(self):
        if self.p is None:  # No process running.
            self.message("Executing process")
            self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)  # Clean up once complete.
            
            
            #self.p.start("python", ['dummy_script.py'])
            source = self.selectSource()
            filename = source[0]
            fullpath = source[1]

            ext = filename.split(".")[-1]
            pad = filename.split(".")[-2]
            name = filename.split("."+pad+".")[-2]
            pads = '%{}d'.format(len(filename.split(".")[-2]))

            #source_file = 'foo.%04d.jpg'
            source_file = '{}/{}.{}.{}'.format(fullpath, name, pads, ext)

            #out_file = 'test2.mp4'
            out_file = '{}/{}.{}'.format(fullpath , name, "mp4")

            codec = 'libx264'
            
            self.p.start("ffmpeg", ['-i', source_file, '-y', out_file])

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}")

    def process_finished(self):
        self.message("Process finished.")
        self.p = None


app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec_()