### CROUS Checker – Système intelligent de veille de logements étudiants
Description du projet :

Dans le but de répondre à la difficulté récurrente de trouver rapidement un logement étudiant via le site du CROUS, j’ai conçu et mis en production une solution entièrement automatisée permettant de surveiller en temps réel les disponibilités de logements dans des villes ciblées (ex. : Lille, Villeneuve d’Ascq, Rennes, etc.).

Cette solution détecte instantanément les nouvelles disponibilités et envoie automatiquement une notification par email dès qu’un logement devient disponible, offrant ainsi un avantage compétitif considérable face à la forte demande.

## Stack technique utilisée :
Python 3.10 – Développement du script de scraping via l’API officielle du CROUS.

GitHub Actions – Automatisation de l’exécution toutes les 10 minutes (cron scheduler), sans serveur ni infrastructure manuelle.

Environnements sécurisés (secrets) – Stockage chiffré des identifiants pour l’envoi d’e-mails via Gmail SMTP.

SMTP (smtplib + Gmail) – Notification en temps réel par email lorsqu’un logement est détecté.

API REST JSON – Interaction avec le backend du site CROUS à l’aide de requests.

Git & GitHub – Versionnage et déploiement.

Automatisation serverless (CI/CD) – Aucun serveur requis, tout est orchestré automatiquement via GitHub Actions.

 ## Objectif et bénéfices :
Objectif principal : Être alerté immédiatement des logements disponibles et agir plus rapidement que la majorité des candidats.

Usage personnel et stratégique : Grâce à ce système, je suis capable de détecter des logements qui apparaissent et disparaissent en quelques minutes.

