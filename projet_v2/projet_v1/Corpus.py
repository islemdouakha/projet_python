import regex as re
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

from Classes import Author
import pandas as pd
from Collections import Counter
from scipy.sparse import csr_matrix


class Corpus(metaclass=Singleton):
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
        self.longueChaineDeCaracteres = None
        self.vocab = {}
        self.vocabulaire = set()
        self.frequence_mots = None

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
    
    def search(self, mot, contexte=30):
        self.concatener_texte()
        
        matches = re.findall(rf"\b{mot}\b", self.longueChaineDeCaracteres, re.IGNORECASE)

        print(f"{mot} a été trouvé {len(matches)} fois dans le corpus.")
        
        
        for match in matches:
            deb = max(0, match.start() - contexte)
            
            fin = min(len(self.longueChaineDeCaracteres), match.end() + contexte)

            passage = self.longueChaineDeCaracteres[deb:fin]

            print(f"...\n{passage}\n...")

        return
    

    def concorde(self, mot, contexte=30):
        self.concatener_texte()

        matches = re.findall(rf"\b{mot}\b", self.longueChaineDeCaracteres, re.IGNORECASE)

        concordancier = []

        for match in matches:
            deb = max(0, match.start() - contexte)
            fin = min(len(self.longueChaineDeCaracteres), match.end() + contexte)
            
            contexte_droite = longueChaineDeCaracteres[deb : match.start()]
            contexte_gauche = longueChaineDeCaracteres[match.end() : fin]

            concordancier.append((contexte_gauche,match.group(),contexte_droite))

        df = pd.DataFrame(concordancier,columns = ["Contexte gauche","Motif Trouvé","Contexte Droit"])

        return df

    def nettoyer_texte(self, chaine):
        chaine = chaine.lower()
        chaine = re.sub(r"\n,", " ", chaine)
        chaine = re.sub(r'[^\w\s]', '', chaine)
        
        return chaine

    def stats(self, n):
        self.concatener_texte()
        
        chaine = self.nettoyer_texte(self.longueChaineDeCaracteres)
        
        mots = chaine.split()
        
        print(f"Le nombre des mots dans le corpus est : {len(mots)}")
        
        
        plus_frequents = Counter(mots).most_common(n)

        print(f"Les {n} mots les plus fréquents sont :")

        for mot, frequence in plus_frequents:
            print(f"{mot} : {freq}")
        

    def creer_vocabulaire(self, texte):
        voc = set(sorted(self.nettoyer_texte(texte).split()))
        

        return self.vocab
    
    def maj_vocabulaire(self):
        for mot in self.vocabulaire:
            if mot not in self.vocab:
                self.vocab[mot] = {
                    "id" : len(self.vocab) + 1,
                    "frequence" : 0
                }
            self.vocab[mot]["frequence"] += 1

    def compter_frequence(self):
        self.concatener_texte()
        
        texte = self.nettoyer_texte(self.longueChaineDeCaracteres)

        words = re.split(r'\s+|[.,;\'"!?()]', texte)
        words = [word for word in words if word != ""]
        words = [word for word in words if word.isalpha()]
        words = [word.lower() for word in words]
        
        self.frequence_mots = Counter(words)

        doc_word_freq = Counter()
        for doc in self.id2doc.values():
            doc_text = self.nettoyer_texte(doc.texte)
            doc_words = set(re.split(r'\s+|[.,;\'"!?()]', doc_text))
            doc_words = {word.lower() for word in doc_words if word.isalpha()}
            doc_word_freq.update(doc_words)

        for word, freq in self.word_frequencies.items():
            self.word_frequencies[word] = {
                "term_frequency": freq,
                "document_frequency": doc_word_freq[word],
            }
        
        freq = pd.DataFrame(
            list(self.frequence_mots.items()), columns=["Word", "Frequencies"]
        )
        
        freq[["Term Frequency", "Document Frequency"]] = pd.DataFrame(
            freq["Frequencies"].tolist(), index=freq.index
        )

        freq.drop(columns=["Frequencies"], inplace=True)
        return freq

        def creer_matrice(self):
            lignes = []
            colonnes = []
            valeurs = []
            for id,doc in self.id2doc:
                mots = self.nettoyer_texte(doc.texte).split()
                compteur = Counter(mots)
                
                for mot,freq in compteur.items():
                    if mot not in self.vocab:
                        print(f"Le mot {mot} n'est pas dans le vocabulaire")
                    else : 
                        lignes.append(self.vocab[mot]["id"] - 1)
                        colonnes.append(id - 1)
                        valeurs.append(freq)
        mat_TF = csr_matrix((valeurs,(lignes,colonnes)),shape=(len(self.vocab),len(self.id2doc)))

        return mat_TF

        def calcul_vecteur(self, requete):

            vecteur = np.zeros((len(self.vocab),1))
            
            for mot in self.nettoyer_texte(requete).split():
                if mot in self.vocab:
                    vecteur[self.vocab[mot]["id"] - 1] += 1
            
            return vecteur

        def calcul_similarite(self,vecteur1, vecteur2):
            vecteur1_norm = np.linalg.norm(vecteur1)
            vecteur2_norm = np.linalg.norm(vecteur2)
            if vecteur1_norm == 0 or vecteur2_norm == 0:
                return 0
            else:
                return np.dot(vecteur1.T, vecteur2) / (vecteur1_norm * vecteur2_norm)
        
        def calcul_score(self, requete):
            vecteur_requete = self.calcul_vecteur()
            score = []
            for id,doc in self.id2doc:
                vecteur_doc = self.calcul_vecteur()
                score.append(self.calcul_similarite(vecteur_requete,vecteur_doc))
            scores = sorted(scores, key=lambda x: x[1], reverse=True)
            scores = [(id, score) for id, score in scores if score > 0]
            return score
