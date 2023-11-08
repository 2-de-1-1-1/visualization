import json
from collections import Counter
import networkx as nx
from networkx.algorithms import bipartite
from matplotlib import rc
import matplotlib.pyplot as plt

# 1. data load
    # missing: sample 94개 중 position 89개, tech_stacks 75개
with open('./job.json', 'r') as f:
    job_data = json.load(f)


# 2. position, tech_stack
position = set([])
tech_stack = set([])
    
for job in job_data:
    for pos in job.get('positions', []):
        position.add(pos)
    for tech in job.get('tech_stacks', []):
        tech_stack.add(tech)


# 3. Graph node, edge 지정
Bipart = nx.Graph()
# Bipart.add_nodes_from(position, bipartite=0) # 그룹 1: positioin
filtered_position = set(list(position)[:5])
Bipart.add_nodes_from(filtered_position, bipartite=0) # 그룹 1_필터링: filtered_position
Bipart.add_nodes_from(tech_stack, bipartite=1) # 그룹 2: tech_stack


edges = []
for job in job_data:
    for pos in job.get('positions', []):
        for tech in job.get('tech_stacks', []):
            edges.append((pos, tech))
        # if pos in filtered_position:
        #     for tech in job.get('tech_stacks', []):
        #         edges.append((pos, tech))

Bipart.add_edges_from(edges)


# 4-1. bipartite graph
# pos = nx.bipartite_layout(Bipart, filtered_position)
# nx.draw(Bipart, pos=pos, with_labels=True, font_family='AppleGothic', font_size=5)
# plt.savefig('networkx_res/bipartite.png')
# plt.show()


# 4-2. tech_stack projection
proj = bipartite.projected_graph(Bipart, tech_stack)
pos = nx.spring_layout(proj)

nx.draw_networkx(proj, pos=pos, font_family='AppleGothic', font_size=5)
plt.savefig('networkx_res/projected.png')
plt.show()


# 4-3. tech_stack projection (가중치)
    # ratio: True_비율 표시, False_개수 표시
# proj = bipartite.weighted_projected_graph(Bipart, tech_stack, ratio=False)
# pos = nx.spring_layout(proj)
# weight = nx.get_edge_attributes(proj, 'weight')

# nx.draw(proj, pos=pos, with_labels=True, font_family='AppleGothic', font_size=5)
# nx.draw_networkx_edge_labels(proj, pos=pos, edge_labels=weight, font_size=3) # edge 위의 라벨
# plt.show()
