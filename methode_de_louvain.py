import pandas as pd
import networkx as nx
import community

data = pd.read_csv('C:/Users/hp/Desktop/prj_pfe_inwi/traffic_matrix.csv')

G = nx.Graph()

# Ajouter des arêtes (liens) entre les nœuds (cellules) en utilisant les colonnes "a_number" et "b_number"
edges_list = [(row['a_number'], row['b_number']) for _, row in data.iterrows()]
G.add_edges_from(edges_list)

# Appliquer la méthode de Louvain pour détecter les communautés
partition = community.best_partition(G)

# Initialiser un dictionnaire pour stocker les éléments dans chaque communauté
community_data = {}
for node, community_id in partition.items():
    if community_id not in community_data:
        community_data[community_id] = {'Elements': set(), 'Calls_Made': {}, 'Calls_Received': {}}
    community_data[community_id]['Elements'].add(node)

# Compter le nombre d'éléments dans chaque communauté
community_counts = {community_id: len(data['Elements']) for community_id, data in community_data.items()}

# Compter le nombre d'appels effectués par chaque numéro dans chaque communauté
for _, row in data.iterrows():
    a_number, b_number = row['a_number'], row['b_number']
    community_id = partition[a_number]
    if a_number not in community_data[community_id]['Calls_Made']:
        community_data[community_id]['Calls_Made'][a_number] = 0
    community_data[community_id]['Calls_Made'][a_number] += 1

# Compter le nombre d'appels reçus par chaque numéro dans chaque communauté
for _, row in data.iterrows():
    a_number, b_number = row['a_number'], row['b_number']
    community_id = partition[b_number]
    if b_number not in community_data[community_id]['Calls_Received']:
        community_data[community_id]['Calls_Received'][b_number] = 0
    community_data[community_id]['Calls_Received'][b_number] += 1

# Calculer le nombre total d'appels dans chaque communauté
for community_id, data in community_data.items():
    total_calls = sum(data['Calls_Made'].values())
    community_data[community_id]['Total_Calls'] = total_calls

# Écrire les résultats dans un fichier texte
with open('venv/resultats_communautes.txt', 'w') as file:

    # Écrire le nombre total de communautés
    num_communities = len(community_data)
    file.write(f"Nombre total de communautés : {num_communities}\n\n")

    # Écrire pour chaque communauté le nombre d'éléments, le nombre total d'appels,
    # les 3 numéros les plus actifs et les 3 numéros les plus appelés
    for community_id, data in community_data.items():
        file.write(f"Community {community_id} - Nombre d'éléments : {community_counts[community_id]}\n")
        file.write(f"Nombre total d'appels : {data['Total_Calls']}\n")

        # Les 3 numéros les plus actifs dans la communauté
        top_active_numbers = sorted(data['Calls_Made'].items(), key=lambda x: x[1], reverse=True)[:3]
        file.write("Les 3 numéros les plus actifs :\n")
        for number, calls_made in top_active_numbers:
            file.write(f"Numéro {number} - Nombre d'appels effectués : {calls_made}\n")

        # Les 3 numéros les plus appelés dans la communauté
        top_called_numbers = sorted(data['Calls_Received'].items(), key=lambda x: x[1], reverse=True)[:3]
        file.write("Les 3 numéros les plus appelés :\n")
        for number, calls_received in top_called_numbers:
            file.write(f"Numéro {number} - Nombre d'appels reçus : {calls_received}\n")

        file.write("\n")
