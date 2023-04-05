# gestion_de_stock

Il s'agit d'un script Python qui utilise la bibliothèque tkinter pour créer une application GUI permettant de gérer les stocks d'un magasin. L'application interagit avec une base de données MySQL pour stocker et récupérer des données. Le script définit plusieurs fonctions pour ajouter, supprimer et modifier les produits et les catégories dans la base de données, ainsi que pour récupérer les données à afficher dans l'interface graphique.

Le script définit une classe appelée GestionStockApp, qui hérite de la classe tk.Tk et sert de fenêtre principale à l'application. La fenêtre contient un widget ttk.Notebook, qui permet à l'utilisateur de passer d'une page à l'autre, chacune contenant des fonctionnalités différentes.

La première page du carnet affiche un widget arborescent qui présente tous les produits de la base de données, ainsi que leurs détails. L'utilisateur peut sélectionner un produit et cliquer sur le bouton "Modifier produit" pour en modifier les détails, ou cliquer sur le bouton "Supprimer produit" pour le supprimer de la base de données.

La deuxième page du carnet propose un formulaire permettant d'ajouter un nouveau produit à la base de données. L'utilisateur peut saisir le nom, la description, le prix, la quantité et la catégorie du produit, puis cliquer sur le bouton "Ajouter produit" pour l'ajouter à la base de données.

La troisième page du carnet propose un formulaire permettant d'ajouter une nouvelle catégorie à la base de données. L'utilisateur peut saisir le nom de la catégorie et cliquer sur le bouton "Ajouter catégorie" pour l'ajouter à la base de données.

Le script définit également plusieurs fonctions utilitaires pour interagir avec la base de données, telles que create_connexion() pour créer une connexion à la base de données, ajouter_produit() pour ajouter un nouveau produit à la base de données, et recuperer_produits() pour récupérer tous les produits de la base de données.
