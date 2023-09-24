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

def carregar_imagem():
    global imagens
    global imagem_atual
    global imagem_label
    global info_label

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

            # Adiciona a imagem à lista de imagens
            imagens.append(imagem)

            # Exibe a primeira imagem na lista
            imagem_atual = imagens[0]
            exibir_imagem(imagem_atual)

            # Exibe informações sobre a imagem
            info_label.config(text=f"Dimensões: {imagem.shape[1]}x{imagem.shape[0]}, "
                                   f"Canais: {imagem.shape[2]}\n"
                                   f"Tipo: {imagem.dtype}")
        else:
            # Se a imagem não puder ser carregada, exibe uma mensagem de erro
            info_label.config(text="Erro ao carregar a imagem. Verifique o caminho do arquivo.")

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
        imagem_atual = cv2.cvtColor(imagem_atual, cv2.COLOR_RGB2GRAY)
        exibir_imagem(imagem_atual)

# Função para aplicar filtro
def aplicar_filtro():
    global imagem_atual
    if imagem_atual is not None:
        # Aplicar o filtro desejado
        # Por exemplo, um filtro de suavização (blur)
        imagem_atual = cv2.blur(imagem_atual, (5, 5))  # Ajuste o tamanho do kernel conforme necessário
        exibir_imagem(imagem_atual)

# Função para aplicar detector de borda
def detector_de_borda():
    global imagem_atual
    if imagem_atual is not None:
        # Aplicar o detector de borda (por exemplo, usando o operador Canny)
        imagem_atual = cv2.Canny(imagem_atual, 100, 200)  # Ajuste os limiares conforme necessário
        exibir_imagem(imagem_atual)

# Função para aplicar binarização
def binarizar():
    global imagem_atual
    if imagem_atual is not None:
        # Aplicar a binarização (por exemplo, usando a função threshold)
        _, imagem_atual = cv2.threshold(imagem_atual, 128, 255, cv2.THRESH_BINARY)
        exibir_imagem(imagem_atual)

# Função para aplicar morfologia matemática
def morfologia_matematica():
    global imagem_atual
    if imagem_atual is not None:
        # Aplicar operações de morfologia matemática (por exemplo, erosão ou dilatação)
        kernel = np.ones((5, 5), np.uint8)  # Ajuste o kernel conforme necessário
        imagem_atual = cv2.erode(imagem_atual, kernel, iterations=1)
        exibir_imagem(imagem_atual)

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

# Inicia a interface gráfica
janela.mainloop()
