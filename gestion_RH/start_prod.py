import os
import sys
import django
from django.db import connections
from django.db.utils import OperationalError

# Configuration de l'environnement Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestion_RH.settings")
django.setup()

def database_is_ready():
    """Vérifie si la base de données est prête à recevoir des connexions"""
    db_conn = connections['default']
    try:
        db_conn.cursor()
        return True
    except OperationalError:
        return False

def run_migrations():
    """Exécute les migrations de la base de données"""
    print("Exécution des migrations...")
    from django.core.management import call_command
    call_command('migrate', interactive=False)
    print("Migrations terminées avec succès.")



def create_superuser():
    """Crée un superutilisateur s'il n'existe pas déjà"""
    print("Vérification du superutilisateur...")
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(username='admin').exists():
        print("Création du superutilisateur avec les identifiants par défaut...")
        User.objects.create_superuser(
            username='admin',
            email='admin@mail.com',
            password='admin'
        )
        print("Superutilisateur créé avec succès.")
    else:
        print("Le superutilisateur existe déjà.")

if __name__ == "__main__":
    print("Démarrage du script d'initialisation de l'application en production...")
    
    # Attend que la base de données soit prête
    max_retries = 10
    retry_count = 0
    
    while not database_is_ready() and retry_count < max_retries:
        print(f"La base de données n'est pas prête. Tentative {retry_count + 1}/{max_retries}...")
        import time
        time.sleep(2)
        retry_count += 1
    
    if database_is_ready():
        print("Base de données connectée avec succès.")
        run_migrations()
        create_superuser()
        print("Initialisation terminée. L'application est prête à être utilisée.")
    else:
        print("Impossible de se connecter à la base de données. Vérifiez la configuration.")
        sys.exit(1)