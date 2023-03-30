import cadquery as cq

def create3DDrawing(dadosParaDesenho3D, cotasDoCliente, keyChosen, dadosDoMotorEscolhido, caracMotor): 
        rectFrontY = dadosParaDesenho3D.rectFrontY
        rectFrontX = dadosParaDesenho3D.rectFrontX
        rectH = dadosParaDesenho3D.rectH
        holeMotorFromCenter = dadosParaDesenho3D.holeMotorFromCenter
        holeBaseFromCenter = dadosParaDesenho3D.holeBaseFromCenter
        cotaKMotor = dadosParaDesenho3D.cotaKMotor
        cotaKBase = dadosParaDesenho3D.cotaKBase
        cotaKMaxBase = dadosParaDesenho3D.cotaKMaxBase
        rebaixoHBase = dadosParaDesenho3D.rebaixoHBase
        rectBackY = dadosParaDesenho3D.rectBackY
        rectBackX = dadosParaDesenho3D.rectBackX
        holeMotorFromCenterBack1 = dadosParaDesenho3D.holeMotorFromCenterBack1
        holeMotorFromCenterBack2 = dadosParaDesenho3D.holeMotorFromCenterBack2
        holeBaseFromCenterBack = dadosParaDesenho3D.holeBaseFromCenterBack
        latConDim = dadosParaDesenho3D.latConDim
        lonConDim = dadosParaDesenho3D.lonConDim
        furosComRebaixo = dadosParaDesenho3D.furosComRebaixo
        print(furosComRebaixo)

        rectFront = (cq.Workplane("XZ")
             .rect(rectFrontX,rectFrontY)
             .extrude(rectH)
             )

        rectFront = (rectFront.faces(">Y").workplane()
                .move(holeMotorFromCenter[0],holeMotorFromCenter[1])
                .hole(cotaKMotor/2,rectH)
                )
        if furosComRebaixo[0] == 1 or furosComRebaixo[1] == 1:
                rectFront = (rectFront.faces(">Y").workplane()
                        .move(holeBaseFromCenter[0],holeBaseFromCenter[1])
                        .cboreHole(cotaKBase/2,cotaKMaxBase/2,rebaixoHBase)
                        )
        else:
                rectFront = (rectFront.faces(">Y").workplane()
                        .move(holeBaseFromCenter[0],holeBaseFromCenter[1])
                        .hole(cotaKBase/2, rectH)
                        )

        rectFrontMirrored = rectFront.mirror(mirrorPlane="XY",basePointVector=(0,0, 0))



        rectBack = (cq.Workplane("XZ")
                .rect(rectBackX,rectBackY)
                .extrude(rectH))



        rectBack = (rectBack.faces(">Y").workplane()
                .move(holeMotorFromCenterBack1[0],holeMotorFromCenterBack1[1])
                .hole(cotaKMotor/2,rectH)
                )
        rectBack = (rectBack.faces(">Y").workplane()
                .move(holeMotorFromCenterBack2[0],holeMotorFromCenterBack2[1])
                .hole(cotaKMotor/2,rectH)
                )
        
        if keyChosen == "HGF":
                rectBack = (rectBack.faces(">Y").workplane()
                        .move(holeMotorFromCenterBack1[0] - (dadosDoMotorEscolhido[caracMotor["B2"]] - dadosDoMotorEscolhido[caracMotor["B mín"]]),holeMotorFromCenterBack1[1])
                        .hole(cotaKMotor/2,rectH)
                        )
                rectBack = (rectBack.faces(">Y").workplane()
                        .move(holeMotorFromCenterBack1[0] - (dadosDoMotorEscolhido[caracMotor["B3"]] - dadosDoMotorEscolhido[caracMotor["B mín"]]),holeMotorFromCenterBack2[1])
                        .hole(cotaKMotor/2,rectH)
                        )
                rectBack = (rectBack.faces(">Y").workplane()
                        .move(holeMotorFromCenterBack1[0] - (dadosDoMotorEscolhido[caracMotor["B4"]] - dadosDoMotorEscolhido[caracMotor["B mín"]]),holeMotorFromCenterBack2[1])
                        .hole(cotaKMotor/2,rectH)
                        )

        if furosComRebaixo[1] == 1 or furosComRebaixo[0] == 1:
                rectBack = (rectBack.faces(">Y").workplane()
                        .move(holeBaseFromCenterBack[0],holeBaseFromCenterBack[1])
                        .cboreHole(cotaKBase/2,cotaKMaxBase/2,rebaixoHBase)
                        )
        else:
               rectBack = (rectBack.faces(">Y").workplane()
                        .move(holeBaseFromCenterBack[0],holeBaseFromCenterBack[1])
                        .hole(cotaKBase/2,rectH)
                        ) 

        rectBackMirrored = rectBack.mirror(mirrorPlane="XY",basePointVector=(0,0, 0))



        latitudeConnectionBar = cq.Workplane("XZ").box(latConDim[0],latConDim[1],latConDim[2])
        longitudeConnectionBar = cq.Workplane("XZ").box(lonConDim[0],lonConDim[1],lonConDim[2])

        assembly = (cq.Assembly(rectFront, name = 'rectFront',color=cq.Color("green"), loc=cq.Location(cq.Vector(0,rectH,0)))
                .add(latitudeConnectionBar, name = 'latitudeConnectionBar',color=cq.Color("red"), loc=cq.Location(cq.Vector(0,-rectH/2,-rectFrontY/2-latConDim[1]/2)))
                .add(rectFrontMirrored, name = 'rectFrontMirrored',color=cq.Color("green"), loc = cq.Location(cq.Vector(0,0,-rectFrontY-latConDim[1])))
                .add(longitudeConnectionBar, name = 'longitudeConnectionBar2',color=cq.Color("red"), loc = cq.Location(cq.Vector(rectFrontX/2+lonConDim[0]/2,-rectH/2,-rectFrontY-latConDim[1])))
                .add(rectBackMirrored, name = 'rectBackMirrored',color=cq.Color("green"),loc = cq.Location(cq.Vector(rectFrontX/2+lonConDim[0]+rectBackX/2,0,-rectFrontY-latConDim[1])) )
                .add(latitudeConnectionBar, name = 'latitudeConnectionBar2',color=cq.Color("red"), loc= cq.Location(cq.Vector(rectFrontX/2+lonConDim[0]+rectBackX/2,-rectH/2,-rectFrontY/2-latConDim[1]/2)))
                .add(rectBack, name = 'rectBack',color=cq.Color("green"), loc= cq.Location(cq.Vector(rectFrontX/2+lonConDim[0]+rectBackX/2,0,0)))
                .add(longitudeConnectionBar, name = 'longitudeConnectionBar',color=cq.Color("red"), loc = cq.Location(cq.Vector(rectFrontX/2+lonConDim[0]/2,-rectH/2,0)))
                )
        assembly.save(f'{cotasDoCliente["NOME"]}.step')


""" rectFront = (cq.Workplane("XZ")
             .rect(rectFrontX,rectFrontY)
             .extrude(rectH)
             )

        rectFront = (rectFront.faces(">Y").workplane()
                .move(holeMotorFromCenter[0],holeMotorFromCenter[1])
                .hole(cotaKMotor/2,rectH)
                )
        rectFront = (rectFront.faces(">Y").workplane()
                .move(holeBaseFromCenter[0],holeBaseFromCenter[1])
                .cboreHole(cotaKBase/2,cotaKMaxBase/2,rebaixoHBase)
                )

        rectFrontMirrored = rectFront.mirror(mirrorPlane="XY",basePointVector=(0,0, 0))



        rectBack = (cq.Workplane("XY")
                .rect(rectBackX,rectBackY)
                .extrude(rectH))



        rectBack = (rectBack.faces(">Z").workplane()
                .move(holeMotorFromCenterBack1[0],holeMotorFromCenterBack1[1])
                .hole(cotaKMotor/2,rectH)
                )
        rectBack = (rectBack.faces(">Z").workplane()
                .move(holeMotorFromCenterBack2[0],holeMotorFromCenterBack2[1])
                .hole(cotaKMotor/2,rectH)
                )
        rectBack = (rectBack.faces(">Z").workplane()
                .move(holeBaseFromCenterBack[0],holeBaseFromCenterBack[1])
                .cboreHole(cotaKBase/2,cotaKMaxBase/2,rebaixoHBase)
                )

        rectBackMirrored = rectBack.mirror(mirrorPlane="XZ",basePointVector=(0,0, 0))



        latitudeConnectionBar = cq.Workplane("XZ").box(latConDim[0],latConDim[1],latConDim[2])
        longitudeConnectionBar = cq.Workplane("XZ").box(lonConDim[0],lonConDim[1],lonConDim[2])

        assembly = (cq.Assembly(rectFront, name = 'rectFront',color=cq.Color("green"), loc=cq.Location(cq.Vector(0,rectH,0)))
                .add(latitudeConnectionBar, name = 'latitudeConnectionBar',color=cq.Color("red"), loc=cq.Location(cq.Vector(0,-rectH/2,-rectFrontY/2-latConDim[1]/2)))
                .add(rectFrontMirrored, name = 'rectFrontMirrored',color=cq.Color("green"), loc = cq.Location(cq.Vector(0,0,-rectFrontY-latConDim[1])))
                .add(longitudeConnectionBar, name = 'longitudeConnectionBar2',color=cq.Color("red"), loc = cq.Location(cq.Vector(rectFrontX/2+lonConDim[0]/2,-rectH/2,-rectFrontY-latConDim[1])))
                #.add(rectFrontMirrored, name = 'rectFrontMirrored',color=cq.Color("green"))
                #.add(rectBack, name = 'rectBack',color=cq.Color("green"))
                #.add(rectBackMirrored, name = 'rectBackMirrored',color=cq.Color("green"))
                )

        assembly = (assembly
                #.add(latitudeConnectionBar, name = 'latitudeConnectionBar2',color=cq.Color("red"))
                #.add(longitudeConnectionBar, name = 'longitudeConnectionBar',color=cq.Color("red"))
                #.add(longitudeConnectionBar, name = 'longitudeConnectionBar2',color=cq.Color("red"))
                #.constrain("rectFront@faces@<Z", "latitudeConnectionBar@faces@>Z", "Plane")
                #.constrain("rectFront@faces@<X", "longitudeConnectionBar@faces@>X", "Plane")
                #.constrain("rectBack@faces@>X", "longitudeConnectionBar@faces@<X", "Plane")
                #.constrain("rectBack@faces@<Y", "latitudeConnectionBar2@faces@>Y", "Plane")
                #.constrain("rectBackMirrored@faces@>Y", "latitudeConnectionBar2@faces@<Y", "Plane")
                #.constrain("rectBackMirrored@faces@>X", "longitudeConnectionBar2@faces@<X", "Plane")
                #.constrain("rectFrontMirrored@faces@<X", "longitudeConnectionBar2@faces@>X", "Plane")
                #.constrain("rectFrontMirrored@faces@>Y", "latitudeConnectionBar@faces@<Y", "Plane")
                
                )
        
        #assembly = assembly.solve()"""
