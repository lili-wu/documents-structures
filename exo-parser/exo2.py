# coding:utf-8
# Lili WU
'''
À partir du fichier exo-parser/Duchn-etiquetage.txt.xml:
    1. Extraire tous les déterminants
    2. Afficher les patrons DET - NOM
    3. Reconstruire les phrases
    4. Transformer l'affichage en : token/lemme/pos
'''
from lxml import etree

xmlfile = 'Duchn-etiquetage.txt.xml'

# Initialiser la lecture du fichier
tree = etree.parse(xmlfile)

# La racine
root = tree.getroot()

# 1 : Extraire tous les déterminants
det_list = [] # liste des déterminants
for element in root.iter('element'):
    if element[0].text[0:3] == 'DET':
        if element[2].text not in det_list:
            det_list.append(element[2].text)

# 2 : Afficher les patrons DET - NOM
patrons = [] # liste de tuples de la forme (DET, NOM)
i = 0
for article in root.iter('article'):
    for element in article:
        if article[i][0].text[0:3] == 'DET':
            if article[i+1][0].text == 'NOM':
                patrons.append((article[i][2].text,article[i+1][2].text))
        i += 1

# 3 : Reconstruire les phrases
phrases = [] # Liste de phrases
phrase = [] # Liste des tokens d'une phrase
for element in root.iter('element'):
    if element[0].text != 'SENT':
        phrase.append(element[2].text)
    else:
        phrase.append(element[2].text) # ajoute la ponctuation de fin de phrase
        phrases.append(" ".join(phrase))
        phrase = [] # réinitialise la variable

# 4 : Transformer l'affichage en : token/lemme/pos
tlp = [] # liste de tuples de la forme (token,lemme,pos)
for element in root.iter('element'):
    tlp.append((element[2].text,element[1].text, element[0].text))

# fichier résultat
with open('result.txt', 'x') as f_out:
    f_out.write('1) Liste de tous les déterminants: \n')
    f_out.write(str(det_list))
    f_out.write('\n2) Patrons DET - NOM:\n')
    f_out.write('\n'.join(['{} - {}'.format(item[0],item[1]) for item in patrons]))
    f_out.write('3) Phrases: \n')
    f_out.write('\n'.join([item for item in phrases]))
    f_out.write('4) Affichage en token/lemme/pos : \n')
    f_out.write('\n'.join(['{}/{}/{}'.format(item[0],item[1],item[2]) for item in tlp]))
