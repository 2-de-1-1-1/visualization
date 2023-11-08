import json
from collections import Counter
import networkx as nx
from networkx.algorithms import bipartite
from matplotlib import rc
import matplotlib.pyplot as plt

# 1. data load
    # missing: sample 94개 중 position 89개, tech_stacks 75개
with open('job/job.json', 'r') as f:
    job_data = json.load(f)


# 2. position, tech_stack node
position = set([])
tech_stack = set([])
    
for job in job_data:
    for pos in job.get('positions', []):
        position.add(pos)
    for tech in job.get('tech_stacks', []):
        tech_stack.add(tech)


# 3. Graph node, edge 지정
Bipart = nx.Graph()

# Bipart.add_nodes_from(position, bipartite=0) # 그룹 1: position
filtered_position = ['시스템/네트워크', '프론트엔드']
Bipart.add_nodes_from(filtered_position, bipartite=0) # 그룹 1_필터링: filtered_position (임의 필터링)
Bipart.add_nodes_from(tech_stack, bipartite=1) # 그룹 2: tech_stack

# edges = set([])
edges = []
for job in job_data:
    for pos in job.get('positions', []):
        # for tech in job.get('tech_stacks', []):
        #     edges.append((pos, tech))
        if pos in filtered_position:
            for tech in job.get('tech_stacks', []):
                edges.append((pos, tech))
                # edges.add((pos, tech))

Bipart.add_edges_from(edges)

print(len(edges))

# 4-1. bipartite graph
# pos = nx.bipartite_layout(Bipart, filtered_position)
# nx.draw(Bipart, pos=pos, with_labels=True, font_family='AppleGothic', font_size=5)
# plt.savefig('networkx_res/bipartite.png')
# plt.show()


# 4-2. tech_stack projection
proj = bipartite.projected_graph(Bipart, tech_stack)
pos = nx.spring_layout(proj)

high_degree = []
low_degree = []
degree_thresh = 50  # 차수 임계치_노드 크기 설정
for node, deg in nx.degree(proj):
    if deg > degree_thresh:
        high_degree.append(node)
    elif deg > 0:
        low_degree.append(node)

high_subnet = proj.subgraph(high_degree)
low_subnet = proj.subgraph(low_degree)

plt.rcParams['figure.figsize'] = (8, 6)

# 차수 높은 subnet
nx.draw_networkx_nodes(high_subnet, pos=pos, node_size=500, node_color='pink') 
nx.draw_networkx_labels(high_subnet, pos=pos, font_size=10, font_color='red')

# 차수 낮은 subnet
nx.draw_networkx_nodes(low_subnet, pos=pos, node_size=300, node_color='grey')
nx.draw_networkx_labels(low_subnet, pos=pos, font_size=7, font_color='black')

# 그래프 전체 edge
nx.draw_networkx_edges(proj, pos=pos, edge_color='lightgrey')

# plt.savefig('networkx_res/projected.png')
plt.show()


# 4-3. tech_stack projection (가중치_ratio)
    # ratio: True_비율 표시, False_개수 표시
# proj = bipartite.weighted_projected_graph(Bipart, tech_stack, ratio=False)
# pos = nx.spring_layout(proj)
# weight = nx.get_edge_attributes(proj, 'weight')

# nx.draw(proj, pos=pos, with_labels=True, font_family='AppleGothic', font_size=5)
# nx.draw_networkx_edge_labels(proj, pos=pos, edge_labels=weight, font_size=3) # edge 위의 라벨
# plt.show()
