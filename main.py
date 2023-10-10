import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import numpy as np
from tkinter import Canvas


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
# Função para atualizar a lista de passos na tela
def atualizar_lista_passos(canny=None):
    if canny is not None:
        lista_passos.delete(0, tk.END)
        print(descricao)
        for i, (descricao, imagem, limiar_canny, canny_maximo) in enumerate(passos, start=1):
            lista_passos.insert(tk.END, f"Passo {i}: {descricao} - Limiares: {limiar_canny}, {canny_maximo}")
    else:
        lista_passos.delete(0, tk.END)
        for i, (descricao, imagem) in enumerate(passos, start=1):
            lista_passos.insert(tk.END, f"Passo {i}: {descricao}")


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
            elif descricao.startswith("Aplicar Filtro de Suavização (Blur)"):
                tamanho_kernel_blur = int(descricao.split()[-1])
                imagem_atual = cv2.blur(imagem_atual, (tamanho_kernel_blur, tamanho_kernel_blur))
            elif descricao.startswith("Detector de Borda (Canny)"):
                tamanho_kernel_canny = int(descricao.split()[-1])
                tamanho_kernel_canny1 = int(descricao.split()[-3])
                print(tamanho_kernel_canny1)
                imagem_atual = cv2.Canny(imagem_atual,tamanho_kernel_canny1 ,tamanho_kernel_canny)

            elif descricao == "Binarização":
                _, imagem_atual = cv2.threshold(imagem_atual, 128, 255, cv2.THRESH_BINARY)
            elif descricao.startswith("Morfologia Matemática (Erosão)"):
                tamanho_kernel_morfologia = int(descricao.split()[-1])
                kernel = np.ones((tamanho_kernel_morfologia, tamanho_kernel_morfologia), np.uint8)
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
            max_height = 700  # Defina a altura máxima desejada
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
            resetar_para_original()
        else:
            # Se a imagem não puder ser carregada, exibe uma mensagem de erro
            info_label.config(text="Erro ao carregar a imagem. Verifique o caminho do arquivo.")
            resetar_para_original()

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

# Função para aplicar binarização
def binarizar():
    global imagem_atual
    if imagem_atual is not None:
        # Aplicar a binarização (por exemplo, usando a função threshold)
        _, imagem_resultante = cv2.threshold(imagem_atual, 128, 255, cv2.THRESH_BINARY)
        adicionar_passo("Binarização", imagem_resultante)
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

# Variável para armazenar o tamanho do kernel de desfoque
tamanho_kernel_blur = 5  # Valor padrão



# Variáveis para armazenar os parâmetros do Detector de Borda
limiar_canny = 100
canny_maximo = 200

# Variável para armazenar o tamanho do kernel da Morfologia Matemática
tamanho_kernel_morfologia = 5  # Valor padrão

# Função para aplicar filtro de desfoque
def aplicar_blur():
    global imagem_atual
    global tamanho_kernel_blur
    if imagem_atual is not None:
        try:
            tamanho_kernel = (int(tamanho_kernel_blur), int(tamanho_kernel_blur))
        except ValueError:
            tamanho_kernel = (5, 5)  # Valor padrão

        # Aplicar o filtro de desfoque com o tamanho do kernel especificado
        imagem_resultante = cv2.blur(imagem_atual, tamanho_kernel)
        adicionar_passo(f"Aplicar Filtro de Suavização (Blur) - Kernel {tamanho_kernel_blur}", imagem_resultante)
        exibir_imagem(imagem_resultante)



# Função para aplicar detector de borda
def detector_de_borda():
    global imagem_atual
    global limiar_canny
    global canny_maximo
    if imagem_atual is not None:
        try:
            limiar_canny = int(limiar_canny)
            canny_maximo = int(canny_maximo)

            # Aplicar o filtro de detecção de bordas de Canny com os limiares especificados
            imagem_resultante = cv2.Canny(imagem_atual, limiar_canny, canny_maximo)
            exibir_imagem(imagem_resultante)
            adicionar_passo(f"Detector de Borda (Canny) - Limiares: {limiar_canny} , {canny_maximo}", imagem_resultante)
            
        except ValueError:
            pass  # Lidere com exceções de conversão de tipo aqui, se necessário

    

# Função para aplicar morfologia matemática
def morfologia_matematica():
    global imagem_atual
    if imagem_atual is not None:
        try:
            tamanho_kernel = (int(tamanho_kernel_morfologia), int(tamanho_kernel_morfologia))
        except ValueError:
            tamanho_kernel = (5, 5)  # Valor padrão

        # Aplicar operações de morfologia matemática (por exemplo, erosão ou dilatação)
        kernel = np.ones((tamanho_kernel), np.uint8)  # Ajuste o kernel conforme necessário
        imagem_resultante = cv2.erode(imagem_atual, kernel, iterations=1)
        adicionar_passo(f"Morfologia Matemática (Erosão) - Kernel {tamanho_kernel_morfologia}", imagem_resultante)
        exibir_imagem(imagem_resultante)

# Função para atualizar o tamanho do kernel de desfoque com base na posição da trackbar
def atualizar_tamanho_kernel(valor):
    global tamanho_kernel_blur
    tamanho_kernel_blur = valor


# Função para atualizar o tamanho do kernel de desfoque com base na posição da trackbar
def atualizar_tamanho_kernel_limiar_canny(valor):
    global limiar_canny
    limiar_canny = valor



# Função para atualizar o tamanho do kernel de desfoque com base na posição da trackbar
def atualizar_tamanho_kernel_limiar_canny_maximo(valor):
    global canny_maximo
    canny_maximo = valor



def atualizar_tamanho_kernel_morfologia(valor):
    global tamanho_kernel_morfologia
    tamanho_kernel_morfologia = int(valor)


# Botão para carregar a imagem
botao_carregar = tk.Button(frame_esquerda, text="Carregar Imagem", command=carregar_imagem)
botao_carregar.pack(pady=10)

# Label para exibir a imagem
imagem_label = tk.Label(frame_direita)
imagem_label.pack(expand=True, fill="both")

# Label para exibir informações da imagem
info_label = tk.Label(frame_direita, text="", anchor="w")
info_label.pack(fill="x")

# Criação do Canvas com uma linha
linha_separator = Canvas(frame_esquerda, height=2, background="gray")
linha_separator.pack(fill="x", padx=10, pady=5)  # Adicione preenchimento horizontal e vertical

# Adicionar botões para as operações
botao_converter_cor = tk.Button(frame_esquerda, text="Converter Cor para tons de cinza", command=converter_cor)
botao_converter_cor.pack(pady=10)
# Criação do Canvas com uma linha
linha_separator = Canvas(frame_esquerda, height=2, background="gray")
linha_separator.pack(fill="x", padx=10, pady=5)  # Adicione preenchimento horizontal e vertical

botao_binarizar = tk.Button(frame_esquerda, text="Binarizar a imagem", command=binarizar)
botao_binarizar.pack()


# Criação do Canvas com uma linha
linha_separator = Canvas(frame_esquerda, height=2, background="gray")
linha_separator.pack(fill="x", padx=10, pady=5)  # Adicione preenchimento horizontal e vertical


# Cria a trackbar (barra de rolagem) para ajustar o tamanho do kernel BLUR
trackbar_tamanho_kernel = tk.Scale(frame_esquerda, from_=1, to=15, orient="horizontal", label="blur",
                                    command=atualizar_tamanho_kernel)
trackbar_tamanho_kernel.set(tamanho_kernel_blur)
trackbar_tamanho_kernel.pack()

# Botão para aplicar o filtro de desfoque com o tamanho do kernel especificado
botao_aplicar_blur = tk.Button(frame_esquerda, text="Aplicar Blur", command=aplicar_blur)
botao_aplicar_blur.pack()


# Criação do Canvas com uma linha
linha_separator = Canvas(frame_esquerda, height=2, background="gray")
linha_separator.pack(fill="x", padx=10, pady=5)  # Adicione preenchimento horizontal e vertical


# Cria a trackbar (barra de rolagem) para ajustar o tamanho do kernel limiar_canny
trackbar_tamanho_kernel = tk.Scale(frame_esquerda, from_=1, to=255, orient="horizontal", label="limiar_canny",
                                    command=atualizar_tamanho_kernel_limiar_canny)
trackbar_tamanho_kernel.set(limiar_canny)
trackbar_tamanho_kernel.pack()


# Cria a trackbar (barra de rolagem) para ajustar o tamanho do kernel canny_maximo
trackbar_tamanho_kernel = tk.Scale(frame_esquerda, from_=1, to=255, orient="horizontal", label="canny_maximo",
                                    command=atualizar_tamanho_kernel_limiar_canny_maximo)
trackbar_tamanho_kernel.set(canny_maximo)
trackbar_tamanho_kernel.pack()



botao_detector_borda = tk.Button(frame_esquerda, text="Aplicar Detector de Borda", command=detector_de_borda)
botao_detector_borda.pack()


 # Criação do Canvas com uma linha
linha_separator = Canvas(frame_esquerda, height=2, background="gray")
linha_separator.pack(fill="x", padx=10, pady=5)  # Adicione preenchimento horizontal e vertical

# Cria a trackbar (barra de rolagem) para ajustar o tamanho do kernel tamanho_kernel_morfologia
trackbar_tamanho_kernel = tk.Scale(frame_esquerda, from_=1, to=25, orient="horizontal", label="morfologia",
                                    command=atualizar_tamanho_kernel_morfologia)
trackbar_tamanho_kernel.set(tamanho_kernel_morfologia)
trackbar_tamanho_kernel.pack()


botao_morfologia = tk.Button(frame_esquerda, text="Aplicar Morfologia Matemática", command=morfologia_matematica)
botao_morfologia.pack()
# Criação do Canvas com uma linha
linha_separator = Canvas(frame_esquerda, height=2, background="gray")
linha_separator.pack(fill="x", padx=10, pady=5)  # Adicione preenchimento horizontal e vertical


# Botão para remover um passo da lista
botao_remover_passo = tk.Button(frame_esquerda, text="Remover Passo", command=remover_passo)
botao_remover_passo.pack(pady=10)

# Lista de passos na interface gráfica
lista_passos = tk.Listbox(frame_esquerda, selectmode=tk.SINGLE, height=20)  # Aumente o valor de 'height' conforme desejado
lista_passos.pack(fill="both", expand=True)


# Botão para salvar a imagem
botao_salvar_imagem = tk.Button(frame_esquerda, text="Salvar Imagem", command=salvar_imagem)
botao_salvar_imagem.pack(pady=10)

# Botão para salvar a lista de passos em um arquivo de texto
botao_salvar_passos = tk.Button(frame_esquerda, text="Salvar Passos", command=salvar_passos)
botao_salvar_passos.pack(pady=10)

# Inicia a interface gráfica
janela.mainloop()
