import threading
import cv2
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtGui import QImage

class VideoThread(QObject, threading.Thread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self, camera_index=0):
        QObject.__init__(self)
        threading.Thread.__init__(self)
        self.camera_index = camera_index
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(self.camera_index)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                self.change_pixmap_signal.emit(qt_img)
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()
