import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

# Função para carregar uma imagem
def carregar_imagem():
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

            # Atualiza o label da imagem
            imagem_label.config(image=imagem_tk)
            imagem_label.image = imagem_tk

            # Exibe informações sobre a imagem
            info_label.config(text=f"Dimensões: {imagem.shape[1]}x{imagem.shape[0]}, "
                                   f"Canais: {imagem.shape[2]}\n"
                                   f"Tipo: {imagem.dtype}")
        else:
            # Se a imagem não puder ser carregada, exibe uma mensagem de erro
            info_label.config(text="Erro ao carregar a imagem. Verifique o caminho do arquivo.")


# Cria a janela principal
janela = tk.Tk()
janela.title("Visualizador de Imagem")

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

# Botão para carregar a imagem
botao_carregar = tk.Button(frame_esquerda, text="Carregar Imagem", command=carregar_imagem)
botao_carregar.pack(pady=10)

# Label para exibir a imagem
imagem_label = tk.Label(frame_direita)
imagem_label.pack(expand=True, fill="both")

# Label para exibir informações da imagem
info_label = tk.Label(frame_direita, text="", anchor="w")
info_label.pack(fill="x")

# Inicia a interface gráfica
janela.mainloop()
