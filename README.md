# AttesationNumeriqueCOVID-19
Générateur multiple d'attestation numérique dérogatoire pour le confinement dû au Covid-19

## Installation
```bash
# Création de l'environment python (facultatif)
python3 -m virtualenv .venv --python=/usr/bin/python3

# Installation des dépendances
pip3 install qrcode 
sudo apt-get install ttf-mscorefonts-installer

```

## Utilisation
```bash
.python3 main.py \
	--first-name John \
	--last-name Doe \
	--birth-date 01/01/1900 \
	--birth-city Paname \
	--address "12 GRANDE RUE 75666 Paname" \
	--current-city Paname \
	--start-date 01/11/2020 \
	--end-date 31/12/2020
	--leave-hour 08:00 \
	--motifs travail-courses-sante-famille-sport-judiciaire-missions
```

Toutes les attestations générée sont disponibles dans le dossier output.