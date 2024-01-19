import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import shutil
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from constants import EXTENSION, TO_AVOID, WHITE, BLACK, FONT_NAME



def move_files_with_progress(folder_path, progress_bar):
    recap_path = os.path.join(folder_path, 'recap.csv')
    total_files = sum([len(files) for _, _, files in os.walk(folder_path)])

    try:
        progress_bar.config(maximum=total_files, mode='determinate')
        progress_bar.start()

        for filename in sorted(os.listdir(folder_path)):
            file_name = filename.split(".")[0]
            file_path = os.path.join(folder_path, filename)
            file_size = os.path.getsize(file_path)
            file_type = filename.split(".")[-1]

            if file_type in EXTENSION.keys():
                subfolder = EXTENSION[file_type]
            else:
                if file_type in TO_AVOID:
                    print("not valid extension")
                else:
                    continue

            subfolder_path = os.path.join(folder_path, subfolder)
            if not os.path.exists(subfolder_path):
                os.mkdir(subfolder_path)

            try:
                # Apre il file di recap solo quando è necessario scriverci
                with open(recap_path, 'a', newline='') as recap_file:
                    writer = csv.writer(recap_file)

                    shutil.move(file_path, os.path.join(subfolder_path, filename))

                    # Stampa informazioni del file
                    print(f'{file_name} type:{file_type} size:{file_size}B')

                    # Aggiunta informazioni del file al file recap.csv
                    writer.writerow([file_name, file_type, file_size])

                    progress_bar.step(1)
                    root.update_idletasks()

            except shutil.SameFileError:
                pass

    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore durante l'organizzazione: {e}")

    finally:
        progress_bar.stop()
        progress_bar.config(mode='indeterminate')
        print("Organizzazione completata.")
        messagebox.showinfo("Operazione completata", "Organizzazione completata con successo!")
        root.destroy()



def select_folder():
    folder_path = filedialog.askdirectory(title="Seleziona la cartella che vuoi Riorganizzare")
    label_cartella.config(text=f"Cartella selezionata: {folder_path}")
    avvia_organizzazione.config(command=lambda: move_files_with_progress(folder_path, progress_bar))
    avvia_organizzazione.config(state=tk.NORMAL)


# Creare una finestra principale
root = tk.Tk()
root.title("Organizza File")
root.config(padx=100, pady=50, bg=BLACK)

title_label = tk.Label(text="File Organizer", bg=BLACK, fg=WHITE, font=(FONT_NAME, 45, "bold"))
title_label.grid(column=2, row=0)

canvas = tk.Canvas(width=280, height=280, background="#f5f5f5", highlightthickness=0)
tomatoImg = tk.PhotoImage(file=os.path.abspath("logo_small.png"))
canvas.create_image(140, 140, image=tomatoImg)
canvas.grid(row=1, column=2, pady=20)

label_descrizione = tk.Label(root,
                             text="Seleziona la cartella che vuoi Riorganizzare:",
                             font=(FONT_NAME, 14), highlightthickness=0,
                             bg=BLACK, fg=WHITE)
label_descrizione.grid(row=2, column=2, pady=10)

label_cartella = tk.Label(root, text="", highlightthickness=0, bg=BLACK, fg=WHITE)
label_cartella.grid(row=3, column=2, pady=10)

pulsante_sfoglia = tk.Button(root, text="Sfoglia", command=select_folder, height=2, width=20, bg=BLACK, fg=WHITE)
pulsante_sfoglia.grid(row=4, column=2, pady=10)

avvia_organizzazione = tk.Button(root, text="Avvia Organizzazione", state=tk.DISABLED, height=2, width=20, bg=BLACK, fg=WHITE)
avvia_organizzazione.grid(row=5, column=2, pady=10)

progress_bar = Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='indeterminate')
progress_bar.grid(row=6, column=2, pady=10)

root.mainloop()


