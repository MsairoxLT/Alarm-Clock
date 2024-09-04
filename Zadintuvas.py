from tkinter import *
from tkinter import filedialog
import datetime
import pygame
import os
import random
from threading import Thread


class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.geometry("510x600")

        pygame.mixer.init()

        self.alarm_running = False
        self.selected_folder = None
        self.alarms = []
        self.snooze_duration = 5

        self.folder_label = Label(self.root, text="", font=("Helvetica 10"), anchor="w", justify=LEFT)
        self.folder_label.pack(side=BOTTOM, fill=X, padx=10, pady=5)

        self.alarm_time_label = Label(self.root, text="", font=("Helvetica 12 bold"), fg="blue")
        self.alarm_time_label.pack(pady=5)

        self.alarms_frame = Frame(self.root)
        self.alarms_frame.pack(pady=5)

        self.snooze_button = Button(self.root, text="Snooze", command=self.snooze_alarm)
        self.stop_button = Button(self.root, text="Stop Alarm", command=self.stop_alarm)

        self.setup_ui()

    def setup_ui(self):
        Label(self.root, text="Alarm Clock", font=("Helvetica 20 bold"), fg="red").pack(pady=10)
        Label(self.root, text="Set Time", font=("Helvetica 15 bold")).pack()

        frame = Frame(self.root)
        frame.pack()

        self.hour = StringVar(self.root)
        self.minute = StringVar(self.root)
        self.second = StringVar(self.root)
        hours = [f"{i:02d}" for i in range(24)]
        minutes = seconds = [f"{i:02d}" for i in range(60)]
        self.hour.set(hours[0])
        self.minute.set(minutes[0])
        self.second.set(seconds[0])

        OptionMenu(frame, self.hour, *hours).pack(side=LEFT)
        OptionMenu(frame, self.minute, *minutes).pack(side=LEFT)
        OptionMenu(frame, self.second, *seconds).pack(side=LEFT)

        day_frame = Frame(self.root)
        day_frame.pack(pady=10)

        self.day_vars = {day: IntVar() for day in
                         ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
        for day, var in self.day_vars.items():
            Checkbutton(day_frame, text=day, variable=var).pack(side=LEFT)

        Button(self.root, text="Set Alarm", font=("Helvetica 15"), command=self.set_alarm).pack(pady=5)
        Button(self.root, text="Select Folder", font=("Helvetica 15"), command=self.select_folder).pack(pady=5)

        self.snooze_entry = Entry(self.root)
        self.snooze_entry.pack(pady=5)
        Button(self.root, text="Set Snooze Duration", font=("Helvetica 15"), command=self.set_snooze_duration).pack(
            pady=5)

    def threading(self):
        self.alarm_running = True
        Thread(target=self.alarm).start()

    def alarm(self):
        while self.alarm_running:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            current_day = datetime.datetime.now().strftime("%A")
            for alarm_time, days in self.alarms:
                if (not days or current_day in days) and current_time == alarm_time:
                    if self.selected_folder:
                        self.play_random_song(self.selected_folder)
                    self.alarm_time_label.config(text="")
                    self.snooze_button.pack(pady=5)
                    self.stop_button.pack(pady=5)
                    return

    def stop_alarm(self):
        self.alarm_running = False
        pygame.mixer.music.stop()
        self.alarm_time_label.config(text="")
        self.snooze_button.pack_forget()
        self.stop_button.pack_forget()

    def snooze_alarm(self):
        self.alarm_running = False
        pygame.mixer.music.stop()
        self.snooze_button.pack_forget()
        self.stop_button.pack_forget()
        snooze_time = datetime.datetime.now() + datetime.timedelta(minutes=self.snooze_duration)
        self.alarms.append((snooze_time.strftime("%H:%M:%S"), [datetime.datetime.now().strftime("%A")]))
        self.threading()

    def select_folder(self):
        self.selected_folder = filedialog.askdirectory()
        self.folder_label.config(text=f"Selected folder: {self.selected_folder}")

    def play_random_song(self, folder):
        files = [file for file in os.listdir(folder) if file.endswith(('.mp3', '.wav'))]
        if files:
            pygame.mixer.music.load(os.path.join(folder, random.choice(files)))
            pygame.mixer.music.play()

    def set_alarm(self):
        set_alarm_time = f"{self.hour.get()}:{self.minute.get()}:{self.second.get()}"
        selected_days = [day for day, var in self.day_vars.items() if var.get() == 1]
        self.alarms.append((set_alarm_time, selected_days))
        self.alarm_time_label.config(
            text=f"Alarm set for: {set_alarm_time} on {', '.join(selected_days) if selected_days else 'every day'}")
        self.update_alarms_label()
        self.threading()

    def delete_alarm(self, index):
        del self.alarms[index]
        self.update_alarms_label()

    def update_alarms_label(self):
        for widget in self.alarms_frame.winfo_children():
            widget.destroy()
        for index, (time, days) in enumerate(self.alarms):
            alarm_text = f"{time} on {', '.join(days) if days else 'every day'}"
            Label(self.alarms_frame, text=alarm_text, font=("Helvetica 10")).pack(side=LEFT)
            Button(self.alarms_frame, text="Delete", command=lambda i=index: self.delete_alarm(i)).pack(side=LEFT)

    def set_snooze_duration(self):
        self.snooze_duration = int(self.snooze_entry.get())


if __name__ == "__main__":
    root = Tk()
    app = AlarmClock(root)
    root.mainloop()
