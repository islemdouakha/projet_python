# Correction de G. Poux-Médard, 2021-2022





import praw


def showDictStruct(d):
    def recursivePrint(d, i):
        for k in d:
            if isinstance(d[k], dict):
                print("-"*i, k)
                recursivePrint(d[k], i+2)
            else:
                print("-"*i, k, ":", d[k])
    recursivePrint(d, 1)


reddit = praw.Reddit(client_id='MPNtLJFi9WDhqwoXyQH_TA', client_secret='-XsL7-l14Rwq8bznow2k59wuz3K40w', user_agent='test')


limit = 100
hot_posts = reddit.subreddit('all').hot(limit=limit)#.top("all", limit=limit)#


docs = []
docs_bruts = []
afficher_cles = False
for i, post in enumerate(hot_posts):

    if afficher_cles:  

        for k, v in post.__dict__.items():
            pass
            print(k, ":", v)
    
    if post.selftext != "":  # Osef des posts sans texte
        pass
        #print(post.selftext)
    docs.append(post.selftext.replace("\n", " "))
    docs_bruts.append(("Reddit", post))





import urllib, urllib.request, _collections
import xmltodict


query_terms = ["clustering", "Dirichlet"]
max_results = 50


url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'
data = urllib.request.urlopen(url)


data = xmltodict.parse(data.read().decode('utf-8'))




for i, entry in enumerate(data["feed"]["entry"]):

    docs.append(entry["summary"].replace("\n", ""))
    docs_bruts.append(("ArXiv", entry))



docs = list(set(docs))


for i, doc in enumerate(docs):

    if len(doc)<100:
        docs.remove(doc)

longueChaineDeCaracteres = " ".join(docs)



from Classes import Document, RedditDocument, ArxivDocument


import datetime
collection = []
for nature, doc in docs_bruts:
    if nature == "ArXiv":  # Les fichiers de ArXiv ou de Reddit sont pas formatés de la même manière à ce stade.

        titre = doc["title"].replace('\n', '')  # On enlève les retours à la ligne
        try:
            authors = ", ".join([a["name"] for a in doc["author"]])  # On fait une liste d'auteurs, séparés par une virgule
        except:
            authors = doc["author"]["name"]  # Si l'auteur est seul, pas besoin de liste
        summary = doc["summary"].replace("\n", "")  # On enlève les retours à la ligne
        date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  # Formatage de la date en année/mois/jour avec librairie datetime
        texte = doc["id"]
        doc_classe = ArxivDocument(titre, date,authors, texte,summary)
        doc_classe.type = doc_classe.getType()


        collection.append(doc_classe)  # Ajout du Document à la liste.

    elif nature == "Reddit":

        titre = doc.title.replace("\n", '')
        auteur = str(doc.author)
        date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
        url = "https://www.reddit.com/"+doc.permalink
        texte = doc.selftext
        nbcmnts = doc.num_comments

        doc_classe = RedditDocument(titre, auteur, date, url, texte, nbcmnts)
        collection.append(doc_classe)


id2doc = {}
for i, doc in enumerate(collection):
    id2doc[i] = doc.titre


from Classes import Author


authors = {}
aut2id = {}
num_auteurs_vus = 0


for doc in collection:
    for aut in doc.auteur :
        if aut not in aut2id:
            num_auteurs_vus += 1
            authors[num_auteurs_vus] = Author(aut)
            aut2id[aut] = num_auteurs_vus

            authors[aut2id[aut]].add(doc.texte)



from Corpus import Corpus
corpus = Corpus("Mon corpus")


for doc in collection:
    corpus.add(doc)




import pickle


with open("corpus.pkl", "wb") as f:
    pickle.dump(corpus, f)


del corpus


with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)


print(corpus)