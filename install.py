import os
import subprocess
import requests
import json

# Obter o nome do usuário a partir das variáveis de ambiente
username = os.getenv('USERNAME')

# URL do primeiro arquivo para download
url1 = 'https://github.com/kaishuu0123/erd-go/releases/latest/download/windows_amd64_erd-go.exe'

# URL do segundo arquivo para download
url2 = 'https://github.com/kaishuu0123/graphviz-dot.js/releases/latest/download/graphviz-dot-win-x64.exe'

# Caminho onde os arquivos serão salvos
path = fr'C:\Users\{username}\Tools'

# Verificar se o diretório de destino existe, se não, criá-lo
if not os.path.exists(path):
    os.makedirs(path)

# Função para fazer o download do arquivo
def download_file(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(response.content)

# Fazer o download do primeiro arquivo
file1_path = os.path.join(path, 'windows_amd64_erd-go.exe')
download_file(url1, file1_path)

# Executar o primeiro arquivo
subprocess.call(file1_path)

# Fazer o download do segundo arquivo
file2_path = os.path.join(path, 'graphviz-dot-win-x64.exe')
download_file(url2, file2_path)

# Executar o segundo arquivo
subprocess.call(file2_path)

# Atualizar o arquivo settings.json
settings_file = os.path.expandvars(r'%APPDATA%\Code\User\settings.json')

# Ler o conteúdo atual do arquivo settings.json
with open(settings_file, 'r') as file:
    settings = json.load(file)

# Atualizar as chaves com os caminhos dos arquivos baixados
settings['erd-preview.erdPath'] = file1_path.replace('\\', '\\\\')
settings['erd-preview.dotPath'] = file2_path.replace('\\', '\\\\')

# Escrever as alterações de volta no arquivo settings.json
with open(settings_file, 'w') as file:
    json.dump(settings, file, indent=4)

# Informar que a atualização foi concluída
print("Arquivo settings.json atualizado com sucesso!")
