from tkinter import *
from tkinter import filedialog
import datetime
import pygame
import os
import random
from threading import Thread

root = Tk()
root.geometry("510x600")

pygame.mixer.init()

alarm_running = False
selected_folder = None
alarms = []
snooze_duration = 5

folder_label = Label(root, text="", font=("Helvetica 10"), anchor="w", justify=LEFT)
folder_label.pack(side=BOTTOM, fill=X, padx=10, pady=5)

alarm_time_label = Label(root, text="", font=("Helvetica 12 bold"), fg="blue")
alarm_time_label.pack(pady=5)

alarms_frame = Frame(root)
alarms_frame.pack(pady=5)

def threading():
    global alarm_running
    alarm_running = True
    Thread(target=alarm).start()

def alarm():
    while alarm_running:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        current_day = datetime.datetime.now().strftime("%A")
        for alarm_time, days in alarms:
            if (not days or current_day in days) and current_time == alarm_time:
                if selected_folder:
                    play_random_song(selected_folder)
                alarm_time_label.config(text="")
                snooze_button.pack(pady=5)
                return

def stop_alarm():
    global alarm_running
    alarm_running = False
    pygame.mixer.music.stop()
    alarm_time_label.config(text="")
    snooze_button.pack_forget()

def snooze_alarm():
    global alarm_running
    alarm_running = False
    pygame.mixer.music.stop()
    snooze_button.pack_forget()
    snooze_time = datetime.datetime.now() + datetime.timedelta(minutes=snooze_duration)
    alarms.append((snooze_time.strftime("%H:%M:%S"), [datetime.datetime.now().strftime("%A")]))
    threading()

def select_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory()
    folder_label.config(text=f"Selected folder: {selected_folder}")

def play_random_song(folder):
    files = [file for file in os.listdir(folder) if file.endswith(('.mp3', '.wav'))]
    if files:
        pygame.mixer.music.load(os.path.join(folder, random.choice(files)))
        pygame.mixer.music.play()

def set_alarm():
    set_alarm_time = f"{hour.get()}:{minute.get()}:{second.get()}"
    selected_days = [day for day, var in day_vars.items() if var.get() == 1]
    alarms.append((set_alarm_time, selected_days))
    alarm_time_label.config(text=f"Alarm set for: {set_alarm_time} on {', '.join(selected_days) if selected_days else 'every day'}")
    update_alarms_label()
    threading()

def delete_alarm(index):
    del alarms[index]
    update_alarms_label()

def update_alarms_label():
    for widget in alarms_frame.winfo_children():
        widget.destroy()
    for index, (time, days) in enumerate(alarms):
        alarm_text = f"{time} on {', '.join(days) if days else 'every day'}"
        Label(alarms_frame, text=alarm_text, font=("Helvetica 10")).pack(side=LEFT)
        Button(alarms_frame, text="Delete", command=lambda i=index: delete_alarm(i)).pack(side=LEFT)

def set_snooze_duration():
    global snooze_duration
    snooze_duration = int(snooze_entry.get())

Label(root, text="Alarm Clock", font=("Helvetica 20 bold"), fg="red").pack(pady=10)
Label(root, text="Set Time", font=("Helvetica 15 bold")).pack()

frame = Frame(root)
frame.pack()

hour = StringVar(root)
minute = StringVar(root)
second = StringVar(root)
hours = [f"{i:02d}" for i in range(24)]
minutes = seconds = [f"{i:02d}" for i in range(60)]
hour.set(hours[0])
minute.set(minutes[0])
second.set(seconds[0])

OptionMenu(frame, hour, *hours).pack(side=LEFT)
OptionMenu(frame, minute, *minutes).pack(side=LEFT)
OptionMenu(frame, second, *seconds).pack(side=LEFT)

day_frame = Frame(root)
day_frame.pack(pady=10)

day_vars = {day: IntVar() for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
for day, var in day_vars.items():
    Checkbutton(day_frame, text=day, variable=var).pack(side=LEFT)

Button(root, text="Set Alarm", font=("Helvetica 15"), command=set_alarm).pack(pady=5)
Button(root, text="Stop Alarm", font=("Helvetica 15"), command=stop_alarm).pack(pady=5)
Button(root, text="Select Folder", font=("Helvetica 15"), command=select_folder).pack(pady=5)

Label(root, text="Set Snooze Duration (5 minutes is standart)", font=("Helvetica 12")).pack(pady=5)
snooze_entry = Entry(root, font=("Helvetica 12"))
snooze_entry.pack(pady=5)
Button(root, text="Set Snooze Duration", font=("Helvetica 12"), command=set_snooze_duration).pack(pady=5)

snooze_button = Button(root, text="Snooze", font=("Helvetica 15"), command=snooze_alarm)

root.mainloop()
