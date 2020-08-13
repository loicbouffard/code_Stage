'''Ce module contient les fonctions pour calculer les différentes variables
lors de la transformation des couleurs RGB vers les longueurs d'ondes.'''
import math


def convertion_0_1(liste_moyenne):
    '''Converti un tuple de listes R, G, B /255 vers /1 et retourne un nouveau tuple de même nature
    liste_moyenne, (R,G,B) où R, G et B sont des listes de longueur égale au nombre de pixel de l'image'''
    length = len(liste_moyenne[0])
    liste_0_1 = ([0]*length, [0]*length, [0]*length)
    for i in range(length):
        liste_0_1[0][i] = liste_moyenne[0][i]/255
        liste_0_1[1][i] = liste_moyenne[1][i]/255
        liste_0_1[2][i] = liste_moyenne[2][i]/255
    return liste_0_1


def liste_MMCLHSSL(liste_0_1, lMax, lMin):
    '''Permet d'obtenir une liste de tuple contenant les valeurs max, min, Chroma, Luminance, Hue, Saturation max,
    Saturation mid et longueur d'onde d'une liste de moyenne converti /1.
    [(max,min,C,L,H,Smax,Smid,Lambda), ...]'''
    length = len(liste_0_1[0])
    liste_mmclhssl = [0]*length
    dic = {}
    lambMax = lMax
    lambMin = lMin
    deltaLamb = lambMax-lambMin
    for i in range(length):
        R = liste_0_1[0][i]
        G = liste_0_1[1][i]
        B = liste_0_1[2][i]
        xmax = max(R, G, B)
        xmin = min(R, G, B)
        c = xmax-xmin
        l = (xmax+xmin)/2
        h = calcul_Hue(c, xmax, R, G, B)
        smax, smid = calcul_saturation(xmax, c, l)
        lamb = round(lambMax - ((deltaLamb*h)/270), 2)
        ajouter_valeur_dicLO(dic, lamb)
        liste_mmclhssl[i] = (xmax, xmin, c, l, h, smax, smid, lamb)
    return liste_mmclhssl, dic


def calcul_saturation(xmax, c, l):
    '''Calcule la saturation max et mid. Retourne le tuple (Smax,Smid)'''
    if xmax == 0:
        smax = 0
    else:
        smax = c/xmax
    if l == 0 or l == 1:
        smid = 0
    else:
        smid = c/(1-abs(2*xmax-c-1))
    return (smax, smid)


def calcul_Hue(c, xmax, R, G, B):
    '''Calcule le Hue '''
    if c == 0:
        h = 0
    elif xmax == R:
        h = 60 * ((G-B)/c)
    elif xmax == G:
        h = 60 * ((B-R)/c) + 120
        # h = 60 * (2 + ((B-R)/c))
    elif xmax == B:
        h = 60 * ((R-G)/c) + 240
        # h = 60 * (4 + ((R-G)/c))
    return h


def liste_norme_RGB(liste_0_1):
    '''Permet d'obtenir une liste de la norme de la moyenne de chaque colonne'''
    length = len(liste_0_1[0])
    liste_norme = [0]*length
    for i in range(length):
        liste_norme[i] = math.sqrt(
            liste_0_1[0][i]**2 + liste_0_1[1][i]**2 + liste_0_1[2][i]**2)
    return liste_norme


def liste_tuple_param(liste_mmclhssl, liste_norme, nbr_param=2):
    '''Retourne une liste de tuples contenant le nombre de paramètre voulu (2 ou 4)
    [(H,Smid,norme,lambda)...] ou [(norme,lambda)...]'''
    length = len(liste_norme)
    liste = [0]*length
    if nbr_param == 2:
        for i in range(length):
            liste[i] = (liste_norme[i], liste_mmclhssl[i][7])
    elif nbr_param == 4:
        for i in range(length):
            liste[i] = (liste_mmclhssl[i][4], liste_mmclhssl[i]
                        [6], liste_norme[i], liste_mmclhssl[i][7])
    return liste


def ajouter_valeur_dicLO(dic, lamb):
    '''Ajoute une valeur de longueur d'onde au dictionnaire. Les clés du ditonnaire sont les longueurs d'onde et les valeurs sont 
    le nombre de fois que celle-ci se retrouve parmis la liste des moyennes de colonnes. Si elle est déjà présente, le nombre s'incrémente de 1,
    si elle ne l'est pas, elle est ajoutée au dictionnaire avec une valeur de 1.'''
    if lamb in dic:
        dic[lamb] = dic[lamb] + 1
    else:
        dic[lamb] = 1
