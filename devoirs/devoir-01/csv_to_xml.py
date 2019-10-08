# coding=utf-8
# Lili WU
def extract(filename):
	"""Extrait les champs du fichier argument 
	arg : nom du fichier au format csv
	return : liste des noms de colonnes + liste de tuples des éléments
	"""
	content = []
	with open(filename,"r") as f:
		first_line = f.readline().rstrip()
		headers = first_line.split(";")
		n = 0
		for k in range(len(headers)):
			headers[k] = headers[k].replace(" ", "_")
			headers[k] = headers[k].replace("é", "e")
		for line in f:
			line = line.rstrip()
			fields = line.split(";")
			line_content = []
			for field in fields:
				line_content.append(field)
			content.append((line_content))
	return headers, content

def convert_row(headers, row):
	"""Conversion au format XML d'une liste"""
	return f"""	<Film>
		<{headers[0]}>{row[0]}</{headers[0]}>
		<{headers[1]}>{row[1]}</{headers[1]}>
		<{headers[3]}>{row[3]}</{headers[3]}>
		<{headers[4]}>{row[4]}</{headers[4]}>
		<Lieu>
			<{headers[2]} {headers[5]}=\"{row[5]}\">{row[2]}</{headers[2]}>
			<{headers[8]}>{row[8]}</{headers[8]}>
		</Lieu>
		<Periode>
			<{headers[6]}>{row[6]}</{headers[6]}>
			<{headers[7]}>{row[7]}</{headers[7]}>
		</Periode>
	</Film>"""

headers, content = extract("tournagesdefilmsparis2011.csv")

def entites(content, row_number):
	"""Création d'entités pour une colonne
	   Renvoie le contenu modifié avec les entités + dico des entités
	"""
	dico = {}
	for line_num in range(len(content)):
		if dico.get(content[line_num][row_number]) == None:
			entite = ""
			for elt in content[line_num][row_number].split(" "):
				entite = entite + elt[0:2].lower()
				entite = entite.replace("'","")
				entite = entite.replace("@","a")
				if entite[0].isdigit():
					entite = "_" + entite
			dico[content[line_num][row_number]] = "&" + entite + ";"
			content[line_num][row_number] = dico[content[line_num][row_number]]
		else:
			content[line_num][row_number] = dico[content[line_num][row_number]]
	return content, dico

content, type_tournage = entites(content, 4) # entités pour les types de tournage
content, organismes = entites(content, 3) # entités pour les organismes demandeurs

# Ecriture du fichier XML
with open("tournagesdefilmsparis2011.xml", "x") as f_out:
	f_out.write("<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"no\"?>\n")
	f_out.write("<!-- Lili Wu -->\n")
	f_out.write("<!DOCTYPE Films SYSTEM \"tournages.dtd\">\n")
	f_out.write("<Films>\n")
	f_out.write("\n".join([convert_row(headers,row) for row in content[0:]]))
	f_out.write("\n</Films>")

# Pour récupérer les entités crées
# python3.7 csv_to_xml.py  > liste_entites.txt
print(f"""Types de tournages : {type_tournage}
Organismes Demandeurs : {(organismes)}
""")

def convert_dv(k, v):
	"""Pour l'écriture des ENTITY dans la DTD
	k : valeur de l'entité
	v : entité
	"""
	v = v.lstrip("&")
	v = v.rstrip(";")
	return f"<!ENTITY {v} \"{k}\">"

with open("tournages.dtd", "x") as f_out:
	f_out.write("<!-- Lili WU -->\n")
	f_out.write("<!-- DTD pour tournages -->\n")
	f_out.write("<!ENTITY % STR \"#PCDATA\">\n")
	f_out.write("\n<!-- Entités pour les types de tournages -->\n")
	f_out.write("\n".join([convert_dv(k,v) for k,v in type_tournage.items()]))
	f_out.write("\n<!-- Entités pour les organismes demandeurs -->\n")
	f_out.write("\n".join([convert_dv(k,v) for k,v in organismes.items()]))
	f_out.write("\n<!-- *************************** -->")
	f_out.write(f"""
<!ELEMENT Films (Film+)>
	<!ELEMENT Film (Titre,Realisateur,Organisme_Demandeur,Type_de_tournage,Lieu,Periode)>
		<!ELEMENT Titre (%STR;)>
		<!ELEMENT Realisateur (%STR;)>
		<!ELEMENT Organisme_Demandeur (%STR;)>
		<!ELEMENT Type_de_tournage (%STR;)>
		<!ELEMENT Lieu (Adresse, xy)>
			<!ELEMENT Adresse (%STR;)>
				<!ATTLIST Adresse Arrondissement CDATA #REQUIRED>
			<!ELEMENT xy (%STR;)>
		<!ELEMENT Periode (Date_debut, Date_fin)>
			<!ELEMENT Date_debut (%STR;)>
			<!ELEMENT Date_fin (%STR;)>
""")