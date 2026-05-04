import os

os.environ['OPENCV_LOG_LEVEL'] = 'OFF'
os.environ['OPENCV_FFMPEG_LOGLEVEL'] = '-8'
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp|probesize;32|analyzeduration;0|fflags;nobuffer|flags;low_delay"

import customtkinter as ctk
import cv2
import threading
import time
from PIL import Image, ImageTk, ImageDraw


class VideoStream(ctk.CTkFrame):
    def __init__(self, parent, rtsp_url, width, height):
        super().__init__(parent, fg_color="black")
        self.rtsp_url = rtsp_url
        self.size = (width, height)
        self.current_frame = None
        self.running = True

        # Create offline placeholder
        self.offline_img = self._create_offline_placeholder()
        self.ctk_image = ctk.CTkImage(light_image=self.offline_img, dark_image=self.offline_img, size=self.size)

        self.image_label = ctk.CTkLabel(self, image=self.ctk_image, text="")
        self.image_label.pack(fill="both", expand=True)

        threading.Thread(target=self._stream_loop, daemon=True).start()
        self.update_ui()

    def stop(self):
        self.running = False

    def _create_offline_placeholder(self):
        img = Image.new("RGB", self.size, color="black")
        draw = ImageDraw.Draw(img)
        # Center text calculation
        text = "CAMERA OFFLINE"
        bbox = draw.textbbox((0, 0), text)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (self.size[0] - text_w) // 2
        y = (self.size[1] - text_h) // 2
        draw.text((x, y), text, fill="white")
        return img

    def _stream_loop(self):
        while self.running:
            cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            try:
                while cap.isOpened() and self.running:
                    if cap.grab():
                        ret, frame = cap.retrieve()
                        if ret:
                            self.current_frame = frame
                        else:
                            break
                    else:
                        break
            finally:
                self.current_frame = None
                cap.release()

            if self.running:
                time.sleep(5)

    def update_ui(self):
        if self.current_frame is not None:
            cv2image = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image).resize(self.size)
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=self.size)
            self.image_label.configure(image=ctk_img)
        else:
            self.image_label.configure(image=self.ctk_image)

        if self.running:
            self.after(30, self.update_ui)