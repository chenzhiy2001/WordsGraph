import re

# 定义解析函数
def parse_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式解析词条
    entries = re.split(r'\n(?=Q:)', content.strip())
    parsed_entries = []

    for entry in entries:
        lines = entry.split('\n')
        word_match = re.match(r'Q:(\S+)', lines[0])
        pronunciation_match = re.search(r'\[(.*?)\]', lines[0])
        
        if not word_match or not pronunciation_match:
            continue  # 如果无法匹配单词或发音，则跳过该词条
        
        word = word_match.group(1)
        pronunciation = pronunciation_match.group(1)
        definitions = []

        current_definition = None

        for line in lines[1:]:
            if line.startswith('A: ♠考法'):
                if current_definition:
                    definitions.append(current_definition)
                current_definition = {'type': '', 'examples': [], 'synonyms': [], 'antonyms': [], 'derivatives': [], 'related': []}
                type_match = re.search(r'♠考法\d\s*(.*)(?<=[\u4e00-\u9fff])', line)
                if type_match:
                    current_definition['type'] = type_match.group(1)
            elif line.startswith('A: ♣例'):
                current_definition['examples'].append(line.split(' ', 1)[1])
            elif line.startswith('A: ♣近'):
                current_definition['synonyms'].extend(line.split(' ', 1)[1].split(', '))
            elif line.startswith('A: ♣同'):
                current_definition['related'].extend(line.split(' ', 1)[1].split(', '))
            elif line.startswith('A: ♣反'):
                current_definition['antonyms'].extend(line.split(' ', 1)[1].split(', '))
            elif line.startswith('A: ♣派'):
                current_definition['derivatives'].extend(line.split(' ', 1)[1].split(', '))

        if current_definition:
            definitions.append(current_definition)

        parsed_entries.append({'word': word, 'pronunciation': pronunciation, 'definitions': definitions})

    return parsed_entries

# 解析文件
entries = parse_txt('L-GRE-再要你命3000顺序版QA.txt')

def generate_html(entries):
    word_set = {entry['word'] for entry in entries}

    def make_clickable(text):
        # 使用正则表达式将文本中的单词转换为链接
        words = text.split()
        clickable_words = []
        for word in words:
            clean_word = re.sub(r'[^\w\s]', '', word)  # 去掉标点符号
            if clean_word in word_set:
                clickable_words.append(f'<a href="#{clean_word}">{word}</a>')
            else:
                clickable_words.append(word)
        return ' '.join(clickable_words)

    html_content = '''
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GRE - 再要你命3000</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            .word-list {
                margin: 20px;
            }
            .word-list a {
                display: block;
                margin: 5px 0;
                text-decoration: none;
                color: blue;
            }
            .entry {
                margin: 20px;
            }
            .entry h2 {
                margin: 0;
            }
            .definition {
                margin: 10px 0;
            }
            ul {
                list-style: none;
            }
        </style>
    </head>
    <body>
        <h1>再要你命3000可点击版 by czy</h1>
        <div class="word-list">
    '''

    for entry in entries:
        html_content += f'<a href="#{entry["word"]}">{entry["word"]}</a>\n'

    html_content += '</div>\n'

    for entry in entries:
        html_content += f'''
        <div class="entry" id="{entry["word"]}">
            <h2>{entry["word"]} [{entry["pronunciation"]}]</h2>
        '''

        for definition in entry['definitions']:
            html_content += f'<div class="definition"><strong>{definition["type"]}:</strong>\n'

            if definition['examples']:
                html_content += '<ul>'
                for example in definition['examples']:
                    html_content += f'<li>{make_clickable(example)}</li>\n'
                html_content += '</ul>'

            if definition['synonyms']:
                #html_content += f'<p><strong>近义词：</strong> {", ".join([make_clickable(syn) for syn in definition["synonyms"]])}</p>\n'
                html_content += f'<p>{", ".join([make_clickable(syn) for syn in definition["synonyms"]])}</p>\n'
            
            if definition['related']:
                html_content += f'<p>{", ".join([make_clickable(rel) for rel in definition["related"]])}</p>\n'

            if definition['antonyms']:
                html_content += f'<p>{", ".join([make_clickable(ant) for ant in definition["antonyms"]])}</p>\n'
            
            if definition['derivatives']:
                html_content += f'<p>{", ".join([make_clickable(der) for der in definition["derivatives"]])}</p>\n'

            html_content += '</div>\n'

        html_content += '</div>\n'

    html_content += '''
    </body>
    </html>
    '''

    with open('dictionary.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

# 生成HTML文件
generate_html(entries)
