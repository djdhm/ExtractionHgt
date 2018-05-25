import os 
import numpy as np
#La configuration des types de fichiers de donnees 
Type_Fichier= {
    'SRTM1':{
            'taille':3601,
            'deplacement':1
            },
    'SRTM3':{
            'taille':1201,
            'deplacement':3
    }
}
# le type par default
default_type='SRTM3'


Frontieres= {
	'NORD': 36.65,
	'SUD': 35.80,
	'EST': 3.28,
	'OUEST': 4.40
}




# lire le fichier Hgt et retourner un tableau correspondant 

def lireFichier(url):
    DIM=Type_Fichier[default_type]['taille']
    # les fichiers HGT contiennent des donnees de type Signed Integer 16bit : i2
    # stocke en bigendian : >
    with open(url,'rb') as fichier:
        altitudes= np.fromfile(
            fichier,
            np.dtype('>i2'),
            DIM * DIM
        ).reshape((DIM,DIM))
    return altitudes



# Avoir le nom de fichier Hgt relative au cordonnees fournies

def getNomFichier(latitude,longitude):
    coord=''
    if(latitude>0):
        coord+='N'
    else:
        coord+='S'
    
    coord+=abs(latitude)
    if(longitude>0):
        coord+='E'
    else:
        coord+='W'

    coord+=abs(longitude)
    return coord
def cartesion_cord(degre,secondes):
	a=secondes/3600
	return str(degre+a)

# Creer le tableau contenant long,lat,alt
def create_table(cordX,cordY,departx,finx,departy,finy,tableau,fichier_sortie,densite=1):
    incorrecte=0
    for x in range(departx,finx,densite):
        for y in range(departy,finy,densite):
		altitude=tableau[x][y]
		if(altitude==-32768):
			incorrecte=incorrecte+1
			print("valeur incorrecte")
		else:
		        lat=cartesion_cord(cordX+1,-x*3)
		        lon=cartesion_cord(cordY,y*3)
		        temp=lat+";"+lon+";"+str(tableau[x][y])+"\n"
		        fichier_sortie.write(temp)

def preaprer_data(nomFichier):
    fichier_sortie=open(nomFichier,'w')
    fichier_sortie.write('Latitude;Longitude;Altitude\n')
    create_table(36,4,456,1201,0,480,lireFichier("hgt/N36E004.hgt"), fichier_sortie)
    create_table(36,3,456,1201,348,1201,lireFichier("hgt/N36E003.hgt"), fichier_sortie)
    create_table(35,3,0,192,348,1201,lireFichier("hgt/N35E003.hgt"), fichier_sortie)
    create_table(35,4,0,192,0,480,lireFichier("hgt/N35E004.hgt"), fichier_sortie)
    print("Initialisation termine avec succes... ")



# Cette fonction extrait tout les points contenus dans le fichier hgt 
# et les ecrit en format CSV 
print("Debut de l'ecriture des donnees ...")
preaprer_data("AltitudeBouira.csv")

# Cette fonction permet de diminuer le nombre de points ecrit 
#  en ecrivant seulement les points appartenant a bouira 
