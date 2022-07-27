#!/usr/bin/env python
# coding: utf-8

# EXTENSAO 
# https://chrome.google.com/webstore/detail/wa-web-plus-for-whatsapp/ekcgkejcjdcmonfpmnljobemcbpnkamh

import re
import pandas as pd
import os
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import io
from colorama import Fore, Style, init
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import urllib
from selenium import webdriver
from time import sleep
import pytz
import datetime
from datetime import datetime
import sys
import json
from utils import *
import matplotlib.pyplot as plt 
import matplotlib
import numpy as np 
import utils

clear = lambda: os.system('cls')

def saveData(escola, turma, contadorSucesso, contadorFalha, timeStart, timeEnd):
    try:
        with open("config/dados.json", "r") as f:
            dados = json.load(f)

        dados[escola][turma]["mensagens enviadas"] += contadorSucesso
        dados[escola][turma]["mensagens nao enviadas"] += contadorFalha
        dados["total"]["mensagens enviadas"] += contadorSucesso
        dados["total"]["mensagens nao enviadas"] += contadorFalha
        dados["total"]["tempo medio gasto por turma"] = ((dados["total"]["tempo medio gasto por turma"] + (timeEnd - timeStart))/2)

        with open("config/dados.json", "w") as f:
            json.dump(dados, f, indent=4)

        print(warningFormat.format("\n------------------------------------------------------"))
        print(validFormat.format(f"\nRELATÓRIO - {getDate()}"))
        print(validFormat.format(f" Mensagens enviadas: {contadorSucesso}"))
        print(validFormat.format(f" Erro ao enviar mensagens: {contadorFalha}"))
        print(validFormat.format(f" Tempo gasto: {timeEnd - timeStart}"))
        print(warningFormat.format("\n------------------------------------------------------"))
    except Exception as E:
        print(errorFormat.format("---------------- Erro -----------------"))
        print(errorFormat.format(E))
        print(errorFormat.format("---------------------------------------"))
        return        

def existExcel(escola, turma):
    try:
        contatos_df = pd.read_excel(f"escolas/{escola}/{turma}.xlsx")
        return contatos_df
    except Exception as E:
        print(errorFormat.format(f'Planilha "escolas/{escola}/{turma}.xlsx" não encontrada'))
        return False

def sendFile(escola, turma, filepath):
    contatos_df = existExcel(escola, turma)
    if contatos_df == False:
        return
        
    try:
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir=C:/Users/{os.getenv('UserName')}/AppData/Local/Google/Chrome/User Data")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        executable_path = Service('config/chromedriver.exe')
        navegador = webdriver.Chrome(service=executable_path,
                                options=options)
        navegador.get("https://web.whatsapp.com/")
    except:
        print(errorFormat.format(f'Erro ao abrir whatsappWeb\n - Finalize todos os processo relacionado ao google chrome\ne execute o programa novamente'))
        return
        

    print(warningFormat.format("Aguardando efetuar login no WhatsappWeb..."))
    while len(navegador.find_elements(by=By.ID, value="side")) < 1:
        time.sleep(1)

    print(validFormat.format("Login efetuado com sucesso"))

    time.sleep(5)

    contadorSucesso = 0
    contadorFalha = 0
    timeStart = time.time()
    for i, mensagem in enumerate(contatos_df['Aluno']):
        try:
            pessoa = contatos_df.loc[i, "Aluno"]
            numero = str(contatos_df.loc[i, "Número aluno"])
            if numero.startswith("5"):
                if numero.endswith(".0"):
                    numero = numero[:-2]
                                                
                actions = navegador.find_elements(by=By.TAG_NAME, value="body")[0]
                actions.send_keys(Keys.CONTROL, Keys.ALT, "s")
                
                time.sleep(1)
                
                writeNumber = navegador.find_elements(by=By.XPATH, value=f'//input[@placeholder="Número de telefone"]')[0]
                writeNumber.send_keys(numero)
                        
                checkNumber = navegador.find_elements(by=By.XPATH, value=f'//a[@class="btn-ok"]')[0]
                checkNumber.click()
                        
                time.sleep(2)
                
                try:
                    auxOK = navegador.find_elements(by=By.XPATH, value=f'//div[@data-testid="popup-controls-ok"]')[0]
                    auxOK.click()
                    time.sleep(1)
                    continue
                except:
                    pass
                
                while len(navegador.find_elements(by=By.XPATH, value=f'//div[@title="Mensagem"]')) < 1:
                    time.sleep(1)
                time.sleep(1)
                            
                clipAttachment = navegador.find_elements(by=By.XPATH, value='//span[@data-icon="clip"]')[0]
                clipAttachment.click()
                
                searchImage  = navegador.find_elements(by=By.XPATH, value='//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')[0]
                searchImage.send_keys(filepath)
                
                time.sleep(3)

                sendImage = navegador.find_elements(by=By.XPATH, value='//span[@data-icon="send"]')[0]
                sendImage.click()
                
                time.sleep(3)
                
                print(validFormat.format(f'[{contadorSucesso}] Mensagem enviada | Nome: {pessoa} | Numero: {numero}'))
                contadorSucesso += 1
                time.sleep(1)
        except Exception as E:
            contadorFalha += 1
            print(errorFormat.format(f'Erro ao enviar mensagem | Nome: {pessoa}  | Numero: {numero}'))

    navegador.quit()
    timeEnd = time.time()
    saveData(escola, turma, contadorSucesso, contadorFalha, timeStart, timeEnd)

def sendMessage(escola, turma, mensagem):
    texto = io.open(mensagem,'r', encoding="utf8").read()

    contatos_df = existExcel(escola, turma)
    if contatos_df == False:
        return

    try:
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir=C:/Users/{os.getenv('UserName')}/AppData/Local/Google/Chrome/User Data")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        executable_path = Service('config/chromedriver.exe')
        navegador = webdriver.Chrome(service=executable_path,
                                options=options)
        navegador.get("https://web.whatsapp.com/")
    except:
        print(errorFormat.format(f'Erro ao abrir whatsappWeb\n - Finalize todos os processo relacionado ao google chrome\ne execute o programa novamente'))
        return
        

    print(warningFormat.format("Aguardando efetuar login no WhatsappWeb..."))
    while len(navegador.find_elements(by=By.ID, value="side")) < 1:
        time.sleep(1)

    print(validFormat.format("Login efetuado com sucesso"))

    time.sleep(5)

    contadorSucesso = 0
    contadorFalha = 0
    timeStart = time.time()
    for i, mensagem in enumerate(contatos_df['Aluno']):
        try:
            pessoa = contatos_df.loc[i, "Aluno"]
            numero = str(contatos_df.loc[i, "Número aluno"])
            if numero.startswith("5"):
                if numero.endswith(".0"):
                    numero = numero[:-2]
                                    
                actions = navegador.find_elements(by=By.TAG_NAME, value="body")[0]
                actions.send_keys(Keys.CONTROL, Keys.ALT, "s")
                
                time.sleep(1)
                
                writeNumber = navegador.find_elements(by=By.XPATH, value=f'//input[@placeholder="Número de telefone"]')[0]
                writeNumber.send_keys(numero)
                        
                checkNumber = navegador.find_elements(by=By.XPATH, value=f'//a[@class="btn-ok"]')[0]
                checkNumber.click()
                        
                time.sleep(2)
                
                try:
                    auxOK = navegador.find_elements(by=By.XPATH, value=f'//div[@data-testid="popup-controls-ok"]')[0]
                    auxOK.click()
                    time.sleep(1)
                    continue
                except:
                    pass
                
                while len(navegador.find_elements(by=By.XPATH, value=f'//div[@title="Mensagem"]')) < 1:
                    time.sleep(1)
                time.sleep(1)
                
                campoDigitarMensagem = navegador.find_elements(by=By.XPATH, value=f'//div[@title="Mensagem"]')[0]
                campoDigitarMensagem.click()
                campoDigitarMensagem.send_keys(str(texto))

                time.sleep(1)

                botaoEnviarMensagem = navegador.find_elements(by=By.XPATH, value='//button/span[@data-icon="send"]')[0]
                botaoEnviarMensagem.click()
                
                print(validFormat.format(f'[{contadorSucesso}] Mensagem enviada | Nome: {pessoa} | Numero: {numero}'))
                contadorSucesso += 1
                time.sleep(1)
        except Exception as E:
            contadorFalha += 1
            pass
        
    navegador.quit()
    timeEnd = time.time()
    saveData(escola, turma, contadorSucesso, contadorFalha, timeStart, timeEnd)

def sendMessageTodos(escola, turma, mensagem):
    texto = io.open(mensagem,'r', encoding="utf8").read()

    contatos_df = existExcel(escola, turma)
    if contatos_df == False:
        return
        
    try:
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir=C:/Users/{os.getenv('UserName')}/AppData/Local/Google/Chrome/User Data")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        executable_path = Service('config/chromedriver.exe')
        navegador = webdriver.Chrome(service=executable_path,
                                options=options)
        navegador.get("https://web.whatsapp.com/")
    except Exception as E:
        print(errorFormat.format(f'Erro ao abrir whatsappWeb\n - Finalize todos os processo relacionado ao google chrome\ne execute o programa novamente'))
        return
        

    print(warningFormat.format("Aguardando efetuar login no WhatsappWeb..."))
    while len(navegador.find_elements(by=By.ID, value="side")) < 1:
        time.sleep(1)

    print(validFormat.format("Login efetuado com sucesso"))

    time.sleep(5)

    contadorSucesso = 0
    contadorFalha = 0
    timeStart = time.time()
    for i, mensagem in enumerate(contatos_df['Aluno']):
        try:
            if turma == "alunos":
                numero = str(contatos_df.loc[i, "Número aluno"])
            else:
                numero = str(contatos_df.loc[i, "Número responsável"])
            if numero.startswith("5"):
                if numero.endswith(".0"):
                    numero = numero[:-2]                
                pessoa = contatos_df.loc[i, "Aluno"]
                                    
                actions = navegador.find_elements(by=By.TAG_NAME, value="body")[0]
                actions.send_keys(Keys.CONTROL, Keys.ALT, "s")
                            
                time.sleep(1)

                writeNumber = navegador.find_elements(by=By.XPATH, value=f'//input[@placeholder="Número de telefone"]')[0]
                writeNumber.send_keys(numero)
                                            
                checkNumber = navegador.find_elements(by=By.XPATH, value=f'//a[@class="btn-ok"]')[0]
                checkNumber.click()
                
                time.sleep(3)
                
                try:
                    auxOK = navegador.find_elements(by=By.XPATH, value=f'//div[@data-testid="popup-controls-ok"]')[0]
                    auxOK.click()
                    time.sleep(1)
                    continue
                except:
                    pass
                
                while len(navegador.find_elements(by=By.XPATH, value=f'//div[@title="Mensagem"]')) < 1:
                    time.sleep(1)
                
                campoDigitarMensagem = navegador.find_elements(by=By.XPATH, value=f'//div[@title="Mensagem"]')[0]
                campoDigitarMensagem.click()
                campoDigitarMensagem.send_keys(str(texto))

                time.sleep(1)

                botaoEnviarMensagem = navegador.find_elements(by=By.XPATH, value='//button/span[@data-icon="send"]')[0]
                botaoEnviarMensagem.click()
                
                print(validFormat.format(f'[{contadorSucesso}] Mensagem enviada | Nome: {pessoa} | Numero: {numero}'))
                contadorSucesso += 1
                time.sleep(1)
        except Exception as E:
            contadorFalha += 1
            pass
        
    navegador.quit()
    timeEnd = time.time()
    saveData(escola, turma, contadorSucesso, contadorFalha, timeStart, timeEnd)

def sendFileTodos(escola, turma, filepath):
    contatos_df = existExcel(escola, turma)
    if contatos_df == False:
        return

    try:
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir=C:/Users/{os.getenv('UserName')}/AppData/Local/Google/Chrome/User Data")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        executable_path = Service('config/chromedriver.exe')
        navegador = webdriver.Chrome(service=executable_path,
                                options=options)
        navegador.get("https://web.whatsapp.com/")
    except Exception as E:
        print(errorFormat.format(f'Erro ao abrir whatsappWeb\n - Finalize todos os processo relacionado ao google chrome\ne execute o programa novamente'))
        return

    print(warningFormat.format("Aguardando efetuar login no WhatsappWeb..."))
    while len(navegador.find_elements(by=By.ID, value="side")) < 1:
        time.sleep(1)

    print(validFormat.format("Login efetuado com sucesso"))

    time.sleep(5)

    contadorSucesso = 0
    contadorFalha = 0
    timeStart = time.time()
    for i, mensagem in enumerate(contatos_df['Aluno']):
        try:
            if turma == "alunos":
                numero = str(contatos_df.loc[i, "Número aluno"])
            else:
                numero = str(contatos_df.loc[i, "Número responsável"])
                
            if numero.startswith("5"):
                if numero.endswith(".0"):
                    numero = numero[:-2]   
                pessoa = contatos_df.loc[i, "Aluno"]

                actions = navegador.find_elements(by=By.TAG_NAME, value="body")[0]
                actions.send_keys(Keys.CONTROL, Keys.ALT, "s")
                
                time.sleep(1)
                
                writeNumber = navegador.find_elements(by=By.XPATH, value=f'//input[@placeholder="Número de telefone"]')[0]
                writeNumber.send_keys(numero)
                        
                checkNumber = navegador.find_elements(by=By.XPATH, value=f'//a[@class="btn-ok"]')[0]
                checkNumber.click()
                        
                time.sleep(2)
                
                try:
                    auxOK = navegador.find_elements(by=By.XPATH, value=f'//div[@data-testid="popup-controls-ok"]')[0]
                    auxOK.click()
                    time.sleep(1)
                    continue
                except:
                    pass
                
                while len(navegador.find_elements(by=By.XPATH, value=f'//div[@title="Mensagem"]')) < 1:
                    time.sleep(1)
                time.sleep(1)
                
                clipAttachment = navegador.find_elements(by=By.XPATH, value='//span[@data-icon="clip"]')[0]
                clipAttachment.click()
                
                searchImage  = navegador.find_elements(by=By.XPATH, value='//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')[0]
                searchImage.send_keys(filepath)
                
                aux = 0
                while aux == 0:
                    try:
                        sendImage = navegador.find_elements(by=By.XPATH, value='//span[@data-icon="send"]')[0]
                        sendImage.click()
                        aux += 1
                    except:
                        time.sleep(1)

                time.sleep(5)
                contadorSucesso += 1
                print(validFormat.format(f'[{contadorSucesso}] Mensagem enviada | Nome: {pessoa} | Numero: {numero}'))
        except Exception as E:
            contadorFalha += 1
            print(errorFormat.format(f'Erro ao enviar mensagem | Nome: {pessoa}  | Numero: {numero}'))

    navegador.quit()
    timeEnd = time.time()
    saveData(escola, turma, contadorSucesso, contadorFalha, timeStart, timeEnd)