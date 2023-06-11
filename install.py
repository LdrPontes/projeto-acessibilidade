import os
import shutil
import subprocess
import requests
import json
import gdown

print("iniciado processo")

# Obter o nome do usuário a partir das variáveis de ambiente
username = os.getenv("USERNAME")
print("usuario : " + username)
# URL do primeiro arquivo para download
url1 = "https://github.com/kaishuu0123/erd-go/releases/latest/download/windows_amd64_erd-go.exe"

urlDrive = 'https://drive.google.com/uc?id=1U9FqQAhuYlEv6YeO33yvhQFeyThNUdCI'

# URL do segundo arquivo para download
url2 = "https://github.com/kaishuu0123/graphviz-dot.js/releases/latest/download/graphviz-dot-win-x64.exe"

# Caminho onde os arquivos serão salvos
path = fr"C:\Users\{username}\Tools"
print("caminho : " + path)
# Verificar se o diretório de destino existe, se não, criá-lo
if not os.path.exists(path):
    os.makedirs(path,exist_ok=True)

# Função para fazer o download do arquivo
def download_file(url, file_path):
    response = requests.get(url)
    with open(file_path, "wb") as file:
        file.write(response.content)

def dowload_stack(nameFile):
    try:
        subprocess.run('stack --version', shell=True, check=True)
        print("'stack' já está instalado.")
    except subprocess.CalledProcessError:
    # 'stack' não está instalado, realizar a instalação
        try:
            subprocess.run(["stack.exe"], shell=True, check=True)
        except:
            print("executando stack")
        subprocess.run(["'copy stack.exe %APPDATA%\\local\\bin'"], shell=True, check=True)
        print("'stack' foi instalado com sucesso.") 
    print("Clonando o repositório Git..." + nameFile)
    subprocess.run('pwd && git clone git://github.com/BurntSushi/erd', shell=True, check=True)
    # Entrar no diretório clonado
    print("Entrando no diretório clonado...")
    subprocess.run('cd erd', shell=True)
    # Executar o comando 'stack install' no diretório clonado
    print("Executando 'stack install'...")
    try:
        subprocess.run(['stack', 'install'], shell=True, check=True)  
    except:
        subprocess.run(['%APPDATA%\local\bin\stack.exe', 'install','--compiler=ghc-8.8.4','--resolver=lts-16.8'], shell=True, check=True)
    print("'stack install' concluído com sucesso.")

# Fazer o download do primeiro arquivo
file1_path = os.path.join(path, "windows_amd64_erd-go.exe")
try:
    if not os.path.exists(file1_path):
        gdown.download(urlDrive, file1_path)
        print(" dowload primeiro arquivo erd-go")
    # Executar o primeiro arquivo
    try:
        comando = f'Add-MpPreference -ExclusionPath "{file1_path}"'
        subprocess.run(['powershell', comando])
    except:
        print("Não foi possivel adicionar o er nos arquivos liberados do windows defender")
    subprocess.call(file1_path)
except:
    try:
       file1_path = dowload_stack(file1_path)
    except:
        print("Não foi possivel baixar o erd")
# Fazer o download do segundo arquivo
file2_path = os.path.join(path, "graphviz-dot-win-x64.exe")
if not os.path.exists(file2_path):
    download_file(url2, file2_path)
    print("Download do segundo arquivo graphviz")
# Executar o segundo arquivo
subprocess.call(file2_path)
print("Chamando execução do instalador do graphviz")
# Atualizar o arquivo settings.json
settings_file = os.path.expandvars(r"%APPDATA%\Code\User\settings.json")

# Ler o conteúdo atual do arquivo settings.json
if os.path.exists(settings_file):
    # Ler o conteúdo atual do arquivo settings.json
    with open(settings_file) as file:
        settings = json.load(file)

    # Adicionar as chaves e os caminhos dos arquivos
    settings["erd-preview.erdPath"] = file1_path
    settings["erd-preview.dotPath"] = file2_path

    # Escrever as alterações de volta no arquivo settings.json
    with open(settings_file, "w") as file:
        json.dump(settings, file, indent=4)

    # Informar que a atualização foi concluída
    print("Arquivo settings.json atualizado com sucesso!")
else:
    print("O arquivo settings.json não existe.")
print("Arquivo settings.json atualizado com sucesso!")

# Verificar o sistema operacional atual
if os.name == 'nt':  # Windows
    vscode_path = shutil.which('code.cmd')
elif os.name == 'posix':  # Linux ou macOS
    vscode_path = shutil.which('code')
else:
    print("Sistema operacional não suportado.")
    exit()

# Verificar se o VSCode está instalado
if vscode_path is None:
    print("Visual Studio Code não encontrado. Verifique se está instalado corretamente.")
    exit()

# Nome da extensão a ser instalada
extension_name = 'kaishuu0123.vscode-erd-preview'

# Executar o comando 'code --install-extension' com o caminho para o executável do VSCode
subprocess.call([vscode_path, '--install-extension', extension_name])

