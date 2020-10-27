class Articles:
    def __init__(self, id, title, date, journal):
        self.id = str(id) if id != '' else None
        self.title = title
        self.date = date
        self.journal = journal

    def drug_mentioned(self, drug):
        if drug.name in self.title.upper():
            return True
        else:
            return False

class PubmedArticle(Articles):
    def __init__(self, id, title, date, journal):
        super().__init__(id, title, date, journal)

class Trial(Articles):
    def __init__(self, id, title, date, journal):
        super().__init__(id, title, date, journal)