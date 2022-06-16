from turtle import width
import matplotlib.pyplot as plt
import numpy as np 
import json
from functionMessage import *
from utils import getDate

def genGraph():
    with open("config/dados.json", "r") as f:
        dados = json.load(f)

    width = 0.15

    x1 = np.arange(3)
    x2 = [x + width for x in x1]
    x3 = [x + width for x in x2]

    azul = list(map(float, [dados["todos"]["alunos"]['mensagens enviadas'], dados["todos"]["responsaveis"]['mensagens enviadas'], dados["total"]['mensagens enviadas']]))
    verde = list(map(float, [dados["todos"]["alunos"]['mensagens nao enviadas'], dados["todos"]["responsaveis"]['mensagens nao enviadas'], dados["total"]['mensagens nao enviadas']]))



    fig, ax = plt.subplots(num="Gráfico automação ActTeens")

    def add_value_label(x_list,y_list):
        for i in range(1, len(x_list)+1):
            plt.text(x_list[i-1],y_list[i-1],int(y_list[i-1]), ha="center")

    plt.bar(x1, azul, color='blue', width=width, edgecolor='white', label='Mensagens enviadas')
    plt.bar(x2, verde, color='green', width=width, edgecolor='white', label='Mensagens não enviadas')
    add_value_label(x1,azul)
    add_value_label(x1+0.2,verde)

    ax.set_ylabel('Quantidade de mensagens')
    ax.set_title(f'Gráfico ACTTEENS ({getDate()})')
    ax.set_xticks(x1)
    ax.set_xticklabels(['Alunos', 'Responsaveis', 'Total'])
    ax.legend()

    fig.tight_layout()

    plt.show()

    