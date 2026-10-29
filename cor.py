import cv2
import numpy as np

# Função vazia exigida pelo createTrackbar
def nothing(x):
    pass

# 1. Carregar a imagem (ou use 0 para a webcam: cv2.VideoCapture(0))
img = cv2.imread('./frames/16.jpg')
if img is None:
    print("Erro: Imagem não encontrada. Verifique o caminho.")
    exit()

# Redimensionar se a imagem for muito grande para caber na tela
img = cv2.resize(img, (640, 480))

# 2. Criar a janela de controle
cv2.namedWindow('Ajuste HSV')

# 3. Criar os Trackbars para Hue, Saturation e Value (Mínimo e Máximo)
# Nota: No OpenCV o Hue vai de 0 a 179, Saturation e Value de 0 a 255
cv2.createTrackbar('H Min', 'Ajuste HSV', 0, 179, nothing)
cv2.createTrackbar('H Max', 'Ajuste HSV', 179, 179, nothing)
cv2.createTrackbar('S Min', 'Ajuste HSV', 0, 255, nothing)
cv2.createTrackbar('S Max', 'Ajuste HSV', 255, 255, nothing)
cv2.createTrackbar('V Min', 'Ajuste HSV', 0, 255, nothing)
cv2.createTrackbar('V Max', 'Ajuste HSV', 255, 255, nothing)

# Definir um valor inicial padrão para o H Max não começar em 0 (opcional)
cv2.setTrackbarPos('H Min', 'Ajuste HSV', 0)
cv2.setTrackbarPos('S Min', 'Ajuste HSV', 76)
cv2.setTrackbarPos('V Min', 'Ajuste HSV', 0)
cv2.setTrackbarPos('H Max', 'Ajuste HSV', 91)
cv2.setTrackbarPos('S Max', 'Ajuste HSV', 255)
cv2.setTrackbarPos('V Max', 'Ajuste HSV', 255)

while True:
    # Converter frame atual para HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Pegar as posições atuais das barras deslizantes
    h_min = cv2.getTrackbarPos('H Min', 'Ajuste HSV')
    h_max = cv2.getTrackbarPos('H Max', 'Ajuste HSV')
    s_min = cv2.getTrackbarPos('S Min', 'Ajuste HSV')
    s_max = cv2.getTrackbarPos('S Max', 'Ajuste HSV')
    v_min = cv2.getTrackbarPos('V Min', 'Ajuste HSV')
    v_max = cv2.getTrackbarPos('V Max', 'Ajuste HSV')

    # Montar os arrays lower e upper com os valores das barras
    lower_limit = np.array([h_min, s_min, v_min])
    upper_limit = np.array([h_max, s_max, v_max])

    # Gerar a máscara binária
    mask = cv2.inRange(hsv, lower_limit, upper_limit)
    
    # Aplicar a máscara na imagem original para ver o resultado recortado
    result = cv2.bitwise_and(img, img, mask=mask)

    # Mostrar as janelas
    cv2.imshow('Original', img)
    cv2.imshow('Ajuste HSV (Mascara)', mask)
    cv2.imshow('Resultado Final', result)

    # Pressione 's' para salvar/imprimir os valores atuais no terminal e sair
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        print("\n--- VALORES ENCONTRADOS ---")
        print(f"lower = np.array([{h_min}, {s_min}, {v_min}])")
        print(f"upper = np.array([{h_max}, {s_max}, {v_max}])")
        break
    elif key == ord('q'): # Pressione 'q' para sair sem salvar
        break

cv2.destroyAllWindows()