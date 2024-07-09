import re
from pyvis.network import Network

# 初始化Pyvis网络
net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

# 读取并解析文本文件
file_path = 'L-GRE-再要你命3000顺序版QA.txt'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 正则表达式解析
entries = re.split(r'\n\n+', content.strip())
nodes = {}
edges = []

for entry in entries:
    lines = entry.strip().split('\n')
    word_info = re.match(r'Q:([a-zA-Z]+)\s+\[.*\]', lines[0])
    if word_info:
        word = word_info.group(1)
        details = {}
        current_definition = ""
        for line in lines[1:]:
            print("processing line "+ line)
            if line.startswith('A: ♠考法'): #有一行是以A: ♠考点开头的！我给改回去了！出现这种错误，是否意味着这份资料是手打的？？？？作者强的可怕
                current_definition = f"{word} {line[3:].strip()}"
                nodes[current_definition] = ""
            elif line.startswith('A: ♣例'):
                nodes[current_definition] += f"Example: {line[3:].strip()}<br>"
            elif line.startswith('A: ♣近'):
                synonyms = line[3:].strip().split(',')
                for synonym in synonyms:
                    edges.append((current_definition, synonym.strip(), 'synonym'))
            elif line.startswith('A: ♣反'):
                antonyms = line[3:].strip().split(',')
                for antonym in antonyms:
                    edges.append((current_definition, antonym.strip(), 'antonym'))
            elif line.startswith('A: ♣派'):
                derivatives = line[3:].strip().split(',')
                for derivative in derivatives:
                    edges.append((current_definition, derivative.strip(), 'derivative'))
            else:
                nodes[current_definition] += f"{line[3:].strip()}<br>"

print(nodes)


# # 添加节点到网络
# for node, info in nodes.items():
#     net.add_node(node, title=info, label=node, color="#dd4b39")

# # 添加边到网络
# for edge in edges:
#     if edge[2] == 'synonym':
#         net.add_edge(edge[0], edge[1], color='green')
#     elif edge[2] == 'antonym':
#         net.add_edge(edge[0], edge[1], color='red')
#     else:
#         net.add_edge(edge[0], edge[1], color='grey')

# # 显示网络
# net.show('word_network.html')
