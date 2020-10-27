import argparse, json

#find journal from built json graph with the most references drugs
def journal_most_different_drugs(path):
    with open(path) as json_file:
        graph = json.load(json_file)

    journals = [e['id'] for e in graph['nodes'] if e['type'] == 'journal']
    drugs = [e['id'] for e in graph['nodes'] if e['type'] == 'drug']
    journals_dict = {}
    for journal in journals:
        for link in graph['links']:
            if link['target'] == journal and link['source'] in drugs:
                if journal in journals_dict:
                    journals_dict[journal].add(link['source'])
                else:
                    journals_dict[journal] = set(link['source'])
    max = 0
    for key in journals_dict:
        if len(journals_dict[key]) > max:
            biggest = key
    return biggest

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="JSON graph, output from pipeline.py ", required=True)
    args = parser.parse_args()

    print(journal_most_different_drugs(args.input))

