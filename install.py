import os
import shutil
import subprocess
import json

print("iniciado processo")

# Obter o nome do usuário a partir das variáveis de ambiente
username = os.getenv("USERNAME")
print("usuario : " + username)
RED = "\033[1;31m"
GREEN = "\033[0;32m"
listError = []

def dowload_stack(nameFile):
    try:
        os.makedirs("C:\\Program Files\\stack")
        subprocess.run(["copy", "stack.exe", "C:\\Program Files\\stack\\"], shell=True, check=True)
        print(GREEN + "stack foi instalado com sucesso.") 
    except:
        print(RED + "Erro ao instalar o stack")
        listError.append(RED + "Erro ao instalar o stack")
    # Executar o comando 'stack install' no diretório clonado
    clone_erd()
    print("Executando stack install do projeto erd")
    try:
        if not os.path.exists(nameFile):
            subprocess.run(["C:\\Program Files\\stack\\stack.exe", 'install','--compiler=ghc-8.8.4','--resolver=lts-16.8'], shell=True, check=True, cwd="erd/")
    except:
        print(RED + "Error ao realizar intalação do Erd-Go.")
        listError.append(RED + "Error ao realizar intalação do Erd-Go.")

def clone_erd():
    if not os.path.exists("erd"):
        try:
            subprocess.run("git --version",shell=True, check=True)
        except:
            if os.name == 'nt':
                subprocess.run(['winget', 'install','-e', '--id' ,'Git.Git'],shell=True, check = True)
            elif os.name == 'posix':
                subprocess.run(["sudo", "apt", "install", "git"])
        print("Clonando o repositório Git...")
        subprocess.run('git clone https://github.com/BurntSushi/erd.git', shell=True, check=True)
    

# Fazer o download do primeiro arquivo
def install_windows():
    file1_path = os.path.expandvars("%APPDATA%\Roaming\local\bin\erd.exe")
    try:
        if not os.path.exists(file1_path):
            dowload_stack(file1_path)
            print(GREEN + "Realização da instalação do erg-go finalizada com sucesso")
        # Executar o primeiro arquivo
    except:
        print(RED + "Não foi possivel baixar o erd")
        listError.append(RED + "Não foi possivel baixar o erd")
    # Fazer o download do segundo arquivo
    file2_path = os.path.join("C:\\Program Files\\Graphviz\\bin", "dot.exe")
    pathSetting = os.path.join("PATH=%PATH%",file2_path)
    if not os.path.exists(file2_path):
        try:
            subprocess.run(['winget', 'install','-e', '--id' ,'Graphviz.Graphviz'],shell=True, check = True)
            subprocess.run(["set", pathSetting], shell=True , check= True)
            print(GREEN + "Instalação do graphviz realizada com sucesso")
        except: 
            print(RED + "Erro ao realizar a instalação do graphviz")
            listError.append(RED + "Erro ao realizar a instalação do graphviz")
    # Atualizar o arquivo settings.json
    settings_file = os.path.expandvars(r"%APPDATA%\Code\User\settings.json")
    config_setting(settings_file,file1_path,file2_path)
    # Ler o conteúdo atual do arquivo settings.json
    

def config_setting(settings_file,file1_path,file2_path):
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
        print(GREEN + "Arquivo settings.json atualizado com sucesso!")
    else:
        print("O arquivo settings.json não existe.")
    print("Arquivo settings.json atualizado com sucesso!")

def install_linux():
    print("Iniciando processo de instalação graphviz")
    try:
        subprocess.run(["sudo", "apt", "install", "graphviz"])
        print(GREEN + "Graphviz instalado com sucesso")
    except:
        print(RED + "Erro ao realizar a instalação do Graphviz")
        listError.append(RED + "Erro ao realizar a instalação do Graphviz")
    try:
        subprocess.run(["sudo","apt","install","haskell-stack"])
        clone_erd()
        subprocess.run(["stack", "install", "--compiler=ghc-8.8.4","--resolver=lts-16.8"],cwd="erd/")
        print(GREEN + "Instalação do Erd-go realizada com sucesso.")
    except:
        print(RED + "Erro ao Realizar instalação do Erd-Go")
        listError.append(RED + "Erro ao Realizar instalação do Erd-Go")
    file1_path = "~/.local/bin/erd"
    file2_path = shutil.which('dot')
    settings_file = os.path.expandvars(r"%$HOME/.config/Code/User/settings.json")
    config_setting(settings_file,file1_path,file2_path)

# Verificar o sistema operacional atual
if os.name == 'nt':  # Windows
    install_windows()
    vscode_path = shutil.which('code.cmd')
elif os.name == 'posix':  # Linux ou macOS
    install_linux()
    vscode_path = shutil.which('code')
else:
    print(RED + "Sistema operacional não suportado.")
    exit()

# Verificar se o VSCode está instalado
if vscode_path is None:
    print("Visual Studio Code não encontrado. Verifique se está instalado corretamente.")
    exit()

# Nome da extensão a ser instalada
extension_name = 'kaishuu0123.vscode-erd-preview'
extension_highlighting = 'mikkel-ol.er-syntax-highlighting'
# Executar o comando 'code --install-extension' com o caminho para o executável do VSCode
subprocess.call([vscode_path, '--install-extension', extension_name])
subprocess.call([vscode_path, '--install-extension', extension_highlighting])

if listError:
    for error in listError:
        print(error)
    print(RED + "Error ao realizar a instalação, verifique a Documentação e realize a instalação manual.")
