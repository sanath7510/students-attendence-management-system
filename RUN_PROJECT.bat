# BAT File to Run the Project

Create a file named `RUN_PROJECT.bat` inside your project folder and paste this:

```bat
@echo off
cd /d "%~dp0"

echo Installing required modules...
pip install -r requirements.txt

echo Starting Hybrid AI Attendance System...
python MAIN_UI.py

pause
```

---

# BAT File to Create EXE Using PyInstaller

Create another file named `BUILD_EXE.bat` and paste this:

```bat
@echo off
cd /d "%~dp0"

echo Installing PyInstaller...
pip install pyinstaller

echo Building EXE...
pyinstaller --noconfirm --onedir --windowed ^
--collect-all tensorflow ^
--collect-all keras ^
--collect-all cv2 ^
--hidden-import=PIL._tkinter_finder ^
--hidden-import=sklearn ^
--hidden-import=pandas ^
--hidden-import=numpy ^
--hidden-import=tkinter ^
--add-data "images;images" ^
--add-data "models;models" ^
--add-data "database;database" ^
MAIN_UI.py

echo.
echo EXE Generated Successfully.
echo Check the dist folder.

pause
```

---

# Folder Structure Example

Your project folder should look like this:

```text
Project Folder
│
├── MAIN_UI.py
├── requirements.txt
├── RUN_PROJECT.bat
├── BUILD_EXE.bat
│
├── images
├── models
├── database
└── other python files
```

---

# How to Run

## Method 1: Run Normally

1. Double-click `RUN_PROJECT.bat`
2. Project starts automatically

---

## Method 2: Create Shareable EXE

1. Double-click `BUILD_EXE.bat`
2. Wait until build completes
3. Open `dist` folder
4. Share the generated application folder

---

# Important Notes

* Install Python before running
* Tick "Add Python to PATH" during installation
* Keep all project files together
* Do not delete images/models/database folders
* If antivirus blocks EXE, allow it manually

---

# Optional: Hide CMD Window While Running

If you want fully GUI mode:

Replace:

```bat
python MAIN_UI.py
```

with:

```bat
pythonw MAIN_UI.py
```
