import tkinter as tk
from tkinter import ttk
import mysql.connector
import csv

boutique = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123",
    database="Boutique"
)

cursor = boutique.cursor()

class Boutique:

    def __init__(self):

        self.Windows = tk.Tk()
        self.Windows.title("Gestion des stocks")
        self.Windows.geometry("800x500")
        self.Windows.resizable(False, False)
        self.Windows.iconbitmap("ico.ico")
        self.interface()

    def actualiser(self):
        self.tree.delete(*self.tree.get_children())
        for produit in self.liste_produits():
            self.tree.insert("", "end", text=produit[0], values=(produit[1], produit[2], produit[3], produit[4], self.nom_categorie(produit[5])))
        
        self.category_cbox = ttk.Combobox(self.Windows, values=self.liste_categories())

    def filter_categories(self):
        self.tree.delete(*self.tree.get_children())
        self.info_label.config(text="Aucun produit ne correspond", fg="red")
        for produit in self.liste_produits():
            if self.nom_categorie(produit[5]) == self.category_cbox.get():
                self.tree.insert("", "end", text=produit[0], values=(produit[1], produit[2], produit[3], produit[4], self.nom_categorie(produit[5])))
                self.info_label.config(text="Filre appliqué", fg="green")

    def reinitialiser_les_filtres(self):
        self.actualiser()
        self.info_label.config(text="Filtre réinitialisé", fg="green")
    def check_produit(self):
        
        self.nom = self.name_entry.get()
        self.description = self.description_entry.get()
        self.prix = self.price_entry.get()
        self.quantite = self.quantity_entry.get()
        self.categorie = self.category_cbox.get()

        if self.nom == "" or self.description == "" or self.prix == "" or self.quantite == "" or self.categorie == "":
            self.info_label.config(text="Veuillez remplir tous les champs", fg="red")
            return False
        if not self.prix.isdigit():
            self.info_label.config(text="Le prix doit être un nombre", fg="red")
            return False
        if not self.quantite.isdigit():
            self.info_label.config(text="La quantité doit être un nombre", fg="red")
            return False
        if (self.categorie,) not in self.liste_categories():
            self.ajouter_categorie()
            self.info_label.config(text="La catégorie a été ajoutée", fg="green")
        return True
    
    def check_selection(self):

        # Vérifier si un produit est sélectionné

        if self.tree.selection() == ():
            self.info_label.config(text="Veuillez sélectionner un produit", fg="red")
            return False
        self.id = self.tree.item(self.tree.selection())["text"]
        return True            

    def ajouter_produit(self):
        """
        ajouter un produit dans la base de données et actualiser la liste
        """
        if self.check_produit():
            query = "INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES (%s, %s, %s, %s, %s)"
            values = (self.nom, self.description, self.prix, self.quantite, self.id_categorie(self.categorie))
            cursor.execute(query, values)
            boutique.commit()
            self.actualiser()
            self.info_label.config (text="Le produit a été ajouté avec succès", fg="green")

    def supprimer_produit(self):
        if self.check_selection():
            cursor.execute("DELETE FROM produit WHERE id=%s", (self.id,))
            boutique.commit()
            self.actualiser()
            self.info_label.config(text="Le produit a été supprimé", fg="green")

    def modifier_produit(self):     # Modifier un produit dans la base de données
        if self.check_produit():
            if self.check_selection():

                query = "UPDATE produit SET nom=%s, description=%s, prix=%s, quantite=%s, id_categorie=%s WHERE id=%s"
                values = (self.nom, self.description, self.prix, self.quantite, self.id_categorie(self.categorie), self.id)
                cursor.execute(query, values)
                boutique.commit()
                self.actualiser()
                self.info_label.config(text="Le produit a été modifié", fg="green")


    def liste_categories(self):
        cursor.execute("SELECT nom FROM categorie")
        categorie = cursor.fetchall()
        return categorie
    
    def nom_categorie(self, id):
        cursor.execute("SELECT nom FROM categorie WHERE id=%s", (id,))
        categorie = cursor.fetchone()
        return categorie[0]
    
    def id_categorie(self, nom):
        cursor.execute("SELECT id FROM categorie WHERE nom=%s", (nom,))
        categorie = cursor.fetchone()
        return categorie[0]
    
    def ajouter_categorie(self):
        cursor.execute("INSERT INTO categorie (nom) VALUES (%s)", (self.categorie,))
        boutique.commit()

    def liste_produits(self):
        query = "SELECT * FROM produit"
        cursor.execute(query)
        produits = cursor.fetchall()
        return produits
    
    def export_csv(self):
        with open("produits.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Nom", "Description", "Prix", "Quantite", "Categorie"])

            for produit in self.liste_produits():
                writer.writerow([produit[0], produit[1], produit[2], produit[3], produit[4], self.nom_categorie(produit[5])])


        self.info_label.config(text="La liste des produits a été exportée avec succès", fg="green")

    def interface(self):
        self.tree = ttk.Treeview(self.Windows, columns=("Nom", "Description", "Prix", "Quantite", "Categorie"), show="headings")
        self.tree.heading("#0", text="ID")
        self.tree.column("#0", minwidth=0, width=30)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=145, anchor="center", minwidth=0)

        self.actualiser()

        self.tree.grid(row=0, column=0, columnspan=5, padx=20, pady=50)
        self.info_label = tk.Label(self.Windows, text="", font=("Arial", 12))
        self.info_label.grid(row=9, column=0, columnspan=5, sticky="NSEW", pady=5)



        self.btn_ajouter = tk.Button(self.Windows, text="Ajouter produit", command=self.ajouter_produit,background="red", fg="white") # Création du bouton ajouter
        self.btn_ajouter.grid(row=1, column=2, sticky="NSEW", padx=20)

        self.btn_modifier = tk.Button(self.Windows, text="Modifier produit", command=self.modifier_produit,background="red", fg="white")
        self.btn_modifier.grid(row=2, column=2, sticky="NSEW", padx=20)

        self.btn_supprimer = tk.Button(self.Windows, text="Supprimer produit", command=self.supprimer_produit,background="red", fg="white")
        self.btn_supprimer.grid(row=3, column=2, sticky="NSEW", padx=20)

        self.btn_exporter = tk.Button(self.Windows, text="Exporter en CSV", command=self.export_csv,background="red", fg="white")
        self.btn_exporter.grid(row=4, column=2, sticky="NSEW", padx=20)


        self.btn_filtrer = tk.Button(self.Windows, text="Filtrer par catégorie", command=self.filter_categories,background="red", fg="white")
        self.btn_filtrer.grid(row=5, column=2, sticky="NSEW", padx=20)

        self.btn_reset = tk.Button(self.Windows, text="Réinitialiser les filtres", command=self.reinitialiser_les_filtres,background="red", fg="white")
        self.btn_reset.grid(row=6, column=2, sticky="NSEW", padx=20)


        tk.Label(self.Windows, text="Nom").grid(row=1, column=0)
        self.name_entry = tk.Entry(self.Windows)
        self.name_entry.grid(row=1, column=1, sticky="NSEW", pady=5)

        tk.Label(self.Windows, text="Description").grid(row=2, column=0)
        self.description_entry = tk.Entry(self.Windows, width=30)
        self.description_entry.grid(row=2, column=1, sticky="NSEW", pady=5)

        tk.Label(self.Windows, text="Prix").grid(row=3, column=0)
        self.price_entry = tk.Entry(self.Windows)
        self.price_entry.grid(row=3, column=1, sticky="NSEW", pady=5)

        tk.Label(self.Windows, text="Quantite").grid(row=4, column=0)
        self.quantity_entry = tk.Entry(self.Windows)
        self.quantity_entry.grid(row=4, column=1, sticky="NSEW", pady=5)

        tk.Label(self.Windows, text="Categorie").grid(row=5, column=0)
        self.categorie_entry = ttk.Combobox(self.Windows, values=self.liste_categories())
        self.categorie_entry.grid(row=5, column=1, sticky="NSEW", pady=5)

        self.Windows.mainloop()

Boutique()