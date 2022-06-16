from tabnanny import check
import pytz
from datetime import datetime, timedelta
import os.path
from os import path

def getTime():
    time_zone = pytz.timezone("Brazil/East")
    date_time = datetime.now(time_zone)
    # time = datetime.strftime("%d/%m as %H:%M:%S")
    time = date_time.strftime("%H:%M:%S")
    return time

def getDate():
    time_zone = pytz.timezone("Brazil/East")
    date_time = datetime.now(time_zone)
    date_date = date_time.strftime("%d/%m as %H:%M")
    return date_date

def checkFiles():
    pastas = ["config", "escolas", "resources", "grupo actteens", "imaculada conceicao", "jose pavan", "luiz setti", "rui barbosa"]
    arquivos = ["chromedriver.exe", "dados.json", "config.json", "todos.xlsx", "banner.png", "favicon.ico", "functionMessage.py", "genGraph.py", "interface.py"]
    grupo_actteens = ["grupo"]
    imaculada_conceicao = ["8C", "8D", "9B", "9D"]
    jose_pavan = ["8A", "8B", "9A", "9B"]
    luiz_setti = ["8A", "9C"]
    rui_barbosa = ["8A", "9A"]
    checkPastas = []
    checkArquivos = []
    checkArquivosExcel = []
    for pasta in pastas:
        if path.exists(pasta):
            for arquivo in arquivos:
                if path.exists(f"{pasta}/{arquivo}"):
                    checkArquivos.append(arquivo)
                if path.exists(arquivo):
                    checkArquivos.append(arquivo)
        elif path.exists(f"escolas/{pasta}"):
            convertVar = pasta.replace(" ", "_")
            for arquivo in eval(convertVar):
                if not path.exists(f"escolas/{pasta}/{arquivo}.xlsx"):
                    checkArquivosExcel.append(f"escolas/{pasta}/{arquivo}.xlsx")
        else:
            checkPastas.append(pasta)

    checkArquivos = [ p for p in arquivos if p not in checkArquivos ]
    return checkPastas, checkArquivos, checkArquivosExcel

checkFiles()

def banner():
    banner = r"""
 ________  ________ _________        _________  _______   _______   ________   ________      
 |\   __  \|\   ____\\___   ___\     |\___   ___\\  ___ \ |\  ___ \ |\   ___  \|\   ____\     
 \ \  \|\  \ \  \___\|___ \  \_|     \|___ \  \_\ \   __/|\ \   __/|\ \  \\ \  \ \  \___|_    
  \ \   __  \ \  \       \ \  \           \ \  \ \ \  \_|/_\ \  \_|/_\ \  \\ \  \ \_____  \   
   \ \  \ \  \ \  \____   \ \  \           \ \  \ \ \  \_|\ \ \  \_|\ \ \  \\ \  \|____|\  \  
    \ \__\ \__\ \_______\  \ \__\           \ \__\ \ \_______\ \_______\ \__\\ \__\____\_\  \ 
    \|__|\|__|\|_______|   \|__|            \|__|  \|_______|\|_______|\|__| \|__|\_________\
                                                                                  \|_________|
                                                                                  
-----------------------------------------------------------------------------------------------------"""
    return banner