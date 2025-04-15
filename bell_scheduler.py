#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import time
from datetime import datetime
from playsound import playsound
import os

class BellSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("벨 스케줄러")
        self.root.geometry("400x500")

        self.times = [
            "09:10", "10:00", "10:10", "11:00", "11:10",
            "12:00", "12:10", "13:00", "14:00", "14:50",
            "15:00", "15:50", "16:00", "16:50"
        ]

        self.bell_path = os.path.abspath("bell.mp3")

        self.time_vars = []
        self.create_widgets()
        self.running = True
        threading.Thread(target=self.check_time_loop, daemon=True).start()

    def create_widgets(self):
        tk.Label(self.root, text="벨 울릴 시간 설정 (HH:MM)").pack()

        for t in self.times:
            var = tk.StringVar(value=t)
            entry = tk.Entry(self.root, textvariable=var, width=10)
            entry.pack(pady=2)
            self.time_vars.append(var)

        tk.Label(self.root, text="MP3 파일 경로").pack(pady=(10,0))
        self.mp3_label = tk.Label(self.root, text=self.bell_path, fg="blue", wraplength=350)
        self.mp3_label.pack()

        tk.Button(self.root, text="MP3 변경", command=self.change_mp3).pack(pady=5)
        tk.Button(self.root, text="설정 저장 및 벨 시작", command=self.save_settings).pack(pady=10)
        tk.Button(self.root, text="종료", command=self.exit_program).pack()

    def change_mp3(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if file_path:
            self.bell_path = file_path
            self.mp3_label.config(text=file_path)

    def save_settings(self):
        self.times = [var.get() for var in self.time_vars]
        messagebox.showinfo("저장됨", "설정이 저장되었어요!")

    def check_time_loop(self):
        already_rung = set()
        while self.running:
            now = datetime.now().strftime("%H:%M")
            if now in self.times and now not in already_rung:
                already_rung.add(now)
                try:
                    playsound(self.bell_path)
                except Exception as e:
                    messagebox.showerror("재생 오류", f"MP3 파일 재생 중 오류 발생: {e}")
            time.sleep(20)  # 20초마다 확인

    def exit_program(self):
        self.running = False
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = BellSchedulerApp(root)
    root.mainloop()

