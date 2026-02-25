import sqlite3
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox, ttk


conn = sqlite3.connect("vaccination.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS animaux (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    type_animal TEXT,
    commune TEXT,
    type_vaccin TEXT,
    date_vaccination TEXT,
    duree_validite INTEGER
)
""")
conn.commit()
conn.close()

def ajouter_animal():
    nom = entry_nom.get()
    type_animal = combo_type.get()
    commune = entry_commune.get()
    type_vaccin = entry_vaccin.get()
    duree = entry_duree.get()

    if nom == "" or commune == "" or type_vaccin == "" or duree == "":
        messagebox.showerror("Erreur", "Remplir tous les champs")
        return

    conn = sqlite3.connect("vaccination.db")
    cursor = conn.cursor()

    date_vaccination = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
    INSERT INTO animaux (nom, type_animal, commune, type_vaccin, date_vaccination, duree_validite)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (nom, type_animal, commune, type_vaccin, date_vaccination, int(duree)))

    conn.commit()
    conn.close()

    messagebox.showinfo("Succès", "Animal enregistré")
    afficher_animaux()

def afficher_animaux():
    for row in table.get_children():
        table.delete(row)

    conn = sqlite3.connect("vaccination.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animaux")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        table.insert("", tk.END, values=row)

def verifier_expiration():
    conn = sqlite3.connect("vaccination.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animaux")
    animaux = cursor.fetchall()
    conn.close()

    for animal in animaux:
        id, nom, type_animal, commune, type_vaccin, date_vaccination, duree = animal

        date_vacc = datetime.strptime(date_vaccination, "%Y-%m-%d")
        date_exp = date_vacc + timedelta(days=duree)
        jours_restants = (date_exp - datetime.now()).days

        if jours_restants in [1, 2]:
            messagebox.showwarning(
                "ALERTE",
                f"{nom} ({type_animal}) - {commune}\n"
                f"Vaccin: {type_vaccin}\n"
                f"Expire dans {jours_restants} jour(s)"
            )



root = tk.Tk()
root.title("Calendrier Vaccination Animaux")
root.geometry("900x500")

# Champs
tk.Label(root, text="Nom Animal").pack()
entry_nom = tk.Entry(root)
entry_nom.pack()

tk.Label(root, text="Type Animal").pack()
combo_type = ttk.Combobox(root, values=["Chat", "Chien"])
combo_type.pack()

tk.Label(root, text="Commune").pack()
entry_commune = tk.Entry(root)
entry_commune.pack()

tk.Label(root, text="Type Vaccin").pack()
entry_vaccin = tk.Entry(root)
entry_vaccin.pack()

tk.Label(root, text="Durée validité (jours)").pack()
entry_duree = tk.Entry(root)
entry_duree.pack()

tk.Button(root, text="Ajouter Animal", command=ajouter_animal).pack(pady=5)
tk.Button(root, text="Vérifier Expiration", command=verifier_expiration).pack(pady=5)

# Tableau
columns = ("ID", "Nom", "Type", "Commune", "Vaccin", "Date", "Durée")
table = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col)

table.pack(fill="both", expand=True)

afficher_animaux()

root.mainloop()
