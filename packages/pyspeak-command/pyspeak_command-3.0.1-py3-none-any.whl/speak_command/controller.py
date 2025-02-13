import subprocess as sp
import os, sys
import pyttsx3
import ftfy
# import utils as util
from deep_translator import GoogleTranslator
from speak_command import utils as util

engine = pyttsx3.init()
if os.name == "nt":
    LOG_DIR = os.path.join(os.getenv("APPDATA"), "speak_command", "logs")
else:
    LOG_DIR = os.path.expanduser("~/.speak_command/logs")

os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "terminal_log.txt")

#funções que executam os comandos, serão chamadas no main.py
def run_normal_command(qtdArgs, cmd):
    if qtdArgs==3:
        log_command(cmd[0])
        translate_log(cmd[1],cmd[2])
        read_log()
                
    elif qtdArgs==1:
        log_command(cmd[0])
        read_log()
    else:
        print('Erro: Insira os argumentos corretamente!')
        util.speak('Erro: Insira os argumentos corretamente!')
        sys.exit()

def run_help(qtdArgs, cmd):
    if qtdArgs==3:
        util.text_help()
        translate_log(cmd[1],cmd[2])
        read_log()
                
    elif qtdArgs==1:
        util.change_voice("Portuguese")
        util.save_log(util.text_help())
        read_log()

    else:
        print('Erro: Insira os argumentos corretamente!')
        util.speak('Erro: Insira os argumentos corretamente!')
        sys.exit()

def run_scripts(qtdArgs, cmd):
    if qtdArgs==2:
        python_script(cmd[1])
        read_log()
    elif qtdArgs==4:
        python_script(cmd[1])
        translate_log(cmd[2], cmd[3])
        read_log()

    else:
        print('Erro: Insira os argumentos corretamente!')
        util.speak('Erro: Insira os argumentos corretamente!')
        sys.exit()

def run_file(qtdArgs, cmd):
    if qtdArgs==2:
        read_file(cmd[1])
        read_log()

    elif qtdArgs==4:
        verif = read_file(cmd[1])

        if verif == False:
            return
        else:
            translate_file(cmd[2], cmd[3], cmd[1])
            read_log()

    else:
        print('Erro: Insira os argumentos corretamente!')
        util.speak('Erro: Insira os argumentos corretamente!')
        sys.exit()

# Traduz um arquivo informado pelo usuário
def translate_file(lingua_ori, lingua_dst, file_name):
    try:
        util.change_voice(lingua_dst)
        
        lingua_ori = util.lang_suport(lingua_ori)
        lingua_dst = util.lang_suport(lingua_dst)


        translated = GoogleTranslator(source=lingua_ori, target=lingua_dst).translate_file(LOG_FILE)
        util.save_log(translated)
        
        base_name, extension = os.path.splitext(file_name)
        new_file_name = f"{base_name}_{lingua_dst}{extension}"
        
        current_directory = os.getcwd()
        file_path = os.path.abspath(file_name)
        
        if not os.path.exists(file_path):
            error_msg = f"Erro: O arquivo '{file_name}' não foi encontrado no diretório '{current_directory}'"
            util.save_log(error_msg)
            return
        
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
        with open(new_file_path, "w", encoding='utf-8', errors='replace') as new_file:
            new_file.write(translated + "\n")
            new_file.flush()
        
    except Exception as e:
        util.save_log(f"Erro ao traduzir o arquivo: {e}")

# Traduz o que está arquivo terminal_log.txt
def translate_log(lingua_ori, lingua_dst):
    try:
        util.change_voice(lingua_dst)
        
        lingua_ori = util.lang_suport(lingua_ori)
        lingua_dst = util.lang_suport(lingua_dst)
                
        translated = GoogleTranslator(source=lingua_ori, target=lingua_dst).translate_file(LOG_FILE)
        
        util.save_log(translated)
        
    except Exception as e:
        util.save_log(f"Erro na tradução: {e}")
        print(f"Erro na tradução: {e}")

# salva o comando no arquivo terminal_log.txt
def log_command(command):
    try:
        result = sp.run(command, shell=True, stdout=sp.PIPE,stderr=sp.PIPE)
        encoding = 'cp850' if os.name == 'nt' else 'utf-8'
        output = result.stderr.decode('utf-8', errors='replace') if result.stderr else result.stdout.decode(encoding, errors='replace')
        output = ftfy.fix_text(output)
        
        format3l.,ted_output = f"\n> {command}\n{output}"
        util.save_log(formatted_output)
                    
    except Exception as e:
        util.save_log(f"Erro ao executar o comando: {e}")
        
# lê o arquivo terminal_log.txt em voz alta
def read_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding='utf-8') as file:
            output = file.read()
        print(output, flush=True)
        util.speak(output)
    else:
        no_history = "Nenhum histórico encontrado."
        print(no_history)
        util.speak(no_history, flush=True)

# Executa um script Python informado pelo usuário
def python_script(script_name):
    current_directory = os.getcwd()
    script_path = os.path.abspath(script_name)
    if not os.path.exists(script_path):
        error_msg = f"Erro: O arquivo '{script_name}' não foi encontrado no diretório '{current_directory}'"
        util.save_log(error_msg)
        return
    
    if os.path.getsize(script_path) == 0:
        error_msg = f"Erro: O arquivo '{script_name}' está vazio."
        util.save_log(error_msg)
        return 
    
    try:
        python_cmd = "python" if os.name == "nt" else "python3"
        
        result = sp.run(
            [python_cmd, script_path],
            capture_output=True,  
            text=True
        )

        stdout_text = ftfy.fix_text(result.stdout) if result.stdout else ""
        stderr_text = ftfy.fix_text(f"\nErros:\n{result.stderr}") if result.stderr else ""

        output = f"\n> {script_name}\n{stdout_text}{stderr_text}"

        util.save_log(output)
    
    except Exception as e:
        error_msg = f"Erro ao executar o script: {e}"
        util.save_log(error_msg)
        return

# Lê um arquivo informado pelo usuário
def read_file(file_name):
    current_directory = os.getcwd()
    file_path = os.path.abspath(file_name)
    if not os.path.exists(file_path):
        error_msg = f"Erro: O arquivo '{file_name}' não foi encontrado no diretório '{current_directory}'"
        util.save_log(error_msg)
        return
    if os.path.getsize(file_path) == 0:
        error_msg = f"Erro: O arquivo '{file_name}' está vazio."
        util.save_log(error_msg)
        return False
    try:   
        with open(file_path, "r", encoding='utf-8') as file:
            output = file.read()
        util.save_log(output)
        
    except Exception as e:
        error_msg = f"Erro ao ler o arquivo: {e}"
        util.save_log(error_msg)
        return