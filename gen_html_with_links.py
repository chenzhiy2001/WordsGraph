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
                # 尝试匹配有无冒号的情况
                type_match = re.search(r'♠考法\d\s*(.*)', line)
                if type_match:
                    current_definition['type'] = type_match.group(1)
            elif line.startswith('A: ♣例'):
                current_definition['examples'].append(line.split(' ', 2)[2] if len(line.split(' ', 2)) >= 3 else '')
            elif line.startswith('A: ♣近'):
                current_definition['synonyms'].extend(re.split(r',\s*', line.split(' ', 2)[2]))
            elif line.startswith('A: ♣同'):
                current_definition['related'].extend(re.split(r',\s*', line.split(' ', 2)[2]))
            elif line.startswith('A: ♣反'):
                current_definition['antonyms'].extend(re.split(r',\s*', line.split(' ', 2)[2]))
            elif line.startswith('A: ♣派'):
                current_definition['derivatives'].extend(re.split(r',\s*', line.split(' ', 2)[2]))

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
                clickable_words.append(f'<a href="#{clean_word}" class="clickable-word">{word}</a>')
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
                background-color: #f9f9f9;
                color: #333;
            }
            .word-list {
                margin: 20px;
                padding: 10px;
                background-color: #fff;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            .word-list a {
                display: block;
                margin: 5px 0;
                text-decoration: none;
                color: #0066cc;
            }
            .word-list a:hover {
                text-decoration: underline;
            }
            .entry {
                margin: 20px;
                padding: 10px;
                background-color: #fff;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            .entry h2 {
                margin: 0;
                color: #0066cc;
            }
            .definition {
                margin: 10px 0;
            }
            .definition strong {
                color: #cc0000;
            }
            ul {
                list-style: none;
                padding: 0;
            }
            li {
                margin: 5px 0;
            }
            .clickable-word {
                color: #0066cc;
            }
            .clickable-word:hover {
                text-decoration: underline;
            }
            .synonyms, .antonyms, .related, .derivatives {
                color: #007700;
                font-weight: bold;
            }
            .examples {
                color: #cc0000;
                font-weight: bold;
            }
            
            h1 {
                text-align: center;
                color: #333;
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
            html_content += f'<div class="definition"><strong>{definition["type"]}</strong>\n'

            if definition['examples']:
                html_content += '<ul>'
                for example in definition['examples']:
                    html_content += f'<li><span class="examples">例：</span>{make_clickable(example)}</li>\n'
                html_content += '</ul>'

            if definition['synonyms']:
                html_content += f'<p><span class="synonyms">近义词：</span>{", ".join([make_clickable(syn) for syn in definition["synonyms"]])}</p>\n'
            
            if definition['related']:
                html_content += f'<p><span class="related">同义词：</span>{", ".join([make_clickable(rel) for rel in definition["related"]])}</p>\n'

            if definition['antonyms']:
                html_content += f'<p><span class="antonyms">反义词：</span>{", ".join([make_clickable(ant) for ant in definition["antonyms"]])}</p>\n'
            
            if definition['derivatives']:
                html_content += f'<p><span class="derivatives">派生词：</span>{", ".join([make_clickable(der) for der in definition["derivatives"]])}</p>\n'

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
