# Test technique

## Setup

Créer un environnement avec:
* python 3.8 
* networkx

## How to run 

Charger l'environnement créé.
Se placer à la racine du repository et lancer le script pipeline.py:

```
python pipeline.py
```

Un fichier graph.json est alors créer dans le dossier outputs

## Conception Data pipeline

Les fichiers articles.py et drug.py contiennent respectivement les classes Articles et Drug utilisés lors du pipeline. Ces classes permettent un traitement clair et une association simple entre les médicaments, les articles et les essais cliniques.

Le graphe de liaison est créé avec le package networkx à partir des objets *drugs*, *articles* et *trials*. Il est ensuite sauvergardé au format JSON.

A Chaque étape du pipeline, un dictionnaire avec les data *drugs*, *articles* et *trials* est retourné, exepté pour la dernière étape ou le graphe est sauvegardé. Cette conception permet de gérer le pipeline avec un orchestrateur de jobs (de type DAG), il est possible de récupérer le dictionnaire retourné à une étape pour l'étape suivante.

Lors de la construction du graph, les médicaments étant l'aspect central, les journaux, articles ou essais cliniques qui ne sont liés à aucun médicament ne sont pas représentés. 

## Partie annexe

Le script python 'find_journal_with_most_drugs.py' prend en entré le graphe JSON ouptut de pipeline.py et retourne le journal avec le plus de médicaments différents cités:

```
python find_journal_with_most_drugs.py -i outputs/graph.json
```

## Pour aller plus loin 

>Quels sont les éléments à considérer pour faire évoluer votre code afin qu’il puisse gérer de grosses
>volumétries de données (fichiers de plusieurs To ou millions de fichiers par exemple) ?
>Pourriez-vous décrire les modifications qu’il faudrait apporter, s’il y en a, pour prendre en considération de
telles volumétries ?

La conception actuelle du pipeline ne permet pas de gérer des fichiers de plusieurs To étant donné que tous les objets drug, articles et trials doivent être en mémoire pour construire le graph (networkx) json final. 
Cependant, pour pouvoir gérer des fichiers de gros volumes, on peut envisager de découper le ou les fichiers inputs afin de ne pas saturer la mémoire en les lisant les uns après les autres. De cette façon, en faisant tourner le pipeline pour chaque sous jeu de données, on obtient autant de graph que d’instance du pipeline. Il suffit alors d’ajouter une étape pour fusionner les graphs générés en seul et unique graph, c’est possible avec la fonction « combine » de networkx. Il serait alors préférable de sauvegarder les graphs au format netwokx avec pickle par exemple afin de pouvoir tous les charger pour les fusionner avant de convertir le graph final en json.

Il en va de même pour la gestion de millions de fichiers, on peut imager créer un graph pour chaque fichier et ensuite les fusionner par paquet ; mille par par mille par exemple ; et fusionner de nouveaux les graphs résultants jusqu’à n’avoir plus qu’un seul graph networkx que l’on converti en json.

Pour répondre à ce problème de volumétrie, on peut aussi envisager d'utiliser des librairies telles que Pandas ou PySpark. On utiliserait alors des dataframe pour charger et gérer de gros volume de données.

## Partie SQL

> Réaliser une requête SQL simple permettant de trouver le chiffre d’affaires (le montant total des ventes), jour par jour, du 1er janvier 2019 au 31 décembre 2019. Le résultat sera trié sur la date à laquelle la commande a été passée.

```
SELECT date, sum(prod_price*prod_qty) AS ventes from transactions WHERE date BETWEEN '2019-01-01' AND '2019-12-31' GROUP BY date ORDER BY date;
```

>Réaliser une requête un peu plus complexe qui permet de déterminer, par client et sur la période allant du
1er janvier 2019 au 31 décembre 2019, les ventes meuble et déco réalisées.

```
WITH 
  v_meuble AS (select client_id, SUM(prod_price * prod_qty) AS ventes_meuble FROM TRANSACTIONS INNER JOIN PRODUCT_NOMENCLATURE ON TRANSACTIONS.prod_id = PRODUCT_NOMENCLATURE.product_id WHERE product_type = 'MEUBLE' AND date BETWEEN '2019-01-01' AND '2019-12-31' GROUP BY client_id),
  v_deco AS (select client_id, SUM(prod_price * prod_qty) AS ventes_deco FROM TRANSACTIONS INNER JOIN PRODUCT_NOMENCLATURE ON TRANSACTIONS.prod_id = PRODUCT_NOMENCLATURE.product_id WHERE product_type = 'deco'AND date BETWEEN '2019-01-01' AND '2019-12-31' GROUP BY client_id)
SELECT v_meuble.client_id, v_meuble.ventes_meuble, v_deco.ventes_deco
FROM v_meuble JOIN v_deco WHERE v_meuble.client_id = v_deco.client_id;
```
