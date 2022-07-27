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
from datetime import datetime

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

try:
    options = webdriver.ChromeOptions()
    options.add_argument(
        f"--user-data-dir=C:/Users/{os.getenv('UserName')}/AppData/Local/Google/Chrome/User Data")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    executable_path = Service('config/chromedriver.exe')
    navegador = webdriver.Chrome(service=executable_path,
                                    options=options)
    navegador.get("https://web.whatsapp.com/")
except Exception as E:
    print(errorFormat.format(
        f'Erro ao abrir whatsappWeb\n - Finalize todos os processo relacionado ao google chrome\ne execute o programa novamente'))

print(warningFormat.format("Aguardando efetuar login no WhatsappWeb..."))
while len(navegador.find_elements(by=By.ID, value="side")) < 1:
    time.sleep(1)

print(validFormat.format("Login efetuado com sucesso"))

time.sleep(5)

contadorSucesso = 0
contadorFalha = 0

actions = navegador.find_elements(by=By.TAG_NAME, value="body")[0]
actions.send_keys(Keys.CONTROL, Keys.ALT, "s")

writeNumber = navegador.find_elements(by=By.XPATH, value=f'//input[@placeholder="Número de telefone"]')[0]
writeNumber.send_keys("14997391223")

checkNumber = navegador.find_elements(
    by=By.XPATH, value=f'//a[@class="btn-ok"]')[0]
checkNumber.click()

time.sleep(2)

try:
    auxOK = navegador.find_elements(by=By.XPATH, value=f'//div[@data-testid="popup-controls-ok"]')[0]
    auxOK.click()
    time.sleep(1)
    input("deu erro nessa merda")
except:
    pass

while len(navegador.find_elements(by=By.XPATH, value=f'//div[@title="Mensagem"]')) < 1:
    time.sleep(1)
time.sleep(1)

campoDigitarMensagem = navegador.find_elements(by=By.XPATH, value=f'//div[@title="Mensagem"]')[0]
campoDigitarMensagem.click()
campoDigitarMensagem.send_keys(str("TESTETESSTESTE"))

time.sleep(1)

botaoEnviarMensagem = navegador.find_elements(by=By.XPATH, value='//button/span[@data-icon="send"]')[0]
botaoEnviarMensagem.click()
time.sleep(1)