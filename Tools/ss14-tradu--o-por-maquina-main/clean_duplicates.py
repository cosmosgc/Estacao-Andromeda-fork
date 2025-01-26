import os
import re
import chardet
from datetime import datetime

def find_top_level_dir(start_dir):
    marker_file = 'SpaceStation14.sln'
    current_dir = start_dir
    while True:
        if marker_file in os.listdir(current_dir):
            return current_dir
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            print(f"Não foi possível encontrar {marker_file} começando {start_dir}")
            exit(-1)
        current_dir = parent_dir

def find_ftl_files(root_dir):
    ftl_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.ftl'):
                ftl_files.append(os.path.join(root, file))
    return ftl_files

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    return chardet.detect(raw_data)['encoding']

def parse_ent_blocks(file_path):
    try:
        encoding = detect_encoding(file_path)
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()
    except UnicodeDecodeError:
        print(f"Erro ao ler o arquivo {file_path}. Tente ler UTF-8.")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            print(f"Falha ao ler o arquivo {file_path}. Pulando.")
            return {}

    ent_blocks = {}
    current_ent = None
    current_block = []

    for line in content.split('\n'):
        if line.startswith('ent-'):
            if current_ent:
                ent_blocks[current_ent] = '\n'.join(current_block)
            current_ent = line.split('=')[0].strip()
            current_block = [line]
        elif current_ent and (line.strip().startswith('.desc') or line.strip().startswith('.suffix')):
            current_block.append(line)
        elif line.strip() == '':
            if current_ent:
                ent_blocks[current_ent] = '\n'.join(current_block)
                current_ent = None
                current_block = []
        else:
            if current_ent:
                ent_blocks[current_ent] = '\n'.join(current_block)
                current_ent = None
                current_block = []

    if current_ent:
        ent_blocks[current_ent] = '\n'.join(current_block)

    return ent_blocks

def remove_duplicates(root_dir):
    ftl_files = find_ftl_files(root_dir)
    all_ents = {}
    removed_duplicates = []

    for file_path in ftl_files:
        ent_blocks = parse_ent_blocks(file_path)
        for ent, block in ent_blocks.items():
            if ent not in all_ents:
                all_ents[ent] = (file_path, block)

    for file_path in ftl_files:
        try:
            encoding = detect_encoding(file_path)
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()

            ent_blocks = parse_ent_blocks(file_path)
            for ent, block in ent_blocks.items():
                if all_ents[ent][0] != file_path:
                    content = content.replace(block, '')
                    removed_duplicates.append((ent, file_path, block))

            content = re.sub(r'\n{3,}', '\n\n', content)

            with open(file_path, 'w', encoding=encoding) as file:
                file.write(content)
        except Exception as e:
            print(f"Erro ao processar arquivo {file_path}: {str(e)}")

    # Salvando um registro de duplicatas excluídas
    log_dir = "log"
    os.makedirs(log_dir, exist_ok=True)

    log_filename = os.path.join(log_dir, f"removed_duplicates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    with open(log_filename, 'w', encoding='utf-8') as log_file:
        for ent, file_path, block in removed_duplicates:
            log_file.write(f"Duplicado removido: {ent}\n")
            log_file.write(f"Arquivo: {file_path}\n")
            log_file.write("Conteudo:\n")
            log_file.write(block)
            log_file.write("\n\n")

    print(f"O processamento foi concluído. Arquivos verificados: {len(ftl_files)}")
    print(f"O log de duplicatas excluídas é salvo em um arquivo: {log_filename}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_folder = find_top_level_dir(script_dir)
    root_dir = os.path.join(main_folder, "Resources\\Locale\\pt-BR")
    remove_duplicates(root_dir)
