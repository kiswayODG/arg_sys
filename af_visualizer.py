import tkinter as tk
from tkinter import filedialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utilities import file_reader, Semantic
from controller import *
from argSys import ArgSys


def extract_edges(attacks):
    # Transforme la structure de données en une liste de tuples
    edges = [(attacker, attacked) for attacker, attacked_set in attacks.items() for attacked in attacked_set]
    return edges



def load_file():
    file_path = filedialog.askopenfilename(
        title="Choisir un fichier AF",
        filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
    )
    if file_path:
        file_label.config(text=f"Fichier chargé : {file_path}")
         
        arguments, attaques = file_reader(file_path) 
        ArgSys.set_attaques(attaques)
        ArgSys.set_arguments(arguments)
        
        print(f"chargé arg {arguments}, att {attaques}")
        return file_path
    return None

# Fonction pour exécuter la sémantique choisie
def execute():
    semantic = semantic_var.get()
   
    argument = argument_entry.get()
    if not file_label.cget("text").startswith("Fichier chargé"):
        messagebox.showerror("Erreur", "Veuillez charger un fichier AF.")
        return
    if semantic in ["DC-CO", "DS-CO", "DC-ST", "DS-ST"] and not argument:
        messagebox.showerror("Erreur", "Veuillez fournir un argument pour cette sémantique.")
        return
    if semantic in ["DC-CO", "DS-CO", "DC-ST", "DS-ST"]:
        result = handle_semanticfrom_screen(semantic,argument)
    else:
        result = handle_semanticfrom_screen(semantic)
    print(result,'icii')
        
    
    file_path = file_label.cget("text").split(":")[1].strip()
    result = f"Résultat pour {semantic} sur {file_path} \n {result}"  # Simule un résultat
    if argument:
        result += f" avec l'argument '{argument}'"
    result_label.config(text=result)

    visualize_graph()



def visualize_graph():
    
    for widget in graph_frame.winfo_children():
        widget.destroy()
        
    edges = extract_edges(ArgSys.attaques)  # Obtenir les tuples des attaques
    G = nx.DiGraph()  # Créer un graphe orienté
    G.add_edges_from(edges)  # Ajouter les arêtes  # Exemples d'attaques

    fig, ax = plt.subplots(figsize=(5, 4))
    nx.draw(G, with_labels=True, node_color='skyblue', ax=ax, node_size=1500, font_size=12)

    # Intégrer Matplotlib dans Tkinter
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()

# Création de la fenêtre principale
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
    


def toggle_argument_entry(*args):
    """Active ou désactive le champ d'entrée d'argument en fonction de la sémantique choisie."""
    selected_semantic = semantic_var.get()
    if selected_semantic.startswith("D"):
        argument_entry.config(state=tk.NORMAL)  
    else:
        argument_entry.delete(0, tk.END)  
        argument_entry.config(state=tk.DISABLED)  

semantic_var.trace("w", toggle_argument_entry)

# Zone pour entrer un argument (facultatif)
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
result_label = tk.Label(result_frame, text="Résultats affichés ici", fg="blue")
result_label.pack()

# Frame pour la visualisation des graphes
graph_frame = tk.LabelFrame(root, text="Visualisation du graphe", padx=10, pady=10)
graph_frame.pack(fill=tk.BOTH, expand=True)


root.mainloop()
