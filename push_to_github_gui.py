import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# === CONFIGURATION ===
GITHUB_REPO_URL = "https://github.com/<ton-nom-utilisateur>/<ton-repo>.git"
BRANCH_NAME = "main"

# === FONCTION PRINCIPALE ===
def push_to_github(progress_bar, status_label):
    try:
        progress_bar.start(10)
        status_label.config(text="🔄 Envoi des fichiers vers GitHub...")

        # Initialisation du dépôt
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "remote", "add", "origin", GITHUB_REPO_URL], check=True)

        # Ajout des fichiers
        subprocess.run(["git", "add", "."], check=True)

        # Commit avec date/heure
        commit_message = f"Auto commit du {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push vers GitHub
        subprocess.run(["git", "branch", "-M", BRANCH_NAME], check=True)
        subprocess.run(["git", "push", "-u", "origin", BRANCH_NAME], check=True)

        progress_bar.stop()
        status_label.config(text="✅ Fichiers poussés avec succès sur GitHub !")
        messagebox.showinfo("Succès", "Les fichiers et dossiers ont été envoyés avec succès sur GitHub !")

    except subprocess.CalledProcessError as e:
        progress_bar.stop()
        status_label.config(text="❌ Erreur lors du push GitHub.")
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
    except Exception as e:
        progress_bar.stop()
        status_label.config(text="❌ Erreur inattendue.")
        messagebox.showerror("Erreur", f"Une erreur inattendue est survenue : {e}")

# === INTERFACE GRAPHIQUE ===
def main():
    window = tk.Tk()
    window.title("GitHub Auto Push")
    window.geometry("400x250")
    window.resizable(False, False)

    title_label = tk.Label(window, text="🚀 Push Automatique vers GitHub", font=("Segoe UI", 13, "bold"))
    title_label.pack(pady=15)

    progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="indeterminate")
    progress_bar.pack(pady=20)

    status_label = tk.Label(window, text="En attente de l’action...", font=("Segoe UI", 10))
    status_label.pack(pady=10)

    def start_push():
        threading.Thread(target=push_to_github, args=(progress_bar, status_label), daemon=True).start()

    push_button = tk.Button(
        window,
        text="Pousser sur GitHub",
        command=start_push,
        bg="#0078D7",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="raised",
        bd=3,
        width=20
    )
    push_button.pack(pady=15)

    window.mainloop()

if __name__ == "__main__":
    main()
