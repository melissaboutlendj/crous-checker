import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Config Email
import os

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_DEST = os.getenv("EMAIL_DEST")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# API URL
API_URL = "https://trouverunlogement.lescrous.fr/api/fr/search/41"

# Payload modèle avec coordonnées pour Lille et Villeneuve d'Ascq
PAYLOAD_TEMPLATE = {
    "idTool": 41,
    "need_aggregation": True,
    "page": 1,
    "pageSize": 24,
    "sector": None,
    "occupationModes": [],
"location": [
    {"lon": 3.057256, "lat": 50.62925},    # Lille
    {"lon": 3.147193, "lat": 50.615554}   # Villeneuve d’Ascq
#    {"lon": 0.6278, "lat": 44.2148}        # Agen approx

    ],
    "price": {"max": 10000000},
    "precision": 5,
    "residence": None,
    "toolMechanism": "residual"
}

# Fonction pour envoyer un email
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SMTP_EMAIL
    msg['To'] = EMAIL_DEST
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email envoyé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")

# Fonction pour récupérer les logements dispo
def fetch_logements(payload):
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get('results', {}).get('items', [])
    except Exception as e:
        print("Erreur lors de la récupération:", e)
        return []

def main():
    seen_ids = set()
    villes_cibles = ["lille", "villeneuve", "rennes"]  # Ajout de "rennes"

    logements = fetch_logements(PAYLOAD_TEMPLATE)

    # Filtrer par ville
    filtered_logements = []
    for logement in logements:
        adresse = logement.get("residence", {}).get("address", "").lower()
        if any(ville in adresse for ville in villes_cibles):
            filtered_logements.append(logement)

    new_logements = []
    for logement in filtered_logements:
        logement_id = logement.get('id')
        available = logement.get('available', False)
        ville = logement.get('residence', {}).get('address', '').lower()
        label = logement.get('label', 'Sans nom')
        if available:
            seen_ids.add(logement_id)
            info = f"Logement disponible : {label}\nAdresse : {ville}\nID : {logement_id}\n"
            new_logements.append(info)
            if "rennes" in ville:
                print(">>> Nouveau logement à Rennes détecté ! <<<")  # Message spécial Rennes

    if new_logements:
        message = "Nouveaux logements disponibles:\n\n" + "\n".join(new_logements)
        send_email("Notification CROUS: logement disponible", message)
    else:
        print("Aucun nouveau logement disponible pour le moment.")





if __name__ == "__main__":
    main()

print(f"SMTP_EMAIL: {SMTP_EMAIL}")
print(f"EMAIL_DEST: {EMAIL_DEST}")
print(f"SMTP_PASSWORD est défini ? {'Oui' if SMTP_PASSWORD else 'Non'}")
