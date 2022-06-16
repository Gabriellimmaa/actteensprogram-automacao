import io
import os
import PySimpleGUI as sg
from PIL import Image
from numpy import size
from utils import *
from functionMessage import *
from threading import Thread
from time import sleep
import asyncio
from multiprocessing import Process, Queue
from genGraph import *

sg.theme("DarkBlue13")

file_types = [("All files (*.*)", "*.*")]


_escolas = ['imaculada conceicao', 'luiz setti', 'rui barbosa',
            'jose pavan', 'grupo actteens', 'todos::alunos', 'todos::responsaveis']

_colunaSalaCombo = "colunaSala-combo"
_colunaSalaText = "colunaSala-text"

BAR_WIDTH = 50      # width of each bar
BAR_SPACING = 75    # space between each bar
EDGE_OFFSET = 3     # offset from the left edge for first bar
GRAPH_SIZE= DATA_SIZE = (500,500)       # size in pixels


# Coluna de escola e sala
colunaEscola = [
    [sg.Text("Selecione a escola:")],
    [sg.Checkbox('Imaculada Conceição', default=False,
                 key="imaculada conceicao", enable_events=True)],
    [sg.Checkbox('Luiz Setti', default=False,
                 key="luiz setti", enable_events=True)],
    [sg.Checkbox('Rui Barbosa', default=False,
                 key="rui barbosa", enable_events=True)],
    [sg.Checkbox('José Pavan', default=False,
                 key="jose pavan", enable_events=True)],
    [sg.Checkbox('Grupo Actteens', default=False,
                 key="grupo actteens", enable_events=True)],
    [sg.Checkbox('Enviar para todos os alunos', default=False,
                 key="todos::alunos", enable_events=True)],
    [sg.Checkbox('Enviar para todos os responsáveis', default=False,
                 key="todos::responsaveis", enable_events=True)]
]
colunaSala = [
    [sg.Text("Selecione uma escola primeiro...", key=_colunaSalaText)],
    [sg.Combo(values=[], default_value='...', key=_colunaSalaCombo,
              size=(245, 20), visible=False, enable_events=True)],
]

_telaInicio = [
    [sg.Text("Selecione o arquivo:")],
    [sg.Input(key="-FILE-", size=(55, 25)),
     sg.FileBrowse(file_types=file_types)],

    [sg.Column(colunaEscola, vertical_alignment="top"),
     sg.Column(colunaSala, vertical_alignment="top")],
    [sg.Button('Enviar mensagens', size=(100, 1), key="SUBMIT")],
    [sg.Multiline(' -------- ACTTEENS Console logs -------- \n', size=(100, 100),
                  autoscroll=True, reroute_stdout=True, reroute_stderr=True, key='-OUTPUT-')]
]

_telaConfig = [
    [sg.Text("Verificar integridade do software")],
    [sg.Button('Verificar integridade', key="verificarIntegridade")],
    [sg.Text("Gráficos:")],
    [sg.Button('Gerar gráfico do software', key="graficoTotal")]
]

# Layout da aplicação
layout = [
    [sg.Image("resources/banner.png", size=(600, 100))],
    [sg.TabGroup([[sg.Tab('Inicio', _telaInicio), sg.Tab('Config', _telaConfig)]])],
]

def main():
    window = sg.Window('Automação ACTTEENS - Whatsapp', layout, size=(600, 650))
    window.set_icon("resources/favicon.ico")

    while True:
        event, values = window.read()
        print(event)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "graficoTotal":
            genGraph()
        if event == "verificarIntegridade":
            check = checkFiles()
            if (len(check[0]) + len(check[1]) + len(check[2])) == 0:
                sg.Popup(f'Integridade do software está em 100%', keep_on_top=True)   
                continue 
            aux1 = ""
            aux2 = ""
            aux3 = ""
            for x in check[0]:
                aux1 += f"{x} \n"
            for x in check[1]:
                aux2 += f"{x} \n"
            for x in check[2]:
                aux3 += f"{x} \n"

            sg.Popup(f'Integridade das pastas: \n{aux1}\n\nIntegridade dos arquivos: \n{aux2}\n\nIntegridade dos excel: \n{aux3}', keep_on_top=True)
        if event == "SUBMIT":
            escola = ""
            turma = values[_colunaSalaCombo]
            filepath = values["-FILE-"]

            for x in values.keys():
                if values[x] == True:
                    if "::" in x:
                        aux = x.split("::")
                        escola += aux[0]
                    else:
                        escola += x
            if escola == "":
                print(f"[{getTime()}] Você não selecionou uma escola")
                continue
            if turma == "" or turma == "...":
                print(f"[{getTime()}] Você não selecionou uma turma")
                continue
            if filepath == "":
                print(f"[{getTime()}] Você não selecionou um arquivo")
                continue

            print(
                f"Escola: {escola}\nTurma: {turma}\nTipo mensagem: Imagem / Video\n")
                
            thread = Thread(target = sendFileTodos, args = (escola, turma, filepath))
            thread.start()
        if event in _escolas:
            for value in _escolas:
                if value != event:
                    window.find_element(value).Update(False)
            window.find_element("colunaSala-text").Update("Selecione uma turma:")
            window.find_element("colunaSala-combo").Update(visible=True)
            if event == "imaculada conceicao":
                window.find_element(_colunaSalaCombo).Update(
                    values=['8C', '8D', '9B', '9D'])
            elif event == "luiz setti":
                window.find_element(_colunaSalaCombo).Update(
                    values=['8A', '9C'])
            elif event == "rui barbosa":
                window.find_element(_colunaSalaCombo).Update(
                    values=['8A', '9A'])
            elif event == "jose pavan":
                window.find_element(_colunaSalaCombo).Update(
                    values=['8A', '8B', '9A', '9B'])
            elif event == "grupo actteens":
                window.find_element(_colunaSalaCombo).Update(
                    values=['grupo'])
            elif event == "todos::alunos":
                window.find_element(_colunaSalaCombo).Update(
                    values=['alunos'])
            if event == "todos::responsaveis":
                window.find_element(_colunaSalaCombo).Update(
                    values=['responsaveis'])
    window.close()

if __name__ == "__main__":
    main()
