import re
from pyvis.network import Network

# 初始化Pyvis网络
net = Network(notebook = True, cdn_resources = "in_line",
                bgcolor = "#222222",
                font_color = "white",
                height = "750px",
                width = "100%",
)

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
    'synonym':'green',
    'antonym':'red',
    'derivative':'grey',
    'same_meaning':'blue'
}

for entry in entries:
    lines = entry.strip().split('\n')
    word_info = re.match(r'Q:([a-zA-Z]+)\s+\[.*\]', lines[0])
    if word_info:
        word = word_info.group(1)
        details = {}
        current_definition = ""
        for line in lines[1:]:
            if line.startswith('A: ♠考法'): #有2行是以A: ♠考点开头的，我给改回去了！出现这种错误，是否意味着这份资料是手打的？？？？作者强的可怕
                current_definition = f"{word} {line[3:].strip()}"
                if word in word_to_nodes:
                    word_to_nodes[word].append(current_definition)
                else:
                    word_to_nodes[word]=[current_definition]
                nodes[current_definition] = ""
            elif line.startswith('A: ♣例'):
                nodes[current_definition] += f"Example: {line[3:].strip()}<br>"
            elif line.startswith('A: ♣近'):
                synonyms = line[len('A: ♣近'):].strip().split(',')
                for synonym in synonyms:
                    edges.append((current_definition, synonym.strip(), 'synonym'))
            elif line.startswith('A: ♣反'):
                antonyms = line[len('A: ♣反'):].strip().split(',')
                for antonym in antonyms:
                    edges.append((current_definition, antonym.strip(), 'antonym'))
            elif line.startswith('A: ♣派'):
                derivatives = line[len('A: ♣派'):].strip().split(',')
                for derivative in derivatives:
                    edges.append((current_definition, derivative.strip(), 'derivative'))
            elif line.startswith('A: ♣同'):
                same_meanings = line[len('A: ♣同'):].strip().split(',')
                for same_meaning in same_meanings:
                    edges.append((current_definition, same_meaning.strip(), 'same_meaning'))
            else:
                print("error! line is "+line)
                #nodes[current_definition] += f"{line[3:].strip()}<br>"

# 添加节点到网络
for node, info in nodes.items():
    net.add_node(node, title=info, label=node, color="#dd4b39")


# 添加边到网络
for edge in edges:
    #print(f"current edge is from {edge[0]} to {edge[1]}")
    end_nodes = [] # 1 word has many meanings, so 1 'edge' is many edges on the graph
    if edge[1] not in word_to_nodes:
        net.add_node(edge[1], label=edge[1], color="#dd4b39")
        end_nodes.append(edge[1])
    else:
        end_nodes = word_to_nodes[edge[1]]
    for end in end_nodes:
        net.add_edge(edge[0], end, color=edge_class_color[edge[2]])
        
# 显示网络
net.show('gre.html',notebook=True)
