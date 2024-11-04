# SystemInfo
A program that allows you to collect device data to speed up inventory. This program will help many system administrators

### Start
To get the application, you need to install Python on the official [website](https://www.python.org/), and then you need to install the library: `pip install pyinstaller`.

Creating an application in the form of .exe: `pyinstaller --onefile file.py`
- `--windowed` - A flag that prevents the application from opening the console window.
- `--icon=/path/path/` - The checkbox is used to indicate the icon in the format `.ico`
- `--add-data "info;info"` - The command allows you to add all files from the section you specified