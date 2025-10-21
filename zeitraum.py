import tkinter as tk
from tkinter import messagebox
from datetime import datetime


def toggle_individuell():
    if var_individuell.get():
        eintrag_individuell.config(state="normal")
    else:
        eintrag_individuell.config(state="disabled")


def toggle_mwst():
    if var_mwst.get():
        eintrag_mwst.config(state="normal")
    else:
        eintrag_mwst.config(state="disabled")


def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    messagebox.showinfo("Kopiert", "Das Ergebnis wurde in die Zwischenablage kopiert.")


def berechnen():
    datum1_str = eintrag_datum1.get().strip()
    datum2_str = eintrag_datum2.get().strip()
    betrag_text = eintrag_betrag.get().strip()

    if not datum1_str or not datum2_str or not betrag_text:
        messagebox.showerror("Fehler", "Bitte beide Daten und Betrag eingeben!")
        return

    try:
        datum1 = datetime.strptime(datum1_str, "%d.%m.%Y")
        datum2 = datetime.strptime(datum2_str, "%d.%m.%Y")
    except ValueError:
        messagebox.showerror(
            "Fehler", "Falsches Datumsformat! Bitte dd.mm.yyyy verwenden."
        )
        return

    if datum2 < datum1:
        messagebox.showerror(
            "Fehler", "Das zweite Datum darf nicht vor dem ersten liegen."
        )
        return

    try:
        betrag = float(betrag_text)
    except ValueError:
        messagebox.showerror("Fehler", "Betrag muss eine gültige Zahl sein.")
        return

    tage_gesamt = (datum2 - datum1).days + 1
    betrag_pro_tag = betrag / tage_gesamt

    if var_mwst.get():
        try:
            mwst = float(eintrag_mwst.get().strip())
            if mwst < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Fehler", "Bitte gültigen MwSt-Wert eingeben (≥ 0).")
            return
        mwst_faktor = 1 + mwst / 100
    else:
        mwst = 0.0
        mwst_faktor = 1.0

    if var_individuell.get():
        try:
            individuell_tage = float(eintrag_individuell.get().strip())
            if individuell_tage <= 0:
                messagebox.showerror(
                    "Fehler", "Individueller Zeitraum muss größer 0 sein."
                )
                return
        except ValueError:
            messagebox.showerror(
                "Fehler", "Ungültiger Wert für individuellen Zeitraum."
            )
            return
    else:
        individuell_tage = None

    for widget in ergebnisse_container.winfo_children():
        widget.destroy()

    def add_erg(text):
        frame = tk.Frame(ergebnisse_container)
        frame.pack(fill="x", pady=4)
        label = tk.Label(frame, text=text, justify="left")
        label.pack(side="left")
        btn = tk.Button(
            frame, text="Kopieren", command=lambda t=text: copy_to_clipboard(t)
        )
        btn.pack(side="right")

    text1 = (
        f"Gesamter Zeitraum ({tage_gesamt} Tage):\n"
        f"  Ohne MwSt: {betrag:.2f} €\n"
        f"  Mit {mwst:.1f}% MwSt: {betrag * mwst_faktor:.2f} €"
    )
    add_erg(text1)

    if individuell_tage is not None:
        wert_indi = betrag_pro_tag * individuell_tage
        text2 = (
            f"Individueller Zeitraum ({individuell_tage} Tage):\n"
            f"  Ohne MwSt: {wert_indi:.2f} €\n"
            f"  Mit {mwst:.1f}% MwSt: {wert_indi * mwst_faktor:.2f} €"
        )
        add_erg(text2)

    text3 = (
        f"Ein Tag:\n"
        f"  Ohne MwSt: {betrag_pro_tag:.2f} €\n"
        f"  Mit {mwst:.1f}% MwSt: {betrag_pro_tag * mwst_faktor:.2f} €"
    )
    add_erg(text3)

    wert_standard = betrag_pro_tag * 30.5
    text4 = (
        f"Standardzeitraum (30,5 Tage):\n"
        f"  Ohne MwSt: {wert_standard:.2f} €\n"
        f"  Mit {mwst:.1f}% MwSt: {wert_standard * mwst_faktor:.2f} €"
    )
    add_erg(text4)


root = tk.Tk()
root.title("Zeitraumrechner mit MwSt")
root.geometry("650x500")
root.resizable(False, False)

# Datum Frame nebeneinander mit Bindestrich
frame_datum = tk.Frame(root)
frame_datum.pack(pady=3)

tk.Label(frame_datum, text="Datum 1 (dd.mm.yyyy):").pack(side=tk.LEFT)
eintrag_datum1 = tk.Entry(frame_datum, width=12)
eintrag_datum1.pack(side=tk.LEFT, padx=(5, 0))

tk.Label(frame_datum, text=" - ").pack(side=tk.LEFT, padx=5)

tk.Label(frame_datum, text="Datum 2 (dd.mm.yyyy):").pack(side=tk.LEFT)
eintrag_datum2 = tk.Entry(frame_datum, width=12)
eintrag_datum2.pack(side=tk.LEFT, padx=(5, 0))

# Betrag Eingabe
tk.Label(root, text="Gesamtbetrag (€):").pack(pady=3)
eintrag_betrag = tk.Entry(root, width=20)
eintrag_betrag.pack()

# MwSt Checkbox + Eingabe, Beschriftung mit (in %) im Text
var_mwst = tk.IntVar(value=0)
frame_mwst = tk.Frame(root)
frame_mwst.pack(pady=5)
check_mwst = tk.Checkbutton(
    frame_mwst,
    text="Mehrwertsteuer angeben (%)",
    variable=var_mwst,
    command=toggle_mwst,
)
check_mwst.pack(side="left")
eintrag_mwst = tk.Entry(frame_mwst, width=8, state="disabled")
eintrag_mwst.insert(0, "19")
eintrag_mwst.pack(side="left", padx=5)

# Individueller Zeitraum Checkbox + Eingabe
var_individuell = tk.IntVar(value=0)
frame_individuell = tk.Frame(root)
frame_individuell.pack(pady=5)
check_individuell = tk.Checkbutton(
    frame_individuell,
    text="Individueller Zeitraum (Tage)",
    variable=var_individuell,
    command=toggle_individuell,
)
check_individuell.pack(side="left")
eintrag_individuell = tk.Entry(frame_individuell, width=10, state="disabled")
eintrag_individuell.pack(side="left", padx=5)

tk.Button(root, text="Berechnen", command=berechnen).pack(pady=12)

ergebnisse_container = tk.Frame(root)
ergebnisse_container.pack(fill="both", expand=True, padx=10)

root.mainloop()
