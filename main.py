import cv2
import numpy as np
import csv

NumFoto_beg = 1     # Foto que vai começar a decomposição
NumFoto_end = 208   # Foto que vai terminar +1

for j in range(NumFoto_beg, NumFoto_end):   # Vai rodar para cada imagem
# Obs. Foto do Raspberry Pi é 1920x1080

    Foto = cv2.imread('TCC/Banana_Teste_1/Foto_{}.bmp'.format(j))   # Repositório q está as fotos
    
    # o Python vê a imagem como 1080x1920
    # Normalização usando o fundo RGB
    Foto_Normalizacao = Foto[0:50, 0:50]  # Recorte do fundo
    # Cubo SUPERIOR - menor
    # Foto_Normalizacao_Red = Foto[255:255 + 40, 45:45 + 40]      # Normalização Usando a cor Red
    # Foto_Normalizacao_Green = Foto[320:320 + 40, 115:115 + 40]  # Normalização Usando a cor Green
    # Foto_Normalizacao_Blue = Foto[253:253 + 40, 180:180 + 40]   # Normalização Usando a cor Blue
    # Cubo INFERIOR - maior
    #Foto_Normalizacao_Red = Foto[469:469 + 50, 173:173 + 50]   # Normalização Usando a cor Red
    #Foto_Normalizacao_Green = Foto[473:473 + 50, 57:57 + 50]   # Normalização Usando a cor Green
    #Foto_Normalizacao_Blue = Foto[571:571 + 50, 175:175 + 50]  # Normalização Usando a cor Blue
    # Fundo Gray
    Foto_gray_Normalizacao = cv2.cvtColor(Foto_Normalizacao, cv2.COLOR_BGR2GRAY)  # Utiliza o recorte do fundo e deixa-o em Gray Scale

    #brn, grn, rrn = cv2.split(Foto_Normalizacao_Red)  # todos os pixels no formato B G R Normalizacao Red
    #bgn, ggn, rgn = cv2.split(Foto_Normalizacao_Green)  # todos os pixels no formato B G R Normalizacao Gren
    #bbn, gbn, rbn = cv2.split(Foto_Normalizacao_Blue)  # todos os pixels no formato B G R Normalizacao Blue
    bn, gn, rn = cv2.split(Foto_Normalizacao)  # Todos os pixels no formato B G R  - Normalização RGB
    grayn = cv2.split(Foto_gray_Normalizacao)  # Utilizado para a normalização Gray

    ttl = Foto_Normalizacao.size / 3  # Pegar o Número de pixels
    #ttl40 = Foto_Normalizacao_Red.size / 3  # Pegar o Número de pixels

    GRAYN = float(np.sum(grayn)) / ttl  # Normalização com o fundo
    GRAY_meanN = list()
    GRAY_meanN.append(GRAYN)
    BN = float(np.sum(bn)) / ttl
    GN = float(np.sum(gn)) / ttl
    RN = float(np.sum(rn)) / ttl
    B_meanN = list()
    G_meanN = list()
    R_meanN = list()
    B_meanN.append(BN)
    G_meanN.append(GN)
    R_meanN.append(RN)
    '''
    BBN = float(np.sum(bbn)) / ttl40  # Normalização com a cor
    GGN = float(np.sum(ggn)) / ttl40
    RRN = float(np.sum(rrn)) / ttl40
    BB_meanN = list()
    GG_meanN = list()
    RR_meanN = list()
    BB_meanN.append(BBN)
    GG_meanN.append(GGN)
    RR_meanN.append(RRN)
    if j == NumFoto_beg:
        BASE_RED = RRN  # É um valor de 0 a 255
        BASE_GREEN = GGN
        BASE_BLUE = BBN
        BASE_GRAY = GRAYN
    '''
    for i in range(1, 2):
        '''if i == 0:          # Banana - Filme superior
            Lar = 220
            Alt = 290'''
        if i == 1:        # Banana - Filme inferior
            Lar = 200
            Alt = 480
        '''elif i == 2:        # Banana - Toda em Filme
            Lar = 1300
            Alt = 300
        else:               # Banana - Sem Filme
            Lar = 1700
            Alt = 300'''

        Foto_crop = Foto[Alt:Alt + 50, Lar:Lar + 50]  # o Python vê a imagem como 900x1600
        Foto_gray1 = cv2.cvtColor(Foto_crop, cv2.COLOR_BGR2GRAY)

        b1, g1, r1 = cv2.split(Foto_crop)   # todos os pixels no formato B G R
        B1 = float(np.sum(b1)) / ttl        # Converter para float se não RGB seria tipo int
        G1 = float(np.sum(g1)) / ttl
        R1 = float(np.sum(r1)) / ttl
        B_mean1 = list()
        G_mean1 = list()
        R_mean1 = list()
        B_mean1.append(B1)                  # Tirando a média
        G_mean1.append(G1)                  # Tirando a média
        R_mean1.append(R1)                  # Tirando a média

        gray1 = cv2.split(Foto_gray1)       # todos os pixels em Gray Scale
        GRAY1 = float(np.sum(gray1)) / ttl  # Converter para float
        GRAY_mean1 = list()
        GRAY_mean1.append(GRAY1)            # Tirando a média
        '''
        # Extract channels
        with np.errstate(invalid='ignore', divide='ignore'):
            bgr1 = Foto_crop.astype(float) / 255
            K1 = 1 - np.max(bgr1, axis=2)
            C1 = (1-bgr1[..., 2] - K1)/(1-K1)
            M1 = (1-bgr1[..., 1] - K1)/(1-K1)
            Y1 = (1-bgr1[..., 0] - K1)/(1-K1)
        with np.errstate(invalid='ignore', divide='ignore'):
            bgrN = Foto_Normalizacao.astype(float) / 255
            KN = 1 - np.max(bgrN, axis=2)
            CN = (1 - bgrN[..., 2] - KN) / (1 - KN)
            MN = (1 - bgrN[..., 1] - KN) / (1 - KN)
            YN = (1 - bgrN[..., 0] - KN) / (1 - KN)

        # Convert the input BGR image to CMYK colorspace
        CMYK1 = (np.dstack((C1, M1, Y1, K1)) * 255).astype(np.uint8)
        CMYKN = (np.dstack((CN, MN, YN, KN)) * 255).astype(np.uint8)

        # Split CMYK channels
        c1, m1, y1, k1 = cv2.split(CMYK1)
        C1 = float(np.sum(c1)) / ttl / 255 * 100
        M1 = float(np.sum(m1)) / ttl / 255 * 100
        Y1 = float(np.sum(y1)) / ttl / 255 * 100
        K1 = float(np.sum(k1)) / ttl / 255 * 100
        cN, mN, yN, kN = cv2.split(CMYKN)
        CN = float(np.sum(cN)) / ttl / 255 * 100
        MN = float(np.sum(mN)) / ttl / 255 * 100
        YN = float(np.sum(yN)) / ttl / 255 * 100
        KN = float(np.sum(kN)) / ttl / 255 * 100
        Y_mean1 = list()
        M_mean1 = list()
        C_mean1 = list()
        K_mean1 = list()
        C_mean1.append(C1)
        M_mean1.append(M1)
        Y_mean1.append(Y1)
        K_mean1.append(K1)
        Y_meanN = list()
        M_meanN = list()
        C_meanN = list()
        K_meanN = list()
        C_meanN.append(CN)
        M_meanN.append(MN)
        Y_meanN.append(YN)
        K_meanN.append(KN)
        '''
        '''
        Aux_R = BASE_RED - RRN
        Aux_G = BASE_GREEN - GGN
        Aux_B = BASE_BLUE - BBN
        Aux_Gray = BASE_GRAY - GRAYN
        '''
        cabeca_Gray = ['Gray1', 'GrayN1', 'GrayN1+delta']
        #cabeca_RGB = ['R1', 'G1', 'B1', 'RN1', 'GN1', 'BN1', 'RRN', 'GGN', 'BBN', 'R1+delta', 'B1+delta', 'G1+delta']
        cabeca_RGB = ['R1', 'G1', 'B1', 'RN1', 'GN1', 'BN1']

        # cabeca_CMYK = ['C1', 'M1', 'Y1', 'K1', 'CN1', 'MN1', 'YN1', 'KN1']
        with open('Decomp_Gray_{}.csv'.format(i), 'a+') as arquivo_csv:
            escrever = csv.DictWriter(arquivo_csv, fieldnames=cabeca_Gray, delimiter=';', lineterminator='\n')
            # Escrever o que já existia ou começar a escrever depois do já existente
            # escrever.writerow({'Gray': GRAY, 'Red': R, 'Green': G, 'Blue': B}) Com todas as casas decimais
            escrever.writerow({
                'Gray1': '{0:0.4f}'.format(GRAY1),
                'GrayN1': '{0:0.4f}'.format(GRAYN)})
                #'GrayN1+delta': '{0:0.4f}'.format(GRAY1 + Aux_Gray)})

            arquivo_csv.close()
        
        with open('Decomp_RGB_{}.csv'.format(i), 'a+') as arquivo_csv:
            escrever = csv.DictWriter(arquivo_csv, fieldnames=cabeca_RGB, delimiter=';', lineterminator='\n')
            escrever.writerow({
                'R1': '{0:0.4f}'.format(R1),
                'G1': '{0:0.4f}'.format(G1),
                'B1': '{0:0.4f}'.format(B1),
                'RN1': '{0:0.4f}'.format(RN),
                'GN1': '{0:0.4f}'.format(GN),
                'BN1': '{0:0.4f}'.format(BN)})
                #'RRN': '{0:0.4f}'.format(RRN),
                #'GGN': '{0:0.4f}'.format(GGN),
                #'BBN': '{0:0.4f}'.format(BBN),
                #'R1+delta': '{0:0.4f}'.format(R1+Aux_R),
                #'G1+delta': '{0:0.4f}'.format(G1+Aux_G),
                #'B1+delta': '{0:0.4f}'.format(B1+Aux_B)})
        arquivo_csv.close()
        '''
        with open('Decomp_CMYK_{}.csv'.format(i), 'a+') as arquivo_csv:
            escrever = csv.DictWriter(arquivo_csv, fieldnames=cabeca_CMYK, delimiter=';', lineterminator='\n')
            escrever.writerow({
                'C1': '{0:0.4f}'.format(C1),
                'M1': '{0:0.4f}'.format(M1),
                'Y1': '{0:0.4f}'.format(Y1),
                'K1': '{0:0.4f}'.format(K1),
                'CN1': '{0:0.4f}'.format(CN),
                'MN1': '{0:0.4f}'.format(MN),
                'YN1': '{0:0.4f}'.format(YN),
                'KN1': '{0:0.4f}'.format(KN)})
        arquivo_csv.close()
        '''