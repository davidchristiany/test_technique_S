class Drug:
    def __init__(self, atccode, name):
        self.atccode = atccode
        self.name = name
        self.articles = None
        self.trials = None

    @property
    def journals(self):
        return [article.journal for article in self.articles]

    @property
    def article_ids(self):
        return [article.id for article in self.articles]

    @property
    def trials_ids(self):
        if self.trials:
            return [trial.id for trial in self.trials]
        else:
            return None

    def add_article(self, article):
        if self.articles is None:
            self.articles = [article]
        else:
            self.articles.append(article)

    def add_trial(self, trial):
        if self.trials is None:
            self.trials = [trial]
        else:
            self.trials.append(trial)