# -*- coding: utf-8 -*-
from Tkinter import *
import tkFileDialog
import tkMessageBox
import os
import webbrowser

global FONT
FONT = ('Arial', '12')

class Interface(object):
    def __init__(self, root):
        self.root = root
        root.geometry("600x550+300+100")
        root.minsize(width='600', height='550')
        root.title('Planilha do Professor')
        ##Label inicial##
        self.frame=Frame(root)
        self.frame.pack()
        label=Label(self.frame, font=FONT, text='\n\n\nBem-vind@ ao programa Planilha do Professor\n'
                               'Originalmente desenvolvido e concebido por Lucas Kirsten\n\n'
                               "Para informações de contato e tutoriais clique no menu 'Ajuda'").pack()
        ##MENUS##
        menubar = Menu(root)
            ##Arquivo
        arquivo_menu = Menu(menubar, tearoff=0)
        arquivo_menu.add_command(label='Nova Turma', command=self.nova_turma,accelerator="Ctrl+N")
        root.bind('<Control-n>', self.nova_turma)
        arquivo_menu.add_command(label='Editar Turma', command=self.editar_turma,accelerator="Ctrl+E")
        root.bind('<Control-e>', self.editar_turma)
        arquivo_menu.add_command(label='Carregar Turma', command=self.carregar_turma,accelerator="Ctrl+O")
        root.bind('<Control-o>', self.carregar_turma)
        arquivo_menu.add_command(label='Salvar', command=self.salvar_atual,accelerator="Ctrl+S")
        root.bind('<Control-s>', self.salvar_atual)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label='Gerar Planilha', command=self.gerar_planilha,accelerator="Ctrl+P")
        root.bind('<Control-p>', self.gerar_planilha)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label='Sair', command=root.quit)
        menubar.add_cascade(label='Arquivo', menu=arquivo_menu)
            ##Opções
        self.definir_aulas = BooleanVar()  #Variaveis
        self.definir_aulas.set(False)       #de
        self.calculo_notas = StringVar()    #comando
        self.calculo_notas.set('media')     #
        self.presenca = BooleanVar()        #
        self.presenca.set(True)             #
        opcoes_menu = Menu(menubar, tearoff=0)
        opcoes_menu.add_radiobutton(label='Fazer Média',variable=self.calculo_notas, value='media')
        opcoes_menu.add_radiobutton(label='Calcular',variable=self.calculo_notas, value='calcular')
        opcoes_menu.add_separator()
        opcoes_menu.add_checkbutton(label='Definir Aulas',variable=self.definir_aulas, onvalue=True, offvalue=False)
        opcoes_menu.add_separator()
        opcoes_menu.add_radiobutton(label='Presença',variable=self.presenca, value=True)
        opcoes_menu.add_radiobutton(label='Ausência',variable=self.presenca, value=False)
        menubar.add_cascade(label='Opções', menu=opcoes_menu)
            ##Ajuda
        ajuda_menu = Menu(menubar, tearoff=0)
        ajuda_menu.add_command(label='Tutoriais', command=self.tutoriais)
        ajuda_menu.add_command(label='Sobre', command=self.sobre)
        menubar.add_cascade(label='Ajuda', menu=ajuda_menu)
        root.config(menu=menubar)
        ###

    def sobre(self):
        tkMessageBox.showinfo('Sobre','Programa Planilha do Professor\n'
                              'Versão 1.0\n\n'
                              'Criado por Lucas Kirsten\n'
                              'Contato: lucasn.kirsten@hotmail.com')

    def tutoriais(self):
        def abrirVideo(event):
            webbrowser.open_new(r'http://www.google.com')

        tuto = Toplevel(self.root)
        tuto.minsize(width='200', height='150')
        tuto.maxsize(width='200', height='150')
        tuto.title('Tutoriais')
        label= Label(tuto, text='Vídeo-Tutorial no Youtube:', font=FONT).pack()
        labelLink = Label(tuto, text='<link do video>',cursor='hand2', underline=1, fg='blue', font=FONT)
        labelLink.pack()
        labelLink.bind('<Button-1>', abrirVideo)
        label= Label(tuto, text='\nDocumentação:\n'
                           '...em construção...', font=FONT).pack()

    def editar_turma(self, event=None):
        arquivo = tkFileDialog.askopenfile(title='Abrir arquivo de nomes...', mode='r',defaultextension=".txt",filetypes=[('Texto','*.txt')])
        nome_turma = arquivo.readline().replace('\n','')
        arquivo.seek(arquivo.tell())
        texto = arquivo.read()
        arquivo.close()
        self.nova_turma()
        self.eTurma.insert(END, nome_turma)
        self.tNomes_alunos.insert(END, texto)

    ##Cria uma Nova Turma partindo dos nomes
    def nova_turma(self, event=None):
        try:
            self.fNomes.destroy()
        except:
            pass
        try:
            self.frame.destroy()
        except:
            pass
        #Salva o arquivo com o nome dos alunos
        def salvar_nomes():
            if self.eTurma.get()=='':
                tkMessageBox.showerror('Ocorreu um erro', 'Não foi fornecido um nome a turma')
            else:
                self.nome_turma = self.eTurma.get()
                arquivo = tkFileDialog.asksaveasfile(title='Salvar nomes da turma como...',mode='w',defaultextension=".txt",filetypes=[('Texto','*.txt')])
                texto = self.nome_turma+'\n'+self.tNomes_alunos.get(0.0,END)
                arquivo.write(texto)
                arquivo.close()
        #Widgets usados
        self.fNomes = Frame(self.root)
        self.fNomes.pack()
        labelTurma = Label(self.fNomes, text='Nome da Turma:', font=FONT).pack()
        self.eTurma = Entry(self.fNomes, font=FONT, width=30)
        self.eTurma.pack()
        labelNome = Label(self.fNomes, text='Nome dos Alunos:', font=FONT).pack()
        fAlunos = Frame(self.fNomes)
        fAlunos.pack()
        scrollbar = Scrollbar(fAlunos)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tNomes_alunos = Text(fAlunos, font=FONT, yscrollcommand=scrollbar.set)
        self.tNomes_alunos.pack()
        scrollbar.config(command=self.tNomes_alunos.yview)
        buttonPronto = Button(self.fNomes, text='Armazenar', font=FONT, command=salvar_nomes).pack(side=LEFT, padx=80, pady=5)
        buttonSair = Button(self.fNomes, text='Sair', font=FONT, command=self.fNomes.destroy).pack(side=RIGHT, padx=80, pady=5)

    ##Carrega os dados de uma turma já existente
    def carregar_turma(self, event=None):
        def myfunction(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"), width='600', height='600')
        try:
            self.fNomes.destroy()
        except:
            pass
        try:
            self.frame.destroy()
        except:
            pass
        self.arquivo = tkFileDialog.askopenfile(defaultextension=[".txt"],filetypes=[('Texto','*.txt')], mode='r')
        self.nome_turma = self.arquivo.readline()
        self.arquivo.seek(self.arquivo.tell())
        texto = self.arquivo.readlines()
        self.arquivo.close()
        info = []
        for linha in texto:
            if linha!='\n' and linha!='' and not linha.isspace():
                linha = linha.split('$')
                info.append(linha)
        r,c=0,0
        self.frame=Frame(self.root)
        self.frame.pack()
        self.canvas=Canvas(self.frame)
        frame=Frame(self.canvas)
        myscrollbar=Scrollbar(self.frame,orient="vertical",command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=myscrollbar.set)
        myscrollbar.pack(side="right",fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=frame)
        frame.bind("<Configure>",myfunction)
        label = Label(frame, text='Nome:').grid(row=0, column=0, pady=10, padx=10)
        label = Label(frame, text='Notas:').grid(row=0, column=1, pady=10, padx=10)
        label = Label(frame, text='Faltas:').grid(row=0, column=2, pady=10, padx=10)
        label = Label(frame, text='Total de Aulas:').grid(row=0, column=3, pady=10, padx=10)
        self.eNomes,self.eNotas,self.eFaltas,self.eAulas=[],[],[],[]
        ##Adicionar os Nomes
        for vetor in info:
            r=r+1
            maxRow=r
            globals()['self.nome%s' %vetor[0]] = Entry(frame)
            globals()['self.nome%s' %vetor[0]].insert(END,vetor[0])
            globals()['self.nome%s' %vetor[0]].grid(row=r,column=c, pady=3, padx=10)
            self.eNomes.append(globals()['self.nome%s' %vetor[0]])
        ##
        ###Verifica se há apenas o nome dos alunos
        if len(info[0])==1:
            r,c=0,c+1
            for i in range(0,maxRow):
                r=r+1
                globals()['self.notas%s' %info[i][0]] = Entry(frame)
                globals()['self.notas%s' %info[i][0]].grid(row=r,column=c,pady=3, padx=10)
                self.eNotas.append(globals()['self.notas%s' %info[i][0]])
            r,c=0,c+1
            for i in range(0,maxRow):
                r=r+1
                globals()['self.faltas%s' %info[i][0]] = Entry(frame)
                globals()['self.faltas%s' %info[i][0]].grid(row=r,column=c,pady=3, padx=10)
                self.eFaltas.append(globals()['self.faltas%s' %info[i][0]])
            r,c=0,c+1
            for i in range(0,maxRow):
                r=r+1
                globals()['self.aulas%s' %info[i][0]] = Entry(frame)
                globals()['self.aulas%s' %info[i][0]].grid(row=r,column=c,pady=3, padx=10)
                self.eAulas.append(globals()['self.aulas%s' %info[i][0]])
        ###Escreve notas,faltas e total de aulas dos alunos
        else:
            r,c=0,c+1
            for i in range(0,maxRow):
                r=r+1
                globals()['self.notas%s' %info[i][1]] = Entry(frame)
                globals()['self.notas%s' %info[i][1]].insert(END,info[i][1])
                globals()['self.notas%s' %info[i][1]].grid(row=r,column=c,pady=3, padx=10)
                self.eNotas.append(globals()['self.notas%s' %info[i][1]])
            r,c=0,c+1
            for i in range(0,maxRow):
                r=r+1
                globals()['self.faltas%s' %info[i][2]] = Entry(frame)
                globals()['self.faltas%s' %info[i][2]].insert(END,info[i][2])
                globals()['self.faltas%s' %info[i][2]].grid(row=r,column=c,pady=3, padx=10)
                self.eFaltas.append(globals()['self.faltas%s' %info[i][2]])
            r,c=0,c+1
            for i in range(0,maxRow):
                r=r+1
                globals()['self.aulas%s' %info[i][3]] = Entry(frame)
                globals()['self.aulas%s' %info[i][3]].insert(END,info[i][3])
                globals()['self.aulas%s' %info[i][3]].grid(row=r,column=c,pady=3, padx=10)
                self.eAulas.append(globals()['self.aulas%s' %info[i][3]])
            ###


    def gerar_planilha(self, event=None):
        try:
            i=0
            texto=[self.nome_turma+'\nNome:\t\t\tMédia:\tAusência:\n',self.nome_turma+'\nNome:\t\t\tMédia:\tPresença:\n'][self.presenca.get()]
            for valor in self.eNomes:
                if '\n' in valor.get():
                    nome=valor.get().split('\n')
                    nome=nome[0]
                else:
                    nome=valor.get()
                notas=self.eNotas[i].get()
                if self.calculo_notas.get()=='calcular':
                    notas=notas.replace(',','.')
                    media=eval(notas)
                else:
                    notas=notas.replace(',','.')
                    calc_notas=notas.split('+')
                    total=0
                    for num in calc_notas:
                        total=total+float(num)
                    media=total/len(calc_notas)
                faltas=float(self.eFaltas[i].get())
                if self.definir_aulas.get()==True:
                    aulas=self.eAulas[0].get()
                else:
                    aulas=self.eAulas[i].get()
                aulas=float(aulas)
                if self.presenca.get()==True:
                    pre = (aulas-faltas)*100/aulas
                else:
                    pre = (faltas*100)/aulas
                texto=texto+'%s\t\t%.1f\t%.1f%%\n' %(nome,media,pre)
                i=i+1
            self.nome_turma=self.nome_turma.split('\n')
            self.nome_turma=self.nome_turma[0]
            try:
                os.mkdir(self.nome_turma)
            except:
                pass
            arquivo=open('%s\Planilha %s.txt' %(self.nome_turma,self.nome_turma), 'w')
            arquivo.write(texto)
            arquivo.close()
	    tkMessageBox.showinfo('Arquivo Salvo','Planilha gerada com êxito!')
        except:
            tkMessageBox.showerror('Ocorreu um erro', 'Erro durante a execução!\n'
                                                     'Verifique sua sintaxe e tente novamente')

    def salvar_atual(self, event=None):
        i=0
        texto=self.nome_turma
        for valor in self.eNomes:
            if '\n' in valor.get():
                nome=valor.get().split('\n')
                nome=nome[0]
            else:
                nome=valor.get()
            notas=self.eNotas[i].get()
            faltas=self.eFaltas[i].get()
            if self.definir_aulas.get()==True:
                aulas=self.eAulas[0].get()
            else:
                aulas=self.eAulas[i].get()
            texto=texto+'%s$%s$%s$%s\n' %(nome,notas,faltas,aulas)
            i=i+1
        self.nome_turma=self.nome_turma.split('\n')
        self.nome_turma=self.nome_turma[0]
        try:
            os.mkdir(self.nome_turma)
        except:
            pass
        arquivo=open('%s\%s_dados.txt' %(self.nome_turma,self.nome_turma), 'w')
        arquivo.write(texto)
        arquivo.close()
	tkMessageBox.showinfo('Arquivo Salvo','Dados salvos com êxito!')


if __name__ == '__main__':
    root = Tk()
    Interface(root)
    root.mainloop()