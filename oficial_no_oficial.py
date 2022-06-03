# from datetime import datetime, timedelta
import shutil
import configparser
from time import sleep
from tkinter import *
from tkinter import ttk

#Função pra retornar a ultima Apo que foi atualizada
def ultima_apo():
    cfg = configparser.ConfigParser()
    cfg.read(r'D:\TOTVS\PROTHEUS\bin\Monitor\appserver.ini')
    ultima_apo_atual = cfg.get("QUEIROZ","SourcePath")
    return ultima_apo_atual[23:]

#Função que vai copiar a RPO do Oficial e enviar para a pasta Apo
def copia_apo_oficial():
    """caminho do repositorio oficio"""
    source = r'D:\TOTVS\PROTHEUS\Apos\Oficial\TTTP120.RPO' 
    """caminho do repositorio a ser atualizado"""
    destino_apo = fr'D:\TOTVS\PROTHEUS\{combo_lista_apo.get()}\TTTP120.RPO' # apo selecionada
    destino_schedule = fr'D:\TOTVS\PROTHEUS\Apos\Schedule\TTTP120.RPO'  #Schedule
    copia_apo = shutil.copy2(source,destino_apo)
    copia_schedule = shutil.copy2(source,destino_schedule)
    
    if copia_apo and copia_schedule:
        atualizar_ini()
    return

# Atualizar os arquivos INI.
def atualizar_ini():
    
    pasta = [ r'D:\TOTVS\PROTHEUS\bin\Monitor\appserver.ini',
                r'D:\TOTVS\PROTHEUS\bin\Slave01\appserver.ini',
                r'D:\TOTVS\PROTHEUS\bin\Slave02\appserver.ini',
                r'D:\TOTVS\PROTHEUS\bin\Slave03\appserver.ini',
                r'D:\TOTVS\PROTHEUS\bin\Slave04\appserver.ini',
                r'D:\TOTVS\PROTHEUS\bin\Slave05\appserver.ini',
                r'D:\TOTVS\PROTHEUS\bin\Slave06\appserver.ini',
                r'D:\TOTVS\PROTHEUS\bin\Slave07\appserver.ini',
                r'D:\TOTVS\PROTHEUS\bin\Slave08\appserver.ini',
                r'D:\TOTVS\PROTHEUS\bin\Slave09\appserver.ini',
                r'D:\TOTVS\PROTHEUS\bin\Slave10\appserver.ini',
                r'D:\TOTVS\PROTHEUS\bin\SlaveEX\appserver.ini',
                r'D:\TOTVS\PROTHEUS\bin_comp\appserver2\appserver.ini'
                ]
    
    for appserver in pasta: #passa pela lista contendo o caminho da pasta que conten o arquivo appserve.ini
        cfg = configparser.ConfigParser()
        cfg.optionxform = str # função para escrever as letras maiscula ( o padrao sobreescreve o arquivo inteiro em minusculo )
        cfg.read(appserver) # abrir arquivo ler
        cam_rpo = cfg.get('QUEIROZ','SourcePath') #pegar o caminho do apo no INI 
        apo = combo_lista_apo.get() #pegar o Apo que foi selecionada para subistituir no arquivo
        cfg.set('QUEIROZ', 'SourcePath', cam_rpo[:23]+apo) # passar para o arquivo o novo caminho
        
        with open(appserver, "w") as ArqTeste: #abrir o arquivo e gravar
            cfg.write(ArqTeste)
            ArqTeste.close()
            sleep(1)
            barra()
    return
def barra():
    progress1['value'] +=33.33
    
        
# Tela  
root = Tk()
root.geometry('300x250+200+200')
root.title('Oficial no Oficial')
root.iconbitmap(r"icone\favicon.ico")

# desativa o maximizar
root.resizable(0,0)

root['bg'] = '#F0F8FF'

barra_titulo = Frame(root,background='#F5FFFA', bd=1,relief=SUNKEN, padx=30)
barra_titulo.grid(columnspan=2,sticky='w')

lb_titulo = Label(barra_titulo,background='#F5FFFA', foreground='black',font=('Times New Roman',12), text='Atualizaçao do Repositório do Sistema')
lb_titulo.grid()

#mostra na Tela a ultima Apo

fr_apo = Frame(root,background='black', bd=1,relief=SUNKEN)
fr_apo.grid(pady=20,sticky='',columnspan=2)
apo_label = Label(fr_apo,text=f'Atualizada: {ultima_apo()} ',font=('',10))

apo_label.grid()

#combobox selecionar a Apo para atualizar
ttk.Label(root,background='#F0F8FF',text='Selecione ',font=('',10)).grid(column=0, row=3,padx=40,sticky='w',columnspan=2)
lista_apo = ['apo1','apo2','apo3','apo4','apo5']

combo_lista_apo=ttk.Combobox(root,values=lista_apo, foreground='#000080')
combo_lista_apo.set(f'{ultima_apo()}')
combo_lista_apo.grid(column=1,padx=40,row=4,sticky='w')

# Barra de progresso
progress1 = ttk.Progressbar(root, orient=HORIZONTAL,length=310,mode='determinate')
progress1.grid(column=1,row=7,columnspan=2,sticky='w')


ttk.Button(root, text="Quit",command=root.destroy).grid(column=1,row=6,padx=50,sticky='w')
ttk.Button(root,text="OK",command=copia_apo_oficial).grid(column=1, row=6,padx=50,pady=35,sticky='e')
# ttk.Button(root, text="Refresh",command=refresh(),padding=4).grid(row=1,padx=20,columnspan=2,sticky='e')

root.mainloop()