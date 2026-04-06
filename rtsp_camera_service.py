import os

os.environ['OPENCV_LOG_LEVEL'] = 'OFF'
os.environ['OPENCV_FFMPEG_LOGLEVEL'] = '-8'
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp|probesize;32|analyzeduration;0|fflags;nobuffer|flags;low_delay"

import tkinter as tk
import cv2
import threading
import time
from PIL import Image, ImageTk, ImageDraw


class VideoStream(tk.Label):
    def __init__(self, parent, rtsp_url, width, height):
        super().__init__(parent, bg="black")
        self.rtsp_url = rtsp_url
        self.size = (width, height)
        self.current_frame = None
        self.running = True

        self.offline_img = self._create_offline_placeholder()
        self.configure(image=self.offline_img)
        self.imgtk = self.offline_img

        threading.Thread(target=self._stream_loop, daemon=True).start()
        self.update_ui()

    def stop(self):
        self.running = False

    def _create_offline_placeholder(self):
        # Offline placeholder
        img = Image.new("RGB", self.size, color="black")
        draw = ImageDraw.Draw(img)
        draw.text((self.size[0] // 2 - 40, self.size[1] // 2), "CAMERA OFFLINE", fill="white")
        return ImageTk.PhotoImage(img)

    def _stream_loop(self):
        while True:
            cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            try:
                while cap.isOpened() and self.running:
                    if cap.grab():
                        ret, frame = cap.retrieve()
                        if ret:
                            self.current_frame = frame
                        else:
                            break  # Connection lost, trigger reconnect
            finally:
                self.current_frame = None
                cap.release()
            if self.running:
                time.sleep(5)  # Wait 5 seconds before retrying

    def update_ui(self):
        if self.current_frame is not None:
            # Show live stream
            cv2image = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image).resize(self.size)
            imgtk = ImageTk.PhotoImage(image=img)
            self.imgtk = imgtk
            self.configure(image=imgtk)
        else:
            self.configure(image=self.offline_img)
            self.imgtk = self.offline_img

        self.after(30, self.update_ui)