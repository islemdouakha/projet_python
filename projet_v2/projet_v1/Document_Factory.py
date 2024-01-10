from Document import RedditDocument, ArxivDocument

class Document_Factory:
    def get_document(self, document_type):
        if document_type == "Reddit":
            return RedditDocument()
        elif document_type == "Arxiv":
            return ArxivDocument()
        else:
            print("Type de document :" + document_type+ " non reconnu.")
            return None
