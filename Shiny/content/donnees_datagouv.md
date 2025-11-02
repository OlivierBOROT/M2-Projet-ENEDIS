
# Présentation des données climatologiques - DATA.GOUV

Les données climatologiques de base mensuelles sont mises à disposition par **DATA.GOUV** et concernent toutes les stations météorologiques française de métropole et d'outre-mer depuis leur ouverture, pour tous les paramètres disponibles. Ces données ont subi un contrôle climatologique afin de garantir leur qualité.

## Informations techniques

- Les données décadaires sont proposées en téléchargement par département et par lots de période au format CSV compressé ou par un **horrible** API basé sur swagger.
- L'ensemble des paramètres est fourni pour l'ensemble des stations météorologiques.  
- Les heures sont exprimées en UTC pour la métropole et en FU pour l'outre-mer.  
- La mise à jour des fichiers est annuelle pour les historiques avant 1950, mensuelle pour les fichiers de 1950 jusqu'à l'année -2, et quotidienne pour les deux dernières années.

## Paramètres principaux

Chaque fichier contient de nombreuses colonnes, dont certaines très intéressantes :

- **NUM_POSTE** : numéro Météo-France du poste (8 chiffres)  
- **NOM_USUEL** : nom du poste  
- **LAT / LON** : coordonnées (latitude, longitude)  
- **ALTI** : altitude (m)  
- **AAAAMM** : mois  
- **RR, QRR, NBRR, RR_ME, RRAB, QRRAB, RRABDAT** : précipitations  
- **TX, TX_ME, TXAB, QTXAB, TXDAT, TXMIN, QTXMIN, TXMINDAT** : températures maximales  
- **TN, TN_ME, TNAB, QTNAB, TNDAT** : températures minimales  
- **TM, TMM, TMMIN, TMMAX** : températures moyennes  
- **UMM, UNAB, UXAB, NBUN, NBUX** : humidité  
- **FFM, FXIAB, FXYAB, FXI3SAB** : vent  
- **INST, NBSIGMA0, NBSIGMA20, NBSIGMA80** : ensoleillement  
- **GLOT, DIFT, DIRT** : rayonnement  
- **HNEIGEFTOT, HNEIGEFAB** : neige  
- **NBJGREL, NBJORAG, NBJBROU** : grêle, orage, brouillard  

> Les valeurs des codes qualité sont :  
> - 9 : donnée filtrée  
> - 0 : donnée protégée (validée définitivement)  
> - 1 : donnée validée  
> - 2 : donnée douteuse en cours de vérification  

De manière générale, les données sont d'une excellente qualité et recouvrent toute la France. Le principal défaut de l'utilisation de l'API pour récupérer ces données est le fait qu'il existe un lien d'API par fichier. L'avantage est d'avoir des données à jour grâce à la mise à jour quotidienne des derniers fichiers que nous utilisons ici.

## Liens utiles

- [Page DATA.GOUV – données climatologiques](https://www.data.gouv.fr/fr/datasets/donnees-climatologiques-de-base-mensuelles/)
- [Dataset DPE Logements neufs](https://data.ademe.fr/datasets/dpe02neuf)
- [Dataset DPE Logements existants](https://data.ademe.fr/datasets/dpe03existant)
