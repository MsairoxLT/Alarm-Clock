# Alarm-Clock

Description:
This Python application is a simple alarm clock that allows users to set alarms with custom times and weekdays. It also features a snooze function and the ability to play random songs from a selected folder when an alarm triggers.

How to Use:
git clone https://github.com/MsairoxLT/alarm-clock

Install dependencies:
   pip install pyinstaller
Run PyInstaller: Use the following command to create the executable:
   pyinstaller Zadintuvas.py
PyInstaller will create a directory named dist containing the executable and any necessary dependencies.

One-file mode: To create a single executable file instead of a directory, use the --onefile option:
   pyinstaller --onefile Zadintuvas.py
* My preffered method of installing.
 
Freezing dependencies: To embed all dependencies within the executable, use the --noconsole option:
   pyinstaller --noconsole Zadintuvas.py

Features:

Set alarms with custom times and weekdays.
Snooze function (5 minutes is standart ).
Play random songs from a selected folder.
User-friendly interface.

Contributing:
Feel free to contribute to this project by submitting pull requests. Please follow the code style guidelines and add unit tests for any new features or bug fixes.

* For full comprehension of guide open up READ ME file.
