import re
import networkx as nx

# 初始化NetworkX图
G = nx.Graph()

# 读取并解析文本文件
file_path = 'L-GRE-再要你命3000顺序版QA.txt'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 正则表达式解析
entries = re.split(r'\n\n+', content.strip())
nodes = {}
edges = []
word_to_nodes = {}
edge_class_color = {
    'synonym': 'green',
    'antonym': 'red',
    'derivative': 'grey',
    'same_meaning': 'blue'
}

for entry in entries:
    lines = entry.strip().split('\n')
    word_info = re.match(r'Q:([a-zA-Z]+)\s+\[.*\]', lines[0])
    if word_info:
        word = word_info.group(1)
        details = {}
        current_definition = ""
        for line in lines[1:]:
            if line.startswith('A: ♠考法'):
                current_definition = f"{word} {line[3:].strip()}"
                if word in word_to_nodes:
                    word_to_nodes[word].append(current_definition)
                else:
                    word_to_nodes[word] = [current_definition]
                nodes[current_definition] = ""
                G.add_node(current_definition, info="")
            elif line.startswith('A: ♣例'):
                example_text = f"Example: {line[3:].strip()}"
                nodes[current_definition] += example_text
                G.nodes[current_definition]['info'] += example_text
            elif line.startswith('A: ♣近'):
                synonyms = line[len('A: ♣近'):].strip().split(',')
                for synonym in synonyms:
                    if synonym: edges.append((current_definition, synonym.strip(), 'synonym'))
            elif line.startswith('A: ♣反'):
                antonyms = line[len('A: ♣反'):].strip().split(',')
                for antonym in antonyms:
                    if antonym: edges.append((current_definition, antonym.strip(), 'antonym'))
            elif line.startswith('A: ♣派'):
                derivatives = line[len('A: ♣派'):].strip().split(',')
                for derivative in derivatives:
                    if derivative: edges.append((current_definition, derivative.strip(), 'derivative'))
            elif line.startswith('A: ♣同'):
                same_meanings = line[len('A: ♣同'):].strip().split(',')
                for same_meaning in same_meanings:
                    if same_meaning: edges.append((current_definition, same_meaning.strip(), 'same_meaning'))
            else:
                print("error! line is " + line)

# 添加节点到网络
for node, info in nodes.items():
    G.nodes[node]['info'] = info

# 添加边到网络
for edge in edges:
    end_nodes = []  # 1 word has many meanings, so 1 'edge' is many edges on the graph
    if edge[1] not in word_to_nodes:
        if edge[1] not in G:
            G.add_node(edge[1], info="")
        end_nodes.append(edge[1])
    else:
        end_nodes = word_to_nodes[edge[1]]
    for end in end_nodes:
        G.add_edge(edge[0], end, relation=edge[2])

# 输出为GraphML文件
nx.write_graphml(G, 'word_network.graphml')