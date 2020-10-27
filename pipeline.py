from articles import Articles, PubmedArticle, Trial
from drug import Drug
import json, csv
import networkx as nx
from networkx.readwrite import json_graph

#return list of drug objects build from the drugs csv file
def get_drugs(file_path):
    with open(file_path, 'r') as drugs_file:
        reader = csv.reader(drugs_file, delimiter=",")
        header = next(reader)
        return [(Drug(line[0], line[1])) for line in reader if len(line)==2]

#return list of PubmedArticle objects build from pubmed file
def get_pubmed_articles(file_path):
    articles = []
    if file_path.endswith('.json'):
        with open(file_path) as json_file:
            data = json.load(json_file)
            return [PubmedArticle(article['id'], article['title'], article['date'], article['journal']) for article in data]
    elif file_path.endswith('.csv'):
        with open(file_path) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            header = next(reader)
            return [PubmedArticle(line[0], line[1], line[2], line[3]) for line in reader if len(line)==4]
    else:
        raise Exception("pubmed file must be a csv or a json")

#return list of Trial objects build from clinical trials csv file
def get_clinical_trials(file_path):
    trials = []
    with open(file_path) as clinical_trials:
        reader = csv.reader(clinical_trials, delimiter=',')
        header = next(reader)
        return [Trial(line[0], line[1], line[2], line[3]) for line in reader if len(line)==4]

#load all input data and return a dictionary
def load_input_data(drugs_csv_file, pubmed_articles_csv, pubmed_articles_json, clinical_tests_csv):
    drugs = get_drugs(drugs_csv_file)
    articles = get_pubmed_articles(pubmed_articles_csv)
    articles.extend(get_pubmed_articles(pubmed_articles_json))
    trials = get_clinical_trials(clinical_tests_csv)
    return {'drugs': drugs, 'articles': articles, 'trials': trials}

#Link drugs to articles and trials, take data dictionary (drugs, trials and articles objects) and return a dictionary
def link_drugs_to_articles(data):
    for drug in data['drugs']:
        for article in data['articles']:
            if article.drug_mentioned(drug):
                drug.add_article(article)
        for trial in data['trials']:
            if trial.drug_mentioned(drug):
                drug.add_trial(trial)
    return data

#Build and save networkx graph from drugs objects (and linked articles and trials)
def build_graph(data,output_graph):
    G = nx.Graph()
    for drug in data['drugs']:
        G.add_node(drug.atccode, type="drug", name=drug.name)
        if drug.articles:
            for article in drug.articles:
                if article.id:
                    if article.id not in G:
                        G.add_node(article.id, type="pubmed_article", title=article.title)
                    G.add_edge(drug.atccode, article.id, quotation_date=article.date)
            for journal in drug.journals:
                if journal not in G:
                    G.add_node(journal, type="journal")
                G.add_edge(drug.atccode, journal, quotation_date=article.date)
        if drug.trials:
            for trial in drug.trials:
                if trial.id:
                    if trial.id not in G:
                        G.add_node(trial.id, type="trial", title='trial.title')
                    G.add_edge(drug.atccode, trial.id, quotation_date=trial.date)
    #nx.draw(G, with_labels=True)
    with open(output_graph, 'w') as graph:
        json.dump(json_graph.node_link_data(G),graph, sort_keys=True, indent=4)

if __name__ == '__main__':

    #inputs
    drugs_csv_file = 'Python_test_DE/drugs.csv'
    pubmed_articles_csv = 'Python_test_DE/pubmed.csv'
    pubmed_articles_json = 'Python_test_DE/pubmed.json'
    clinical_tests_csv = 'Python_test_DE/clinical_trials.csv'

    #output
    output_graph = 'outputs/graph.json'

    #pipeline
    data = load_input_data(drugs_csv_file, pubmed_articles_csv, pubmed_articles_json, clinical_tests_csv)
    data = link_drugs_to_articles(data)
    build_graph(data,output_graph)

