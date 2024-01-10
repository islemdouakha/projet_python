import regex as re
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

from Classes import Author


class Corpus(metaclass=Singleton):
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
        self.longueChaineDeCaracteres = None

    def add(self, doc):
        for aut in doc.auteur:
            if aut not in self.aut2id:
                self.naut += 1
                self.authors[self.naut] = Author(aut)
                self.aut2id[aut] = self.naut
            self.authors[self.aut2id[aut]].add(doc.texte)
        
        self.ndoc += 1
        self.id2doc[self.ndoc] = doc


    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))

    def concatener_texte(self):
        if self.longueChaineDeCaracteres is None:
            self.longueChaineDeCaracteres = " ".join([doc.texte for doc in self.id2doc.values()])

    def get_longue_chaine_de_caracteres(self):
        self.concatener_texte()
        return self.longueChaineDeCaracteres
    
    def search(self, mot):
        self.concatener_texte()
        matches = re.findall(rf"\b{mot}\b", self.longueChaineDeCaracteres, re.IGNORECASE)
        print(f"{mot} a été trouvé {len(matches)} fois dans le corpus.")
        for match in matches:
            print(match)

