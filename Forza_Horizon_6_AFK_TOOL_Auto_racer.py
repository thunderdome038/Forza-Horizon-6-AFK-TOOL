import sys
import subprocess

# --- AUTOMATISCHE DEPENDENCY CHECK ---
ontbrekende_packages = []

try:
    import pyautogui
except ImportError:
    ontbrekende_packages.append("pyautogui")

try:
    import pynput
except ImportError:
    ontbrekende_packages.append("pynput")

if ontbrekende_packages:
    import tkinter as tk
    from tkinter import messagebox
    
    root = tk.Tk()
    root.withdraw()
    
    install_command = f"pip install {' '.join(ontbrekende_packages)}"
    
    fout_bericht = (
        "⚠️ FOUT: Er ontbreken benodigde bibliotheken om dit script te draaien!\n\n"
        f"De volgende dependenties zijn niet gevonden:\n"
        f"{', '.join([f'- {p}' for p in ontbrekende_packages])}\n\n"
        f"Hoe op te lossen?\n"
        f"Open je Command Prompt (cmd) of Terminal en voer het volgende commando uit:\n\n"
        f"👉  {install_command}\n\n"
        "Zodra de installatie klaar is, kun je dit script opnieuw opstarten."
    )
    
    messagebox.showerror("Dependenties Ontbreken", fout_bericht)
    sys.exit(1)

# --- NORMALE IMPORTS ---
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import threading
import json
from pynput import keyboard

pyautogui.PAUSE = 0.01

# --- TAALDICTIONARY ---
TEXTS = {
    "nl": {
        "title": "Forza Horizon 6 - AFK RACER TOOL",
        "frame_input_key": " Nieuw Template bouwen ",
        "label_key": "Toets:",
        "label_tip": "(Typ zelf als de toets er niet bij staat)",
        "label_duration": "Duur (sec):",
        "check_game_mode": "Toets ingedrukt houden / Gasgeven",
        "btn_add_key": "Voeg Toets Toe",
        "frame_input_pauze": " Losse Pauze / Wachttijd Toevoegen ",
        "label_pauze_duration": "Duur pauze (sec):",
        "btn_add_pauze": "Voeg Pauze Toe",
        "frame_templates": " Standaard race - Vul alleen de tijd de rest van het script word automatisch aangemaakt. ",
        "label_fh5_duration": "Forza Race Duur (sec):",
        "btn_load_fh5": "Laad Forza Horizon 5 Template",
        "frame_program": " Jouw Programma ",
        "btn_delete": "Verwijder",
        "btn_clear_all": "Wis Alles",
        "btn_export": "💾 Export",
        "btn_import": "📂 Import",
        "frame_execute": " Uitvoeren ",
        "label_loops": "Aantal herhalingen:",
        "btn_start": "START PROGRAMMA",
        "status_standby": "Status: Standby. Druk op ESC om te stoppen.",
        "status_noodstop": "Status: Noodstop geactiveerd!",
        "status_start_in": "Status: Start over {} seconden... Klik snel in je game!",
        "status_loop": "Status: Herhaling {}/{}...",
        "status_done": "Status: Klaar / Standby.",
        "status_saved": "Status: Configuratie succesvol opgeslagen!",
        "status_loaded": "Status: Configuratie succesvol ingeladen!",
        "status_fh5_loaded": "Status: Forza Horizon 5 template succesvol geladen!",
        "err_duration_key": "Vul een geldig getal in voor de duur van de toets.",
        "err_duration_pauze": "Vul een geldig getal in voor de duur van de pauze.",
        "err_fh5_duration": "Vul een geldige raceduur in (getal groter dan 0).",
        "err_loops": "Vul een geldig aantal herhalingen in.",
        "warn_no_actions": "Voeg eerst een actie toe.",
        "warn_empty_export": "Er is geen programma om op te slaan.",
        "err_save_failed": "Kon het bestand niet opslaan:\n{}",
        "err_load_failed": "Dit bestand is geen geldige configuratie:\n{}",
        "pauze_text": "⏳ Rustpauze inlassen ({:.1f}s)",
        "key_text": "Toets '{}' ({}s){}"
    },
    "en": {
        "title": "Forza Horizon 6 - AFK RACER TOOL",
        "frame_input_key": " Add New Keystroke ",
        "label_key": "Key:",
        "label_tip": "(Type yourself if the key is not listed)",
        "label_duration": "Duration (sec):",
        "check_game_mode": "Hold down key (continuous repeat for in-game acceleration)",
        "btn_add_key": "Add Key",
        "frame_input_pauze": " Add Pause / Waiting Time ",
        "label_pauze_duration": "Pause duration (sec):",
        "btn_add_pauze": "Add Pause",
        "frame_templates": " Default Settings for race - Just add the duration of the race ",
        "label_fh5_duration": "Forza Race Duration (sec):",
        "btn_load_fh5": "Load Forza Horizon 5 Template",
        "frame_program": " Your Program ",
        "btn_delete": "Delete",
        "btn_clear_all": "Clear All",
        "btn_export": "💾 Export",
        "btn_import": "📂 Import",
        "frame_execute": " Execution ",
        "label_loops": "Number of loops:",
        "btn_start": "START PROGRAM",
        "status_standby": "Status: Standby. Press ESC to stop.",
        "status_noodstop": "Status: Emergency stop activated!",
        "status_start_in": "Status: Starting in {} seconds... Click into your game quickly!",
        "status_loop": "Status: Loop {}/{}...",
        "status_done": "Status: Done / Standby.",
        "status_saved": "Status: Configuration saved successfully!",
        "status_loaded": "Status: Configuration loaded successfully!",
        "status_fh5_loaded": "Status: Forza Horizon 5 template loaded successfully!",
        "err_duration_key": "Please enter a valid number for the key duration.",
        "err_duration_pauze": "Please enter a valid number for the pause duration.",
        "err_fh5_duration": "Please enter a valid race duration (number greater than 0).",
        "err_loops": "Please enter a valid number for loops.",
        "warn_no_actions": "Please add an action first.",
        "warn_empty_export": "There is no program to save.",
        "err_save_failed": "Could not save the file:\n{}",
        "err_load_failed": "This file is not a valid configuration:\n{}",
        "pauze_text": "⏳ Pause added ({:.1f}s)",
        "key_text": "Key '{}' ({}s){}"
    }
}

class LanguageSelectionDialog:
    def __init__(self):
        self.lang = None
        self.root = tk.Tk()
        self.root.title("Language / Taal")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        
        # Center window
        self.root.eval('tk::PlaceWindow . center')
        
        label = ttk.Label(self.root, text="Select your language / Kies uw taal:", font=("Arial", 11))
        label.pack(pady=15)
        
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)
        
        nl_btn = ttk.Button(btn_frame, text="Nederlands", command=lambda: self.select_lang("nl"))
        nl_btn.pack(side="left", padx=10)
        
        en_btn = ttk.Button(btn_frame, text="English", command=lambda: self.select_lang("en"))
        en_btn.pack(side="left", padx=10)
        
        self.root.mainloop()

    def select_lang(self, lang):
        self.lang = lang
        self.root.destroy()

class KeySimulatorGUI:
    def __init__(self, root, lang):
        self.root = root
        self.lang = lang
        self.t = TEXTS[lang] # Sla de gekozen taalset op
        
        self.root.title(self.t["title"])
        self.root.geometry("600x750")
        
        self.acties = []
        self.running = False
        
        self.listener = keyboard.Listener(on_press=self.check_noodstop)
        self.listener.start()
        
        self.create_widgets()

    def create_widgets(self):
        # --- Invoer Sectie: Toetsen ---
        input_frame = ttk.LabelFrame(self.root, text=self.t["frame_input_key"], padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text=self.t["label_key"]).grid(row=0, column=0, sticky="w", padx=5)
        self.toets_var = tk.StringVar(value="w")
        self.toets_menu = ttk.Combobox(input_frame, textvariable=self.toets_var, width=25)
        
        standaard_toetsen = ['w', 'a', 's', 'd', 'enter', 'space', 'backspace', 'tab', 'esc', 'shift', 'ctrl', 'alt']
        pijltjes = ['up', 'down', 'left', 'right']
        letters_cijfers = [chr(x) for x in range(97, 123) if chr(x) not in ['w','a','s','d']] + [str(x) for x in range(10)]
        functie_toetsen = [f'f{i}' for i in range(1, 13)]
        numpad = ['numpad0', 'numpad1', 'numpad2', 'numpad3', 'numpad4', 'numpad5', 'numpad6', 'numpad7', 'numpad8', 'numpad9', 'numpadenter']
        
        self.toets_menu['values'] = standaard_toetsen + pijltjes + letters_cijfers + functie_toetsen + numpad
        self.toets_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(input_frame, text=self.t["label_tip"], font=("Arial", 8, "italic")).grid(row=0, column=2, padx=5)
        
        ttk.Label(input_frame, text=self.t["label_duration"]).grid(row=1, column=0, sticky="w", padx=5)
        self.duur_entry = ttk.Entry(input_frame, width=28)
        self.duur_entry.insert(0, "2.0")
        self.duur_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        self.game_mode_var = tk.BooleanVar(value=True)
        self.game_mode_check = ttk.Checkbutton(input_frame, text=self.t["check_game_mode"], variable=self.game_mode_var)
        self.game_mode_check.grid(row=2, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        
        add_btn = ttk.Button(input_frame, text=self.t["btn_add_key"], command=self.add_actie)
        add_btn.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5, padx=5)

        # --- Invoer Sectie: Losse Pauze ---
        pauze_frame = ttk.LabelFrame(self.root, text=self.t["frame_input_pauze"], padding=10)
        pauze_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(pauze_frame, text=self.t["label_pauze_duration"]).grid(row=0, column=0, sticky="w", padx=5)
        self.pauze_duur_entry = ttk.Entry(pauze_frame, width=28)
        self.pauze_duur_entry.insert(0, "1.0")
        self.pauze_duur_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        add_pauze_btn = ttk.Button(pauze_frame, text=self.t["btn_add_pauze"], command=self.add_pauze)
        add_pauze_btn.grid(row=0, column=2, padx=10, sticky="w")

        # --- NIEUW: Invoer Sectie: Templates ---
        template_frame = ttk.LabelFrame(self.root, text=self.t["frame_templates"], padding=10)
        template_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(template_frame, text=self.t["label_fh5_duration"]).grid(row=0, column=0, sticky="w", padx=5)
        self.fh5_duur_entry = ttk.Entry(template_frame, width=28)
        self.fh5_duur_entry.insert(0, "60.0")
        self.fh5_duur_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        load_fh5_btn = ttk.Button(template_frame, text=self.t["btn_load_fh5"], command=self.load_fh5_template)
        load_fh5_btn.grid(row=0, column=2, padx=10, sticky="w")

        # --- Overzicht Sectie ---
        list_frame = ttk.LabelFrame(self.root, text=self.t["frame_program"], padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.listbox = tk.Listbox(list_frame, font=("Courier", 10))
        self.listbox.pack(fill="both", expand=True, side="left")
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(fill="y", side="right")
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill="y", side="right", padx=5)
        ttk.Button(btn_frame, text=self.t["btn_delete"], command=self.delete_actie).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text=self.t["btn_clear_all"], command=self.clear_all).pack(fill="x", pady=2)
        
        ttk.Separator(btn_frame, orient='horizontal').pack(fill='x', pady=10)
        
        ttk.Button(btn_frame, text=self.t["btn_export"], command=self.export_config).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text=self.t["btn_import"], command=self.import_config).pack(fill="x", pady=2)

        # --- Instellingen & Start ---
        control_frame = ttk.LabelFrame(self.root, text=self.t["frame_execute"], padding=10)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(control_frame, text=self.t["label_loops"]).grid(row=0, column=0, padx=5, pady=5)
        self.loop_entry = ttk.Entry(control_frame, width=8)
        self.loop_entry.insert(0, "1")
        self.loop_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.start_btn = tk.Button(control_frame, text=self.t["btn_start"], bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), command=self.start_thread)
        self.start_btn.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5, padx=5)
        
        self.status_label = ttk.Label(self.root, text=self.t["status_standby"], relief="sunken", anchor="w")
        self.status_label.pack(fill="x", side="bottom", pady=2)

    def add_actie(self):
        toets = self.toets_var.get().strip().lower()
        game_mode = self.game_mode_var.get()
        try:
            duur = float(self.duur_entry.get())
            if duur < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error / Fout", self.t["err_duration_key"])
            return
            
        self.acties.append({'toets': toets, 'duur': duur, 'game_mode': game_mode})
        modus_tekst = " (Game)" if game_mode else ""
        self.listbox.insert(tk.END, self.t["key_text"].format(toets, duur, modus_tekst))

    def add_pauze(self):
        try:
            duur = float(self.pauze_duur_entry.get())
            if duur < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error / Fout", self.t["err_duration_pauze"])
            return
            
        self.acties.append({'toets': '[PAUZE]', 'duur': duur, 'game_mode': False})
        self.listbox.insert(tk.END, self.t["pauze_text"].format(duur))

    def load_fh5_template(self):
        try:
            race_duur = float(self.fh5_duur_entry.get())
            if race_duur <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error / Fout", self.t["err_fh5_duration"])
            return

        # Vraag voor de zekerheid of de huidige lijst leeggemaakt moet worden
        self.clear_all()

        # Het template opbouwen met de dynamische 'w' duur
        fh5_template = [
            {"toets": "enter", "duur": 0.5, "game_mode": False},
            {"toets": "[PAUZE]", "duur": 5.0, "game_mode": False},
            {"toets": "w", "duur": race_duur, "game_mode": True}, # Dynamische tijd ingevuld
            {"toets": "[PAUZE]", "duur": 6.0, "game_mode": False},
            {"toets": "x", "duur": 1.0, "game_mode": False},
            {"toets": "[PAUZE]", "duur": 0.5, "game_mode": False},
            {"toets": "enter", "duur": 1.0, "game_mode": False},
            {"toets": "[PAUZE]", "duur": 0.5, "game_mode": False},
            {"toets": "enter", "duur": 1.0, "game_mode": False},
            {"toets": "[PAUZE]", "duur": 10.0, "game_mode": False}
        ]

        # Inladen in de interne lijst en de GUI listbox
        for actie in fh5_template:
            self.acties.append(actie)
            if actie['toets'] == '[PAUZE]':
                self.listbox.insert(tk.END, self.t["pauze_text"].format(actie['duur']))
            else:
                modus_tekst = " (Game)" if actie['game_mode'] else ""
                self.listbox.insert(tk.END, self.t["key_text"].format(actie['toets'], actie['duur'], modus_tekst))

        self.status_label.config(text=self.t["status_fh5_loaded"])

    def delete_actie(self):
        try:
            index = self.listbox.curselection()[0]
            self.listbox.delete(index)
            self.acties.pop(index)
        except IndexError:
            pass

    def clear_all(self):
        self.listbox.delete(0, tk.END)
        self.acties.clear()

    def export_config(self):
        if not self.acties:
            messagebox.showwarning("Warning / Waarschuwing", self.t["warn_empty_export"])
            return
            
        bestand = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Config" if self.lang == "en" else "Configuratie opslaan"
        )
        
        if bestand:
            try:
                with open(bestand, 'w') as f:
                    json.dump(self.acties, f, indent=4)
                self.status_label.config(text=self.t["status_saved"])
            except Exception as e:
                messagebox.showerror("Error / Fout", self.t["err_save_failed"].format(e))

    def import_config(self):
        bestand = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Open Config" if self.lang == "en" else "Configuratie openen"
        )
        
        if bestand:
            try:
                with open(bestand, 'r') as f:
                    geladen_acties = json.load(f)
                
                self.clear_all()
                
                for actie in geladen_acties:
                    if 'game_mode' not in actie:
                        actie['game_mode'] = False
                        
                    self.acties.append(actie)
                    
                    if actie['toets'] in ['[PAUZE]', '[PAUZE / WACHTEN]']:
                        actie['toets'] = '[PAUZE]'
                        self.listbox.insert(tk.END, self.t["pauze_text"].format(actie['duur']))
                    else:
                        modus_tekst = " (Game)" if actie['game_mode'] else ""
                        self.listbox.insert(tk.END, self.t["key_text"].format(actie['toets'], actie['duur'], modus_tekst))
                    
                self.status_label.config(text=self.t["status_loaded"])
            except Exception as e:
                messagebox.showerror("Error / Fout", self.t["err_load_failed"].format(e))

    def check_noodstop(self, key):
        if key == keyboard.Key.esc and self.running:
            self.running = False
            self.status_label.config(text=self.t["status_noodstop"])

    def start_thread(self):
        if not self.acties:
            messagebox.showwarning("Warning / Waarschuwing", self.t["warn_no_actions"])
            return
        if self.running:
            return
            
        t = threading.Thread(target=self.run_simulation)
        t.daemon = True
        t.start()

    def run_simulation(self):
        try:
            loops = int(self.loop_entry.get())
        except ValueError:
            messagebox.showerror("Error / Fout", self.t["err_loops"])
            return

        self.running = True
        self.start_btn.config(state="disabled", bg="#95a5a6")
        
        for i in range(3, 0, -1):
            if not self.running: break
            self.status_label.config(text=self.t["status_start_in"].format(i))
            self.root.update()
            time.sleep(1)
            
        for l in range(loops):
            if not self.running: break
            self.status_label.config(text=self.t["status_loop"].format(l+1, loops))
            self.root.update()
            
            for index, actie in enumerate(self.acties):
                if not self.running: break
                
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(index)
                self.root.update()
                
                eind_tijd = time.time() + actie['duur']
                
                if actie['toets'] == '[PAUZE]':
                    while time.time() < eind_tijd and self.running:
                        time.sleep(0.05)
                else:
                    try:
                        if actie['game_mode']:
                            while time.time() < eind_tijd and self.running:
                                pyautogui.keyDown(actie['toets'])
                                time.sleep(0.02)
                        else:
                            pyautogui.keyDown(actie['toets'])
                            while time.time() < eind_tijd and self.running:
                                time.sleep(0.05)
                    except Exception as e:
                        print(f"Error: {e}")
                    finally:
                        try:
                            pyautogui.keyUp(actie['toets'])
                        except:
                            pass
                    
                time.sleep(0.1)
                
        self.listbox.selection_clear(0, tk.END)
        self.running = False
        self.start_btn.config(state="normal", bg="#2ecc71")
        self.status_label.config(text=self.t["status_done"])

if __name__ == "__main__":
    # 1. Start taalkeuzemenu
    selector = LanguageSelectionDialog()
    
    # 2. Start de hoofdapp mits er een taal gekozen is (dus niet via kruisje gesloten)
    if selector.lang:
        root = tk.Tk()
        app = KeySimulatorGUI(root, selector.lang)
        root.mainloop()