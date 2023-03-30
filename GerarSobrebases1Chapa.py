import csv
from classses import DadosParaDesenho3D
import functions
from constants import geometriaDosMotoresMap, caracMotor
import matplotlib.pyplot as plt
from drawing3D import create3DDrawing
import ocp


geometriaDosMotoresList = []
dadosParaDesenho3D = DadosParaDesenho3D()

normaEscolhida = functions.definirNorma()

with open(f"Geometria das linhas W50 W51 HGF {normaEscolhida}.csv", "r") as geometriaDosMotores:
    readDataFromCSV = csv.reader(geometriaDosMotores, delimiter=";")
    for row in readDataFromCSV:
        geometriaDosMotoresList.append(row)
        for key in geometriaDosMotoresMap.keys():
            if row[0] == key:
                geometriaDosMotoresMap[key] = geometriaDosMotoresMap[key] + [row[1]]

keyChosen = functions.escolherLinhaDoMotor()
dadosDoMotorEscolhido, linhaMotorEscolhido = functions.frameEscolhido(geometriaDosMotoresList, geometriaDosMotoresMap, keyChosen) 
cotasDoCliente = functions.dadosDeVendas(hmotor= dadosDoMotorEscolhido[caracMotor["H"]], norma = normaEscolhida)
dadosParaDesenho3D.rectH = cotasDoCliente["H"] - dadosDoMotorEscolhido[caracMotor["H"]]
dadosParaDesenho3D.cotaKMotor = dadosDoMotorEscolhido[caracMotor["K"]]



furoBaseSO1 = [0,0]
furoBaseNO1 = [0,cotasDoCliente["A"]]
furoBaseNL1 = [cotasDoCliente["B"], cotasDoCliente["A"]]
furoBaseSL1 = [cotasDoCliente["B"], 0]

comprimentoZ = cotasDoCliente["B"] + cotasDoCliente["C"] - float(dadosDoMotorEscolhido[caracMotor["C"]])
furoMotorSL1 = [comprimentoZ, cotasDoCliente["A"]/2 - dadosDoMotorEscolhido[caracMotor["A"]]/2]
furoMotorNL1 = [comprimentoZ, cotasDoCliente["A"]/2 + dadosDoMotorEscolhido[caracMotor["A"]]/2]
furoMotorSO1 = [comprimentoZ - dadosDoMotorEscolhido[caracMotor["B mín"]], cotasDoCliente["A"]/2 - dadosDoMotorEscolhido[caracMotor["A"]]/2]
furoMotorNO1 = [comprimentoZ - dadosDoMotorEscolhido[caracMotor["B mín"]], cotasDoCliente["A"]/2 + dadosDoMotorEscolhido[caracMotor["A"]]/2]
furoMotorSO2 = [comprimentoZ - dadosDoMotorEscolhido[caracMotor["B máx"]], cotasDoCliente["A"]/2 - dadosDoMotorEscolhido[caracMotor["A"]]/2]
furoMotorNO2 = [comprimentoZ - dadosDoMotorEscolhido[caracMotor["B máx"]], cotasDoCliente["A"]/2 + dadosDoMotorEscolhido[caracMotor["A"]]/2]


baseMotorSLSL = [furoMotorSL1[0] + dadosDoMotorEscolhido[caracMotor["BD"]], furoMotorSL1[1] - dadosDoMotorEscolhido[caracMotor["AA"]]/2]
baseMotorSLSO = [baseMotorSLSL[0] - dadosDoMotorEscolhido[caracMotor["BA"]], furoMotorSL1[1] - dadosDoMotorEscolhido[caracMotor["AA"]]/2]
baseMotorSLNL = [furoMotorSL1[0] + dadosDoMotorEscolhido[caracMotor["BD"]], furoMotorSL1[1] + dadosDoMotorEscolhido[caracMotor["AA"]]/2]
baseMotorSLNO = [baseMotorSLSL[0] - dadosDoMotorEscolhido[caracMotor["BA"]], furoMotorSL1[1] + dadosDoMotorEscolhido[caracMotor["AA"]]/2]
limiteBaseMotorSL = [baseMotorSLNL[0], baseMotorSLNL[1], baseMotorSLSO[0], baseMotorSLSO[1]]

baseMotorNLSL = [furoMotorSL1[0] + dadosDoMotorEscolhido[caracMotor["BD"]], furoMotorNL1[1] - dadosDoMotorEscolhido[caracMotor["AA"]]/2]
baseMotorNLSO = [baseMotorSLSL[0] - dadosDoMotorEscolhido[caracMotor["BA"]], furoMotorNL1[1] - dadosDoMotorEscolhido[caracMotor["AA"]]/2]
baseMotorNLNL = [furoMotorSL1[0] + dadosDoMotorEscolhido[caracMotor["BD"]], furoMotorNL1[1] + dadosDoMotorEscolhido[caracMotor["AA"]]/2]
baseMotorNLNO = [baseMotorSLSL[0] - dadosDoMotorEscolhido[caracMotor["BA"]], furoMotorNL1[1] + dadosDoMotorEscolhido[caracMotor["AA"]]/2]
limiteBaseMotorNL = [baseMotorNLNL[0], baseMotorNLNL[1], baseMotorNLSO[0], baseMotorNLSO[1]]

baseMotorSOSO = [baseMotorSLSL[0] - dadosDoMotorEscolhido[caracMotor["BB"]], furoMotorSO1[1] - dadosDoMotorEscolhido[caracMotor["AA"]]/2]
baseMotorSONO = [baseMotorSOSO[0], furoMotorSO1[1] + dadosDoMotorEscolhido[caracMotor["AA"]]/2]
baseMotorSOSL = [baseMotorSOSO[0] + dadosDoMotorEscolhido[caracMotor["BC"]], furoMotorSO1[1] - dadosDoMotorEscolhido[caracMotor["AA"]]/2]
baseMotorSONL = [baseMotorSOSL[0], baseMotorSONO[1]]
limiteBaseMotorSO = [baseMotorSONL[0], baseMotorSONL[1], baseMotorSOSO[0], baseMotorSOSO[1]]

baseMotorNOSO = [baseMotorSOSO[0], furoMotorNO1[1] - dadosDoMotorEscolhido[caracMotor["AA"]]/2]
baseMotorNONO = [baseMotorSOSO[0], furoMotorNO1[1] + dadosDoMotorEscolhido[caracMotor["AA"]]/2]
baseMotorNOSL = [baseMotorSOSL[0], baseMotorNOSO[1]]
baseMotorNONL = [baseMotorSOSL[0], baseMotorNONO[1]]
limiteBaseMotorNO = [baseMotorNONL[0], baseMotorNONL[1], baseMotorNOSO[0], baseMotorNOSO[1]]

#plot do furo da base
plt.plot([furoBaseNO1[0], furoBaseNL1[0], furoBaseSL1[0], furoBaseSO1[0]],[furoBaseNO1[1], furoBaseNL1[1], furoBaseSL1[1], furoBaseSO1[1]], "ro")
#plot do furo do motor
plt.plot([furoMotorNO1[0], furoMotorNL1[0], furoMotorSL1[0], furoMotorSO1[0], furoMotorSO2[0], furoMotorNO2[0]],[furoMotorNO1[1], furoMotorNL1[1], furoMotorSL1[1], furoMotorSO1[1], furoMotorSO2[1], furoMotorNO2[1]], "bo")
#plot dos pés do motor
plt.plot([baseMotorSLSO[0], baseMotorSLSL[0], baseMotorSLNL[0], baseMotorSLNO[0], baseMotorSLSO[0]], [baseMotorSLSO[1], baseMotorSLSL[1], baseMotorSLNL[1], baseMotorSLNO[1], baseMotorSLSO[1]], "b")
plt.plot([baseMotorNLSO[0], baseMotorNLSL[0], baseMotorNLNL[0], baseMotorNLNO[0], baseMotorNLSO[0]], [baseMotorNLSO[1], baseMotorNLSL[1], baseMotorNLNL[1], baseMotorNLNO[1], baseMotorNLSO[1]], "b")
plt.plot([baseMotorSOSO[0], baseMotorSOSL[0], baseMotorSONL[0], baseMotorSONO[0], baseMotorSOSO[0]], [baseMotorSOSO[1], baseMotorSOSL[1], baseMotorSONL[1], baseMotorSONO[1], baseMotorSOSO[1]], "b")
plt.plot([baseMotorNOSO[0], baseMotorNOSL[0], baseMotorNONL[0], baseMotorNONO[0], baseMotorNOSO[0]], [baseMotorNOSO[1], baseMotorNOSL[1], baseMotorNONL[1], baseMotorNONO[1], baseMotorNOSO[1]], "b")

furosDoMotor = [furoMotorSO1, furoMotorSL1, furoMotorNL1, furoMotorNO1, furoMotorNO2, furoMotorSO2]
furosDaBase = [furoBaseNL1, furoBaseNO1, furoBaseSO1, furoBaseSL1]
limitesBaseMotor = [limiteBaseMotorNL, limiteBaseMotorNO, limiteBaseMotorSO, limiteBaseMotorSL]
furosComRebaixo, dadosParaDesenhoCotas = functions.gerarFurosSemFuroLongo(furosDoMotor, furosDaBase, dadosDoMotorEscolhido, limitesBaseMotor, cotasDoCliente)

furoBaseCritico = [furoBaseNL1, furoBaseNO1, furoBaseSO1, furoBaseSL1]
print(furoBaseCritico)
baseMotorCritico = [[baseMotorNLNL, baseMotorNLSO], [baseMotorNONL, baseMotorNOSO], [baseMotorSONL, baseMotorSOSO],[baseMotorSLNL, baseMotorSLSO]]
chapasMetalicasBase = functions.gerarChapasMetalicasBase(furoBaseCritico,baseMotorCritico, dadosDoMotorEscolhido, furosComRebaixo) #NL, NO, SO, SL

dadosParaDesenho3D.furosComRebaixo = furosComRebaixo
dadosParaDesenho3D.rectFrontY = chapasMetalicasBase[0][1] - chapasMetalicasBase[0][3]
dadosParaDesenho3D.rectFrontX = chapasMetalicasBase[0][0] - chapasMetalicasBase[0][2]
dadosParaDesenho3D.rectFrontPos = [chapasMetalicasBase[0][2] + dadosParaDesenho3D.rectFrontX/2, chapasMetalicasBase[0][3] + dadosParaDesenho3D.rectFrontY/2]
dadosParaDesenho3D.middlePoint = [(chapasMetalicasBase[0][0]+chapasMetalicasBase[1][2])/2, (chapasMetalicasBase[0][1]+chapasMetalicasBase[3][3])/2]
dadosParaDesenho3D.holeMotorFromCenter = [furoMotorNL1[0] - dadosParaDesenho3D.rectFrontPos[0], furoMotorNL1[1] - dadosParaDesenho3D.rectFrontPos[1]]
dadosParaDesenho3D.holeBaseFromCenter = [furoBaseNL1[0] - dadosParaDesenho3D.rectFrontPos[0], furoBaseNL1[1] - dadosParaDesenho3D.rectFrontPos[1]]

dadosParaDesenho3D.rectBackY = chapasMetalicasBase[1][1] - chapasMetalicasBase[1][3]
dadosParaDesenho3D.rectBackX = chapasMetalicasBase[1][0] - chapasMetalicasBase[1][2]
dadosParaDesenho3D.rectBackPos = [chapasMetalicasBase[1][2] + dadosParaDesenho3D.rectBackX/2, chapasMetalicasBase[1][3] + dadosParaDesenho3D.rectBackY/2]
dadosParaDesenho3D.holeBaseFromCenterBack = [furoBaseNO1[0]- dadosParaDesenho3D.rectBackPos[0], furoBaseNO1[1]- dadosParaDesenho3D.rectBackPos[1]]
dadosParaDesenho3D.holeMotorFromCenterBack1 = [furoMotorNO1[0] - dadosParaDesenho3D.rectBackPos[0], furoMotorNO1[1] - dadosParaDesenho3D.rectBackPos[1]]
dadosParaDesenho3D.holeMotorFromCenterBack2 = [furoMotorNO2[0] - dadosParaDesenho3D.rectBackPos[0], furoMotorNO2[1] - dadosParaDesenho3D.rectBackPos[1]]

dadosParaDesenho3D.cotaKBase = dadosParaDesenhoCotas[0]
dadosParaDesenho3D.cotaKMaxBase = dadosParaDesenhoCotas[1]
dadosParaDesenho3D.rebaixoHBase = dadosParaDesenhoCotas[2]

#Gerar as ligações
v1 = chapasMetalicasBase[0][0] - chapasMetalicasBase[0][2]
v2 = chapasMetalicasBase[0][1] - chapasMetalicasBase[0][3]
v3 = chapasMetalicasBase[1][0] - chapasMetalicasBase[1][2]
min = min(v1,v2,v3)
compChapaLiga = min * 0.8/2

pontoMedioNLO = [chapasMetalicasBase[0][2], chapasMetalicasBase[0][1]/2 + chapasMetalicasBase[0][3]/2]
pontoMedioNOL = [chapasMetalicasBase[1][0], chapasMetalicasBase[1][1]/2 + chapasMetalicasBase[1][3]/2]
pontoMedioNOS = [chapasMetalicasBase[1][0]/2 + chapasMetalicasBase[1][2]/2, chapasMetalicasBase[1][3]]
pontoMedioSON = [chapasMetalicasBase[2][0]/2 + chapasMetalicasBase[2][2]/2, chapasMetalicasBase[2][1]]
pontoMedioSOL = [chapasMetalicasBase[2][0], chapasMetalicasBase[2][1]/2 + chapasMetalicasBase[2][3]/2]
pontoMedioSLO = [chapasMetalicasBase[3][2], chapasMetalicasBase[3][1]/2 + chapasMetalicasBase[3][3]/2]
pontoMedioSLN = [chapasMetalicasBase[3][0]/2 + chapasMetalicasBase[3][2]/2, chapasMetalicasBase[3][1]]
pontoMedioNLS = [chapasMetalicasBase[0][0]/2 + chapasMetalicasBase[0][2]/2, chapasMetalicasBase[0][3]]

pontosMediosChapaLiga = [pontoMedioNLO, pontoMedioNOL, pontoMedioNOS, pontoMedioSON, pontoMedioSOL, pontoMedioSLO, pontoMedioSLN, pontoMedioNLS]

dadosParaDesenho3D.latConDim = [compChapaLiga*2, pontoMedioNLS[1] - pontoMedioSLN[1], dadosParaDesenho3D.rectH/2]
dadosParaDesenho3D.lonConDim = [pontoMedioNLO[0] - pontoMedioNOL[0], compChapaLiga*2, dadosParaDesenho3D.rectH/2]



for i in range(0,4):
    n1 = 0
    n2 = 0
    n3 = 0
    n4 = 0
    if pontosMediosChapaLiga[2*i][1] == pontosMediosChapaLiga[2*i + 1][1]:
        n1 = [pontosMediosChapaLiga[2*i][0], pontosMediosChapaLiga[2*i][1] + compChapaLiga] 
        n2 = [pontosMediosChapaLiga[2*i][0], pontosMediosChapaLiga[2*i][1] - compChapaLiga]
        n3 = [pontosMediosChapaLiga[2*i + 1][0], pontosMediosChapaLiga[2*i+1][1] + compChapaLiga] 
        n4 = [pontosMediosChapaLiga[2*i + 1][0], pontosMediosChapaLiga[2*i+1][1] - compChapaLiga]
    else: 
        n1 = [pontosMediosChapaLiga[2*i][0] + compChapaLiga, pontosMediosChapaLiga[2*i][1]] 
        n2 = [pontosMediosChapaLiga[2*i][0] - compChapaLiga, pontosMediosChapaLiga[2*i][1]]
        n3 = [pontosMediosChapaLiga[2*i+1][0] + compChapaLiga, pontosMediosChapaLiga[2*i + 1][1]] 
        n4 = [pontosMediosChapaLiga[2*i+1][0] - compChapaLiga, pontosMediosChapaLiga[2*i + 1][1]]
    plt.plot([n1[0],n3[0]],[n1[1],n3[1]],'g')
    plt.plot([n2[0],n4[0]],[n2[1],n4[1]],'g')


#plot indicações
plt.annotate('Furo base', xy=(furoBaseNL1[0], furoBaseNL1[1]), xytext=(furoBaseNL1[0] + 100, furoBaseNL1[1] + 100),
             arrowprops=dict(facecolor='black', shrink=0.05),
             )
plt.annotate('Furo Motor', xy=(furoMotorSL1[0], furoMotorSL1[1]), xytext=(furoMotorSL1[0] + 100, furoMotorSL1[1] + 100),
             arrowprops=dict(facecolor='black', shrink=0.05),
             )
plt.annotate('Pés do Motor', xy=(baseMotorSOSO[0], baseMotorSOSO[1]), xytext=(baseMotorSOSO[0] + 100, baseMotorSOSO[1] + 100),
             arrowprops=dict(facecolor='black', shrink=0.05),
             )

plt.annotate('Sobrebase', xy=(chapasMetalicasBase[1][2], chapasMetalicasBase[1][1]), xytext=(chapasMetalicasBase[1][2] + 100, chapasMetalicasBase[1][1] + 100),
             arrowprops=dict(facecolor='black', shrink=0.05),
             )
create3DDrawing(dadosParaDesenho3D, cotasDoCliente, keyChosen, dadosDoMotorEscolhido, caracMotor)
plt.axis('equal')
plt.show()

#Mudar limite de altura