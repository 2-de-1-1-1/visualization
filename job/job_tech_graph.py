import json
from collections import Counter
import networkx as nx
from networkx.algorithms import bipartite
from matplotlib import rc
import matplotlib.pyplot as plt

plt.rc('font', family='AppleGothic')

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

position = ['시스템/네트워크', '서버/백엔드', '프론트엔드', '머신러닝']
Bipart.add_nodes_from(position, bipartite=0) # 그룹 1: position
Bipart.add_nodes_from(tech_stack, bipartite=1) # 그룹 2: tech_stack

# edges = set([])
edges = []
for job in job_data:
    for pos in job.get('positions', []):
        if pos in position:
            for tech in job.get('tech_stacks', []):
                edges.append((pos, tech))

Bipart.add_edges_from(edges)


# 4-1. bipartite graph
# pos = nx.bipartite_layout(Bipart, position)
# nx.draw(Bipart, pos=pos, with_labels=True, font_family='AppleGothic', font_size=5)
# plt.savefig('networkx_res/bipartite.png')
# plt.show()


# 4-2. tech_stack projection
proj = bipartite.projected_graph(Bipart, tech_stack)
pos = nx.spring_layout(proj)


# 차수 thresh 설정
degree = []

for node, deg in nx.degree(proj):
    degree.append(deg)

degree = sorted(list(set(degree)))
degree_thresh = degree[2] # 0, min값인 노드는 제외
max_degree = degree[-1]
min_degree = degree[1]

# 차수 낮은 노드는 제외
high_degree_node = []

for node, deg in nx.degree(proj):
    degree.append(deg)
    if deg >= degree_thresh:
        high_degree_node.append(node)

        
proj_subnet = proj.subgraph(high_degree_node)

# 노드:차수 pair 딕셔너리 생성
node_degrees = dict(proj_subnet.degree())
node_sizes = {node: degree * 20 for node, degree in node_degrees.items()} # 차수에 비례하는 크기 가짐
node_values = {node: degree for node, degree in node_degrees.items()} # 차수에 따른 색상 지정


cmap = plt.get_cmap('spring')
plt.figure(figsize=(20, 15))

# subnet node, label
# nx.draw_networkx_nodes(proj_subnet, pos=pos, node_size=[node_sizes[n] for n in node_sizes.keys()], node_color=['pink' if node_sizes[n] > 50 * 100 else 'grey' for n in node_sizes.keys()]) 
nx.draw_networkx_nodes(proj_subnet, pos=pos, node_size=[node_sizes[n] for n in node_sizes.keys()],
                                            node_color=list(node_values.values()),
                                            cmap=cmap,
                                            vmin=min_degree, vmax=max_degree)
nx.draw_networkx_labels(proj_subnet, pos=pos, font_size=17, font_color='black')

# subnet edge
nx.draw_networkx_edges(proj_subnet, pos=pos, edge_color='lightgrey')

plt.title('포지션 별 연관 기술 스택', fontsize=30)
plt.savefig('networkx_res/projected.png')
# plt.show()


# 4-3. tech_stack projection (가중치_ratio)
    # ratio: True_비율 표시, False_개수 표시
# proj = bipartite.weighted_projected_graph(Bipart, tech_stack, ratio=False)
# pos = nx.spring_layout(proj)
# weight = nx.get_edge_attributes(proj, 'weight')

# nx.draw(proj, pos=pos, with_labels=True, font_family='AppleGothic', font_size=5)
# nx.draw_networkx_edge_labels(proj, pos=pos, edge_labels=weight, font_size=3) # edge 위의 라벨
# plt.show()