#Url de flux:
BASE_URL = 'http://192.168.107.204:8089/SiteBourse'
#Liste des actions disponibles avec leurs noms et groupes pour utilisation dans le flux.
STOCK_DATA_FILE = 'stock_list.csv'
#Liste des actions disponibles avec leurs noms pour l'extraction des données historiques de stocks
HISTORY_STOCK_DATA_FILE = 'stock_list_hist_data.csv'
#Le premier jour pour commencer à récupérer les données historiques 
date1 = ""
#Le dernier jour 
date2 = ""
# Configuration pour la connexion à la base de données MySQL(historique des actions)
DB_CONFIG = {
    'host': 'localhost',    # Adresse IP ou nom d'hôte du serveur MySQL
    'user': 'root',         # Nom d'utilisateur MySQL
    'password': 'nafaa',    # Mot de passe MySQL
    'database': 'stock_data' # Nom de la base de données à utiliser
}
