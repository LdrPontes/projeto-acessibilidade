import os
import shutil
import subprocess
import json

print("iniciado processo")

# Obter o nome do usuário a partir das variáveis de ambiente
username = os.getenv("USERNAME")
print("usuario : " + username)

def dowload_stack(nameFile):
    try:
        os.makedirs("C:\\Program Files\\stack")
        subprocess.run(["copy", "stack.exe", "C:\\Program Files\\stack\\"], shell=True, check=True)
        print("stack foi instalado com sucesso.") 
    except:
        print("Erro ao instalar o stack")
    # Executar o comando 'stack install' no diretório clonado
    clone_erd()
    print("Executando stack install do projeto erd")
    try:
       subprocess.run(["C:\\Program Files\\stack\\stack.exe", 'install','--compiler=ghc-8.8.4','--resolver=lts-16.8'], shell=True, check=True, cwd="erd/")
    except:
        print("stack install concluído com sucesso.")

def clone_erd():
    if not os.path.exists("erd"):
        print("Clonando o repositório Git...")
        subprocess.run('git clone https://github.com/BurntSushi/erd.git', shell=True, check=True)
    

# Fazer o download do primeiro arquivo
def install_windows():
    file1_path = os.path.expandvars("%APPDATA%\Roaming\local\bin\erd.exe")
    try:
        if not os.path.exists(file1_path):
            dowload_stack(file1_path)
            print("Realização da instalação do erg-go finalizada com sucesso")
        # Executar o primeiro arquivo
    except:
        print("Não foi possivel baixar o erd")
    # Fazer o download do segundo arquivo
    file2_path = os.path.join("C:\\Program Files\\Graphviz\\bin", "dot.exe")
    pathSetting = os.path.join("PATH=%PATH%",file2_path)
    if not os.path.exists(file2_path):
        try:
            subprocess.run(['winget', 'install','-e', '--id' ,'Graphviz.Graphviz'],shell=True, check = True)
            subprocess.run(["set", pathSetting], shell=True , check= True)
            print("Instalação do graphviz realizada com sucesso")
        except: 
            print("Erro ao realizar a instalação do graphviz")
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

def install_linux():
    subprocess.run(["sudo", "apt", "install", "graphviz"])
    subprocess.run(["curl","-sSL","https://get.haskellstack.org/" +"|"+ "sh"])
    clone_erd()
    subprocess(["stack", "install", "--compiler=ghc-8.8.4","--resolver=lts-16.8"],cwd="erd/")

# Verificar o sistema operacional atual
if os.name == 'nt':  # Windows
    install_windows()
    vscode_path = shutil.which('code.cmd')
elif os.name == 'posix':  # Linux ou macOS
    install_linux()
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
extension_highlighting = 'mikkel-ol.er-syntax-highlighting'
# Executar o comando 'code --install-extension' com o caminho para o executável do VSCode
subprocess.call([vscode_path, '--install-extension', extension_name])
subprocess.call([vscode_path, '--install-extension', extension_highlighting])

