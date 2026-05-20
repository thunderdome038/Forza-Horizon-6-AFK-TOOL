# Forza Horizon 6 - AFK Racer Tool 🏎️💨

A handy automation tool featuring a graphical user interface (GUI) designed for Forza Horizon. It allows you to program macros and key combinations for AFK (Away From Keyboard) racing. The tool supports both manual configurations and automatic templates, and is fully bilingual (Dutch & English).

---

## 📌 Features

*   **Automated Dependency Check:** The script automatically checks if the required libraries are installed. If any are missing, it immediately displays a pop-up window with the correct setup instructions.
*   **Game Mode Activation:** A specialized mode for in-game acceleration where the key is pressed virtually in a rapid, continuous loop to prevent any input loss.
*   **Forza Templates:** Ready-to-use presets for Forza races where you only need to specify the total duration of the race.
*   **Import & Export:** Easily save your custom macro configurations as `.json` files to reuse or share them later.
*   **Emergency Stop:** Safely interrupt and stop the simulation at any given time by simply pressing the **`ESC`** key.

---

## ⚙️ Requirements

To run this script, you need **Python 3.x** along with a few external libraries that handle the keyboard and mouse simulations.

### Core Libraries (Built-in with Python):
*   `tkinter` (For the graphical user interface)
*   `sys`, `subprocess`, `time`, `threading`, `json`

### External Dependencies:
*   `pyautogui` (For simulating keystrokes)
*   `pynput` (For capturing the emergency stop / ESC key)

---

## 🚀 Installation Steps

Follow these steps to get the tool up and running on your computer.

### Step 1: Open your Terminal or Command Prompt
*   **Windows:** Press the `Windows Key`, type `cmd` or `PowerShell`, and hit Enter.
*   **Mac/Linux:** Open the `Terminal` application.

### Step 2: Install the required libraries
Copy and paste the following command into your terminal and press Enter:

```bash
pip install pyautogui pynput
