import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import numpy as np

# Cria a janela principal
janela = tk.Tk()
janela.title("Ferramenta de Processamento de Imagem")

# Lista para armazenar as imagens
imagens = []

# Variável para rastrear a imagem atual
imagem_atual = None

# Variável para armazenar a imagem original
imagem_original = None

# Cria os frames para as colunas
frame_esquerda = tk.Frame(janela, width=300)
frame_direita = tk.Frame(janela)

# Define o tamanho relativo das colunas
frame_esquerda.grid(column=0, row=0, rowspan=2, sticky="nsew")
frame_direita.grid(column=1, row=0, sticky="nsew")

janela.grid_columnconfigure(0, weight=3)
janela.grid_columnconfigure(1, weight=7)
janela.grid_rowconfigure(0, weight=1)
janela.grid_rowconfigure(1, weight=1)

# Lista para armazenar os passos realizados
passos = []

# Função para atualizar a lista de passos na tela
def atualizar_lista_passos():
    lista_passos.delete(0, tk.END)
    for i, (descricao, imagem) in enumerate(passos, start=1):
        lista_passos.insert(tk.END, f"Passo {i}: {descricao}")

# Função para adicionar um passo à lista
def adicionar_passo(descricao, imagem):
    passos.append((descricao, imagem))
    atualizar_lista_passos()

# Função para remover um passo da lista
def remover_passo():
    global passos
    global imagem_atual

    selecionado = lista_passos.curselection()
    if selecionado:
        index = selecionado[0]

        # Verifica se há passos seguintes ao passo removido
        if index < len(passos) - 1:
            passos = passos[:index] + passos[index+1:]
        else:
            passos = passos[:index]

        # Restaura a imagem original
        imagem_atual = imagem_original.copy()

        # Reaplica todos os passos na lista
        for descricao, imagem_passo in passos:
            if descricao == "Carregar Imagem":
                imagem_atual = imagem_passo
            elif descricao == "Converter Cor para Escala de Cinza":
                imagem_atual = cv2.cvtColor(imagem_atual, cv2.COLOR_RGB2GRAY)
            elif descricao == "Aplicar Filtro de Suavização (Blur)":
                imagem_atual = cv2.blur(imagem_atual, (5, 5))
            elif descricao == "Detector de Borda (Canny)":
                imagem_atual = cv2.Canny(imagem_atual, 100, 200)
            elif descricao == "Binarização":
                _, imagem_atual = cv2.threshold(imagem_atual, 128, 255, cv2.THRESH_BINARY)
            elif descricao == "Morfologia Matemática (Erosão)":
                kernel = np.ones((5, 5), np.uint8)
                imagem_atual = cv2.erode(imagem_atual, kernel, iterations=1)

        # Atualiza a lista de passos e exibe a imagem atualizada
        atualizar_lista_passos()
        exibir_imagem(imagem_atual)



# Função para carregar uma imagem
def carregar_imagem():
    global imagens
    global imagem_atual
    global imagem_label
    global info_label
    global imagem_original

    # Abre a caixa de diálogo para selecionar a imagem
    file_path = filedialog.askopenfilename()

    # Verifica se um arquivo foi selecionado
    if file_path:
        # Carrega a imagem usando o OpenCV
        imagem = cv2.imread(file_path)

        # Verifica se a imagem foi carregada com sucesso
        if imagem is not None:
            # Converte a imagem para o formato RGB
            imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)

            # Redimensiona a imagem para manter o mesmo tamanho na janela
            max_height = 400  # Defina a altura máxima desejada
            ratio = max_height / imagem.shape[0]
            new_width = int(imagem.shape[1] * ratio)
            imagem = cv2.resize(imagem, (new_width, max_height))

            # Converte a imagem para um formato compatível com o Tkinter
            imagem_pil = Image.fromarray(imagem)
            imagem_tk = ImageTk.PhotoImage(imagem_pil)

            # Salva a imagem original
            imagem_original = imagem

            # Adiciona a imagem à lista de imagens
            imagens.append(imagem)

            # Exibe a primeira imagem na lista
            imagem_atual = imagens[0]
            exibir_imagem(imagem_atual)

            # Exibe informações sobre a imagem
            info_label.config(text=f"Dimensões: {imagem.shape[1]}x{imagem.shape[0]}, "
                                   f"Canais: {imagem.shape[2]}\n"
                                   f"Tipo: {imagem.dtype}")
            adicionar_passo("Carregar Imagem", imagem_atual)
        else:
            # Se a imagem não puder ser carregada, exibe uma mensagem de erro
            info_label.config(text="Erro ao carregar a imagem. Verifique o caminho do arquivo.")

# Função para reverter para a imagem original e limpar a lista de passos
def resetar_para_original():
    global imagem_atual
    global imagem_original
    global passos
    if passos:
        imagem_atual = passos[-1][1]
    else:
        imagem_atual = imagem_original.copy()
    passos = []
    atualizar_lista_passos()
    exibir_imagem(imagem_atual)

# Função para exibir uma imagem
def exibir_imagem(imagem):
    global imagem_label
    global imagem_atual

    # Converte a imagem para o formato compatível com o Tkinter
    imagem_pil = Image.fromarray(imagem)
    imagem_tk = ImageTk.PhotoImage(imagem_pil)

    # Atualiza o label da imagem
    imagem_label.config(image=imagem_tk)
    imagem_label.image = imagem_tk

    # Atualiza a imagem atual
    imagem_atual = imagem

# Função para aplicar conversão de cor
def converter_cor():
    global imagem_atual
    if imagem_atual is not None:
        # Aplicar a conversão de cor (por exemplo, de RGB para escala de cinza)
        imagem_resultante = cv2.cvtColor(imagem_atual, cv2.COLOR_RGB2GRAY)
        adicionar_passo("Converter Cor para Escala de Cinza", imagem_resultante)
        exibir_imagem(imagem_resultante)

# Função para aplicar filtro
def aplicar_filtro():
    global imagem_atual
    if imagem_atual is not None:
        # Aplicar o filtro desejado
        # Por exemplo, um filtro de suavização (blur)
        imagem_resultante = cv2.blur(imagem_atual, (5, 5))  # Ajuste o tamanho do kernel conforme necessário
        adicionar_passo("Aplicar Filtro de Suavização (Blur)", imagem_resultante)
        exibir_imagem(imagem_resultante)

# Função para aplicar detector de borda
def detector_de_borda():
    global imagem_atual
    if imagem_atual is not None:
        # Aplicar o detector de borda (por exemplo, usando o operador Canny)
        imagem_resultante = cv2.Canny(imagem_atual, 100, 200)  # Ajuste os limiares conforme necessário
        adicionar_passo("Detector de Borda (Canny)", imagem_resultante)
        exibir_imagem(imagem_resultante)

# Função para aplicar binarização
def binarizar():
    global imagem_atual
    if imagem_atual is not None:
        # Aplicar a binarização (por exemplo, usando a função threshold)
        _, imagem_resultante = cv2.threshold(imagem_atual, 128, 255, cv2.THRESH_BINARY)
        adicionar_passo("Binarização", imagem_resultante)
        exibir_imagem(imagem_resultante)

# Função para aplicar morfologia matemática
def morfologia_matematica():
    global imagem_atual
    if imagem_atual is not None:
        # Aplicar operações de morfologia matemática (por exemplo, erosão ou dilatação)
        kernel = np.ones((5, 5), np.uint8)  # Ajuste o kernel conforme necessário
        imagem_resultante = cv2.erode(imagem_atual, kernel, iterations=1)
        adicionar_passo("Morfologia Matemática (Erosão)", imagem_resultante)
        exibir_imagem(imagem_resultante)

# Função para salvar a imagem exibida
def salvar_imagem():
    global imagem_atual
    if imagem_atual is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Arquivos PNG", "*.png")])
        if file_path:
            # Salva a imagem atual em formato PNG
            cv2.imwrite(file_path, cv2.cvtColor(imagem_atual, cv2.COLOR_RGB2BGR))

# Função para salvar a lista de passos em um arquivo de texto
def salvar_passos():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt")])
    if file_path:
        with open(file_path, 'w') as arquivo:
            for descricao, _ in passos:
                arquivo.write(descricao + "\n")


# Botão para carregar a imagem
botao_carregar = tk.Button(frame_esquerda, text="Carregar Imagem", command=carregar_imagem)
botao_carregar.pack(pady=10)

# Label para exibir a imagem
imagem_label = tk.Label(frame_direita)
imagem_label.pack(expand=True, fill="both")

# Label para exibir informações da imagem
info_label = tk.Label(frame_direita, text="", anchor="w")
info_label.pack(fill="x")

# Adicionar botões para as operações
botao_converter_cor = tk.Button(frame_esquerda, text="Converter Cor", command=converter_cor)
botao_converter_cor.pack(pady=10)

botao_aplicar_filtro = tk.Button(frame_esquerda, text="Aplicar Filtro", command=aplicar_filtro)
botao_aplicar_filtro.pack()

botao_detector_borda = tk.Button(frame_esquerda, text="Detector de Borda", command=detector_de_borda)
botao_detector_borda.pack()

botao_binarizar = tk.Button(frame_esquerda, text="Binarizar", command=binarizar)
botao_binarizar.pack()

botao_morfologia = tk.Button(frame_esquerda, text="Morfologia Matemática", command=morfologia_matematica)
botao_morfologia.pack()

# Botão para remover um passo da lista
botao_remover_passo = tk.Button(frame_esquerda, text="Remover Passo", command=remover_passo)
botao_remover_passo.pack(pady=10)

# Lista de passos na interface gráfica
lista_passos = tk.Listbox(frame_esquerda, selectmode=tk.SINGLE, height=25)  # Aumente o valor de 'height' conforme desejado
lista_passos.pack(fill="both", expand=True)


# Botão para salvar a imagem
botao_salvar_imagem = tk.Button(frame_esquerda, text="Salvar Imagem", command=salvar_imagem)
botao_salvar_imagem.pack(pady=10)

# Botão para salvar a lista de passos em um arquivo de texto
botao_salvar_passos = tk.Button(frame_esquerda, text="Salvar Passos", command=salvar_passos)
botao_salvar_passos.pack(pady=10)

# Inicia a interface gráfica
janela.mainloop()
