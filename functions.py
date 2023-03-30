import numpy as np
from math import floor
from constants import caracMotor
import matplotlib.pyplot as plt

def dadosDeVendas(hmotor, norma):
    unidade = ""
    if norma == "IEC":
        unidade = "mm"
    else:
        unidade = "pol"
    print(f"Qual cota A do cliente? [{unidade}]")
    cotA = float(input())
    print(f"Qual cota B do cliente? [{unidade}]")
    cotB = float(input())
    print(f"Qual cota C do cliente? [{unidade}]")
    cotC = float(input())
    while True:
        print(f"Qual cota H do cliente? [{unidade}]")
        cotH = float(input())
        if norma == "NEMA":
            cotH = cotH *25.4
        if cotH - hmotor > 91: ###63.5
            print("Cota inválida para essa aplicação, digite uma cota que a diferença para o motor seja menos de 63.5mm [2.5pol]")
        else:
            break
    print(f"Deseja informar a cota K do cliente? [{unidade}]")
    print("1 - Sim\n2 - Não")
    choiceK = int(input())
    cotK = 0
    if choiceK == 1:
        print(f"Qual a cota K do cliente? [{unidade}]")        
        cotK = float(input())
    print("Qual nome para o arquivo 3D? [.step]")
    nomeArquivo = input()
    if norma == "NEMA":
        return {"A": cotA * 25.4, "B": cotB * 25.4, "C": cotC * 25.4, "H": cotH, "NOME": nomeArquivo, "K": cotK * 25.4}
    return {"A": cotA, "B": cotB, "C": cotC, "H": cotH, "NOME": nomeArquivo, "K": cotK}




def escolherLinhaDoMotor():
    print("Qual linha de motor? Digite o número")
    print("1 - W50\n2 - W51 HD\n3 - HGF")
    chosenNumber = input()
    keyChosen = ""
    if chosenNumber == "1":
        keyChosen = "W50"
    elif chosenNumber == "2":
        keyChosen = "W51 HD"
    else:
        keyChosen = "HGF"
    return keyChosen

def frameEscolhido(geometriaDosMotoresList, geometriaDosMotoresMap, keyChosen):
    print("Qual carcaça? Digite o número")
    for i, frame in enumerate(geometriaDosMotoresMap[keyChosen]):
        print(f'{i} - {frame}')
    chosenNumber = int(input())
    finalRow = []
    finalRowNumber = 0
    for i, w in enumerate(geometriaDosMotoresList):
        if geometriaDosMotoresList[i][1] == geometriaDosMotoresMap[keyChosen][chosenNumber]:
            finalRowNumber = i
            finalRow = finalRow + w
    for i, w in enumerate(finalRow):
        if i >1 and i<=18:
            finalRow[i] = float(finalRow[i])
    return finalRow, finalRowNumber

def gerarFuros(furosDoMotor, furosDaBase, dadosDoMotorEscolhido, limitesBaseMotor):
    furosComRebaixo = [0, 0, 0, 0]
    angle = np.linspace(np.pi/2, 2.5 * np.pi , 150 )
    radius = dadosDoMotorEscolhido[caracMotor["K"]]/2
    x = radius * np.cos( angle ) 
    y = radius * np.sin( angle )
    for furo in furosDoMotor:
        plt.plot(x + furo[0], y + furo[1], "b")

    halfX = floor(float(len(x)/2))
    if dadosDoMotorEscolhido[caracMotor["Carcaça"]] != "355 J/H" and dadosDoMotorEscolhido[caracMotor["Carcaça"]] != "355H/G":
        zLinha = dadosDoMotorEscolhido[caracMotor["K'"]]
        z = dadosDoMotorEscolhido[caracMotor["K"]]
        if z == 28:
            rebaixoZ = 52
            rebaixoZlinha = zLinha - z + rebaixoZ
        else:
            rebaixoZ = 60
            rebaixoZlinha = zLinha - z + rebaixoZ
    else:
        zLinha = 56
        z = 36
        radius = z/2
        rebaixoZ = 60
        rebaixoZlinha = zLinha - z + rebaixoZ
        x = radius * np.cos( angle ) 
        y = radius * np.sin( angle )
        halfX = floor(float(len(x)/2))
    for i, furo in enumerate(furosDaBase):
        limNL = [furo[0] + (zLinha - z)/2, furo[1] + z/2]
        limSL = [furo[0] + (zLinha - z)/2, furo[1] - z/2]
        limNO = [furo[0] - (zLinha - z)/2, furo[1] + z/2]
        limSO = [furo[0] - (zLinha - z)/2, furo[1] - z/2]
        circleLeft = [x[0:halfX], y[0:halfX]]
        circleRight = [x[halfX:], y[halfX:]]
        plt.plot([limNO[0], limNL[0]],[limNO[1], limNL[1]], "r")
        plt.plot([limSO[0], limSL[0]],[limSO[1], limSL[1]], "r")
        plt.plot(circleLeft[0] + limNO[0],circleLeft[1] + furo[1], "r")
        plt.plot(circleRight[0] + limNL[0],circleRight[1] + furo[1], "r")
        limL = furo[0] + zLinha/2
        limO = furo[0] - zLinha/2
        limN = furo[1] + z/2
        limS = furo[1] - z/2
        limSL = [0,0]
        if limL > limitesBaseMotor[i][2] and limN > limitesBaseMotor[i][3] and limO < limitesBaseMotor[i][0] and limS < limitesBaseMotor[i][1]:
            furosComRebaixo[i] = 1
            radius2 = rebaixoZ/2
            x2 = radius2 * np.cos( angle ) 
            y2 = radius2 * np.sin( angle )
            halfX2 = floor(float(len(x)/2))
            limNL2 = [furo[0] + (rebaixoZlinha - rebaixoZ)/2, furo[1] + rebaixoZ/2]
            limSL2 = [furo[0] + (rebaixoZlinha - rebaixoZ)/2, furo[1] - rebaixoZ/2]
            limNO2 = [furo[0] - (rebaixoZlinha - rebaixoZ)/2, furo[1] + rebaixoZ/2]
            limSO2 = [furo[0] - (rebaixoZlinha - rebaixoZ)/2, furo[1] - rebaixoZ/2]
            circleLeft2 = [x2[0:halfX2], y2[0:halfX2]]
            circleRight2 = [x2[halfX2:], y2[halfX2:]]
            plt.plot([limNO2[0], limNL2[0]],[limNO2[1], limNL2[1]], "k")
            plt.plot([limSO2[0], limSL2[0]],[limSO2[1], limSL2[1]], "k")
            plt.plot(circleLeft2[0] + limNO2[0],circleLeft2[1] + furo[1], "k")
            plt.plot(circleRight2[0] + limNL2[0],circleRight2[1] + furo[1], "k")
    return furosComRebaixo, limSL2

def gerarChapasMetalicasBase(furoBaseCritico, baseMotorCritico, dadosDoMotorEscolhido, furosComRebaixo):
    chapasMetalicasBase = []
    for i, furo in enumerate(furoBaseCritico):
        pontosCriticos = []
        if furosComRebaixo.count(1) == 0:
            criticoLesteBase = furo[0] + dadosDoMotorEscolhido[caracMotor["K"]]/2
            criticoNorteBase = furo[1] + dadosDoMotorEscolhido[caracMotor["K"]]/2
            criticoSulBase = furo[1] - dadosDoMotorEscolhido[caracMotor["K"]]/2
            criticoOesteBase = furo[0] - dadosDoMotorEscolhido[caracMotor["K"]]/2
        else:
            z = dadosDoMotorEscolhido[caracMotor["K"]]
            zLinha = dadosDoMotorEscolhido[caracMotor["K'"]]
            if dadosDoMotorEscolhido[caracMotor["Carcaça"]] != "355 J/H" and dadosDoMotorEscolhido[caracMotor["Carcaça"]] != "355H/G":
                if z == 28:
                    rebaixoZ = 52
                    rebaixoZlinha = zLinha - z + rebaixoZ
                else:
                    rebaixoZ = 60
                    rebaixoZlinha = zLinha - z + rebaixoZ
            else:
                    rebaixoZ = 60
                    rebaixoZlinha = zLinha - z + rebaixoZ
            criticoLesteBase = furo[0] + rebaixoZlinha/2
            criticoNorteBase = furo[1] + rebaixoZ/2
            criticoSulBase = furo[1] - rebaixoZ/2
            criticoOesteBase = furo[0] - rebaixoZlinha/2
        criticosFuro = [criticoLesteBase, criticoNorteBase, criticoOesteBase, criticoSulBase]
        criticosBase = [baseMotorCritico[i][0][0], baseMotorCritico[i][0][1], baseMotorCritico[i][1][0], baseMotorCritico[i][1][1]]
        for i in range(0, len(criticosFuro)):
            if i < 2:
                if criticosFuro[i] > criticosBase[i]:
                    pontosCriticos = pontosCriticos + [criticosFuro[i]+10]
                else:
                    pontosCriticos = pontosCriticos + [criticosBase[i]+10] 
            else:
                if criticosFuro[i] < criticosBase[i]:
                    pontosCriticos = pontosCriticos + [criticosFuro[i] - 10]
                else:
                    pontosCriticos = pontosCriticos + [criticosBase[i] - 10] 
        plt.plot([pontosCriticos[0], pontosCriticos[2]],[pontosCriticos[1],pontosCriticos[1]],'g')
        plt.plot([pontosCriticos[2], pontosCriticos[2]],[pontosCriticos[1],pontosCriticos[3]],'g')
        plt.plot([pontosCriticos[2], pontosCriticos[0]],[pontosCriticos[3],pontosCriticos[3]],'g')
        plt.plot([pontosCriticos[0], pontosCriticos[0]],[pontosCriticos[3],pontosCriticos[1]],'g')
        chapasMetalicasBase = chapasMetalicasBase + [pontosCriticos]
    return chapasMetalicasBase

def gerarFurosSemFuroLongo(furosDoMotor, furosDaBase, dadosDoMotorEscolhido, limitesBaseMotor, cotasDoCliente):
    furosComRebaixo = [0, 0, 0, 0]
    angle = np.linspace(np.pi/2, 2.5 * np.pi , 150 )
    radius = dadosDoMotorEscolhido[caracMotor["K"]]/2
    x = radius * np.cos( angle ) 
    y = radius * np.sin( angle )
    for furo in furosDoMotor:
        plt.plot(x + furo[0], y + furo[1], "b")

    if cotasDoCliente["K"] == 0:
        if dadosDoMotorEscolhido[caracMotor["Carcaça"]] != "355 J/H" and dadosDoMotorEscolhido[caracMotor["Carcaça"]] != "355H/G":
            z = dadosDoMotorEscolhido[caracMotor["K"]]
            radius = z/2
            if z == 28:
                rebaixoZ = 52
                rebaixoHbase = 24
            else:
                rebaixoZ = 60
                rebaixoHbase = 32
        else:
            z = 36
            radius = z/2
            rebaixoZ = 60
            rebaixoHbase = 32
    else:
        z = cotasDoCliente["K"]
        radius = z/2
        rebaixoZ = z * 2
        rebaixoHbase = z
    dadosParaDesenho3DcotaKBase = z
    dadosParaDesenho3DcotaKMaxBase = rebaixoZ
    dadosParaDesenho3DrebaixoHBase = rebaixoHbase
    dadosParaDesenhoCotas = [dadosParaDesenho3DcotaKBase, dadosParaDesenho3DcotaKMaxBase, dadosParaDesenho3DrebaixoHBase]
    x2 = radius * np.cos( angle ) 
    y2 = radius * np.sin( angle )
    for i, furo in enumerate(furosDaBase):
        plt.plot(x2 + furo[0], y2 + furo[1], "r")
        limL = furo[0] + z/2
        limO = furo[0] - z/2
        limN = furo[1] + z/2
        limS = furo[1] - z/2
        if limL > limitesBaseMotor[i][2] and limN > limitesBaseMotor[i][3] and limO < limitesBaseMotor[i][0] and limS < limitesBaseMotor[i][1]:
            furosComRebaixo[i] = 1
            radiusRebaixo = rebaixoZ/2
            x3 = radiusRebaixo * np.cos( angle ) 
            y3 = radiusRebaixo * np.sin( angle )
            plt.plot(x3 + furo[0], y3 + furo[1], "r")
    if furosComRebaixo.count(1) >=1:
        for i, furo in enumerate(furosDaBase):
            if furosComRebaixo[i] == 0:
                radiusRebaixo = rebaixoZ/2
                x3 = radiusRebaixo * np.cos( angle ) 
                y3 = radiusRebaixo * np.sin( angle )
                plt.plot(x3 + furo[0], y3 + furo[1], "r")
    return furosComRebaixo, dadosParaDesenhoCotas


def definirNorma ():
    print('Qual norma você deseja usar?')
    print("1 - IEC\n2 - NEMA")
    chosenNumber = input()
    keyChosen = ""
    if chosenNumber == "1":
        keyChosen = "IEC"
    else:
        keyChosen = "NEMA"
    return keyChosen