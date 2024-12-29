import tkinter as tk
from tkinter import filedialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utilities import file_reader, Semantic,choose_random_extension
from controller import *
from argSys import ArgSys

def extract_edges(attacks):
    edges = [(attacker, attacked) for attacker, attacked_set in attacks.items() for attacked in attacked_set]
    return edges

def load_file():
    file_path = filedialog.askopenfilename(
        title="Choisir un fichier AF",
        filetypes=[("Fichiers contenant AF", "*.apx"), ("Tous les fichiers", "*.*")]
    )
    if file_path:
        file_label.config(text=f"Fichier chargé : {file_path}")
        arguments, attaques = file_reader(file_path)
        ArgSys.set_attaques(attaques)
        ArgSys.set_arguments(arguments)
        print(f"chargé arg {arguments}, att {attaques}")
        return file_path
    return None

def execute():
    global all_extensions
    semantic = semantic_var.get()
    all_extensions = []

    argument = argument_entry.get()
    if not file_label.cget("text").startswith("Fichier chargé"):
        messagebox.showerror("Erreur", "Veuillez charger un fichier AF.")
        return
    if semantic in ["DC-CO", "DS-CO", "DC-ST", "DS-ST"] and not argument:
        messagebox.showerror("Erreur", "Veuillez fournir un argument pour cette sémantique.")
        return
    if semantic in ["DC-CO", "DS-CO", "DC-ST", "DS-ST"]:
        result = handle_semanticfrom_screen(semantic, argument)
    else:
        all_extensions = handle_semanticfrom_screen(semantic)
        result = choose_random_extension(all_extensions)

    file_path = file_label.cget("text").split(":")[1].strip()
    result = f"Résultat pour {semantic} \n {result}"
    if argument:
        result += f" avec l'argument '{argument}'"
    result_label.config(text=result)
    visualize_graph()

def visualize_graph():
    for widget in graph_frame.winfo_children():
        widget.destroy()

    edges = extract_edges(ArgSys.attaques)
    G = nx.DiGraph()
    G.add_edges_from(edges)

    fig, ax = plt.subplots(figsize=(5, 4))
    nx.draw(G, with_labels=True, node_color='skyblue', ax=ax, node_size=1500, font_size=12)

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()

def toggle_argument_entry(*args):
    selected_semantic = semantic_var.get()
    if selected_semantic.startswith("D"):
        argument_entry.config(state=tk.NORMAL)
    else:
        argument_entry.delete(0, tk.END)
        argument_entry.config(state=tk.DISABLED)
    toggle_show_extensions_button()

def toggle_show_extensions_button():
    selected_semantic = semantic_var.get()
    if selected_semantic in ["DC-CO", "DS-CO", "DC-ST", "DS-ST"]:
        show_extensions_button.config(state=tk.DISABLED)
    else:
        show_extensions_button.config(state=tk.NORMAL)

def show_all_extensions():
    if not all_extensions:
        messagebox.showinfo("Information", "Aucune extension disponible. Exécutez une sémantique d'abord.")
        return
    all_ext_label.config(text="------\n".join(map(str, all_extensions)))

# Fenêtre principale
root = tk.Tk()
root.title("Solveur AF - Visualisation de Graphe")

# Widgets pour le fichier
file_frame = tk.Frame(root, padx=10, pady=5)
file_frame.pack(fill=tk.X)
tk.Button(file_frame, text="Charger un fichier", command=load_file).pack(side=tk.LEFT)
file_label = tk.Label(file_frame, text="Aucun fichier chargé")
file_label.pack(side=tk.LEFT, padx=10)

# Widgets pour choisir la sémantique
semantic_frame = tk.Frame(root, padx=10, pady=5)
semantic_frame.pack(fill=tk.X)
tk.Label(semantic_frame, text="Choisir la sémantique :").pack(side=tk.LEFT)
semantic_var = tk.StringVar(value="SE-CO")
options = ["SE-CO", "SE-ST", "DC-CO", "DS-CO", "DC-ST", "DS-ST"]
for option in options:
    tk.Radiobutton(semantic_frame, text=option, variable=semantic_var, value=option).pack(side=tk.LEFT)
semantic_var.trace("w", toggle_argument_entry)

# Zone pour entrer un argument
argument_frame = tk.Frame(root, padx=10, pady=5)
argument_frame.pack(fill=tk.X)
tk.Label(argument_frame, text="Argument (si nécessaire) :").pack(side=tk.LEFT)
argument_entry = tk.Entry(argument_frame)
argument_entry.pack(side=tk.LEFT)
argument_entry.config(state=tk.DISABLED)

# Bouton pour exécuter
execute_button = tk.Button(root, text="Exécuter", command=execute, bg="green", fg="white")
execute_button.pack(pady=10)

# Affichage des résultats
result_frame = tk.Frame(root, padx=10, pady=5)
result_frame.pack(fill=tk.X)

#bouton et affichage pour toutes les extensions
show_extensions_button = tk.Button(root, text="Afficher toutes les extensions", command=show_all_extensions, bg="green", fg="white")
show_extensions_button.pack(pady=5)
result_label = tk.Label(result_frame, text="Résultats :", fg="blue")
all_ext_label = tk.Label(result_frame, fg="black")


result_label.pack()
all_ext_label.pack()

# Frame pour la visualisation des graphes
graph_frame = tk.LabelFrame(root, text="Visualisation du graphe", padx=10, pady=10)
graph_frame.pack(fill=tk.BOTH, expand=True)




root.mainloop()
