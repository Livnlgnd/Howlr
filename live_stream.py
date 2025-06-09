import cv2
import threading

class LiveStreamController:
    def __init__(self, on_frame_callback=None):
        self.on_frame_callback = on_frame_callback
        self.cap = None
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            raise RuntimeError("Stream already running")
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera")
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def _run(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret and self.on_frame_callback:
                self.on_frame_callback(frame)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        if self.cap:
            self.cap.release()
