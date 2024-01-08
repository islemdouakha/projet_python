


class Document:

    def __init__(self, titre="", auteur="", date="", url="", texte="",type=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte



    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"


    def __str__(self):
        return f"{self.titre}, par {self.auteur}"
    def getType(self):
        pass




class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []

    def add(self, production):
        self.ndoc += 1
        self.production.append(production)
    def __str__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"

class RedditDocument(Document):
    def __init__(self, titre="", auteur="", date="", url="", texte="", nbcmnts="",type=""):
        super().__init__( titre, auteur, date, url, texte,type)
        self.nbcmnts = nbcmnts

    def get_nbcmnts(self):
        return self.nbcmnts
    
    def set_nbcmnts(self, nb):
        self.nbcmnts = nb
        
    def __str__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\tNombre de commentaires : {self.nbcmnts}\tType : {self.getType()}"
    def getType(self):
        return "RedditDocument"

class ArxivDocument(Document):

    def __init__(self, titre="", date="", auteur="", url="", texte="",type=""):
        super().__init__(titre,auteur,date, url, texte,type)
        self.auteur = auteur.split(',')
        
    def get_auteurs(self):
        return self.auteur
    
    def set_auteurs(self, auteurs):
        self.auteur = auteurs.split(",")
    
    def getType(self):
        return "ArxivDocument"
    def __str__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\tType : {self.getType()}"