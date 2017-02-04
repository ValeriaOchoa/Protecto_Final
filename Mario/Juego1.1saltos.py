import sys, pygame
import StringIO
import json
import gzip
import base64
from pygame.locals import *
from pygame.constants import K_x

# Constantes
WIDTH = 900#ancho pantalla
HEIGHT = 500#altura de pantalla
PposX=300#posicion den x de mario
PposY=318#posicion en y de mario 
cont=6
dire=True#direccion 
i=0#guardara la posicion del arreglo 
xixf={}#xinicio y xfin movimiento derecha
Rxixf={}#xinicio y Xfin movimiento izquierda 
Scurva={}#arreglo para los saltos
saltar = False 
saltar_Cur=False
tWidth=0# tamaño del ancho del tile 
tHeigth=0# tamaño de la altura del tile
WidthMap=0# ancho del mapa
HeightMap=0# altura del mapa
MatrizMapa=[]# arreglo para el mapa


#=================>>>>IMAGEN<<<<====================================
def imagen(n_archivo, transparencia=False):# parametros el nombre de la imagen y su tipo.
        try: image = pygame.image.load(n_archivo)#detecta el error de archivos
        except pygame.error, message:
                raise SystemExit, message
        image = image.convert()#convierte la imagen para python
        if transparencia:
                color = image.get_at((0,0))#Obtiene el color de la parte sup izquierda de la imagen
                image.set_colorkey(color, RLEACCEL)#le damos la orden para que ese color no aparesca
        return image

#======================>>>>TECLADO<<<<===================================
def teclado():# funcion para el teclado que maneja el movimiento
    teclado = pygame.key.get_pressed()# Pygame obtine la informacion del teclado obtiene 
     
    global PposX# llama a la posicion del personaje(Mario)
    global cont, dire, saltar, saltar_Cur#llamada a variables globales

    if teclado[K_x] and teclado[K_RIGHT] and saltar_Cur==False:
        saltar_Cur=True
    elif teclado[K_x] and teclado[K_LEFT] and saltar_Cur==False:
        saltar_Cur=True
         
    elif teclado[K_RIGHT]and saltar==False and saltar_Cur==False:
        PposX+=2
        cont+=1
        dire=True
    elif teclado[K_LEFT]and saltar==False and saltar_Cur==False:
        PposX-=2
        cont+=1
        dire=False
    elif teclado[K_x] and saltar==False and saltar_Cur==False:
        saltar=True          
    else :
         cont=6
         
    return

#===================>>>>SPRITE<<<<===============================
def spriteMARIO():
 
    global cont
 #tamaño en bits de la imagen (donde,inicia,donde,termina)
    xixf[0]=(0,0,20,41)#primer dibujo
    xixf[1]=(21,0,25,41)#segundo dibujo
    xixf[2]=(47,0,25,41)
    xixf[3]=(73,0,20,41)
    xixf[4]=(93,0,27,41)
    xixf[5]=(120,0,27,41)
 #medidas al reves para que se de la vuelta la imagen. 
    Rxixf[0]=(122,0,21,41)
    Rxixf[1]=(96,0,25,41)
    Rxixf[2]=(74,0,22,41)
    Rxixf[3]=(50,0,23,41)
    Rxixf[4]=(24,0,26,41)
    Rxixf[5]=(0,0,25,41)
   
    p=6 #inicio del contador
   
    global i# aqui se guarda el valor 
    # este es un contador para que cuando llegue a 6 el contador cambie la imagen
    if cont==p:
        i=0
   
    if cont==p*2:
        i=1
   
    if cont==p*3:
        i=2
   
    if cont==p*4:
        i=3
   
    if cont==p*5:
        i=4
   
    if cont==p*6:
       i=5
       cont=0
   
    return
#==================>>>>>CARGAR_MAPA<<<<<<=======================
def cargar_mapa(Nivel1):# creamos la funcion cargar mapa y le agregamos la variable nivel1 como parametro 
    global tWidth,tHeight,WidthMap,HeightMap,MatrizMapa# llamamos a las variables globales
    a=open ("mapas/"+Nivel1+".json","r")#acceder al archivo
    data=json.load(a)#almacenar los datos de la variable a
    a.close()
    tWidth=data["tilewidth"]
    tHeight=data["tileheight"]
    WidthMap=data["width"]
    HeightMap=data["height"]
    #tomar el mapa
    for item in data["layers"]:
        mapa=item["data"]
    print mapa
    mapa=base64.decoestring(mapa)#traducir
    print mapa
    cadena=gzip.zlib.decompress(mapa);#descomprimir los bloques de la imagen
    print cadena
    salidaMapa=[]
    for idx in xrange(0,len(cadena),4):#algoritmo de conversion a numeros de los caracteres
        val=odr(str(cadena[idx]))|(odr(str(cadena[idx+1]))<<8)|\
        (odr(str(cadena[idx+2]))<<16)| (odr(str(cadena[idx+3]))<<24)
        salidaMapa.append(val)
    print salidaMapa
    for i in range(0, len(salidaMapa),WidthMap):# convertir en matriz el mapa, for desde 0 al tamaño del mapa con porsiones del ancho del mapa.
        MatrizMapa.append(salidaMapa[i:i+WidthMap])# (tramos) añadir datos al final del mapa con la posision deseada y su ancho
    for i in range(HeightMap):
        print MatrizMapa
def arreglo_Tiles(img):#obritne imagen y lo almacena en hoja de tiles de tamaño 29 de alto y 27 de ancho
    x=0
    y=0
    hojaTiles=[]
    for i in range(29):
        for j in range(27):
            imagen=cortar(img,(x,y,16,16))
            hojaTiles.append(imagen)
            x+=18
        x=0
        y+=18
    return hojaTiles
    
def cortar(img,rectan):
    rec=pygame.Rect(rectan)
    image=pygame.Surface(rec.size).convert()
    image.blit(img,(0,0),rect)
    return image 

    

#==================>>>>>MAIN<<<<<<=====================================
 
def main():
    pygame.init()  #inicializar las variables de pygame y sus clases  
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) # tamaño de pantalla 
    pygame.display.set_caption("JuegoMario_YOSHI")#nombre en la ventana
    reloj= pygame.time.Clock()#reloj para detener el while
   
    #fondo = imagen("imagenes/fondo.png")#llamar imagen fondo      
    mario = imagen("imagenes/sprites_mario.png",True)#llamarimagen del mario, el true indica que el mario tiene transparencia
    mario_inv=pygame.transform.flip(mario,True,False);# se crea un mario a la inversa ya que transforma la imagen con valores boleanos para invertir en el true en el eje x
    img=pygame.image.load("imagenes/Mario Bros tileset.png")
    cargar_mapa("Nivel1")
    hoja=arreglo_Tiles(img)

       
    global saltar_Cur  
    caer=False
    caer_Cur=False
 
    # Bucle principal 
    while True:# revisa eventos del teclado.
        spriteMARIO()
        teclado()
        time= reloj.tick(60)
       #fondo = pygame.transform.scale(fondo, (1000, 400))#transformacion del tamaño de la imagen.
        #screen.blit(fondo, (0, 0))# carga la imagen en el filo superior izquierdo de la imagen.
        for i in range(HeightMap):
            for j in range(WidthMap):
                minum=MatrizMapa[i][j]
                tileImg=hoja[minum-1]
                tileImg=pygame.transform.scale(tileImg,(tWidth*2,tHeight*2))
                screen.blit(tileImg,(j*tWidth*2,i*tHeight*2+100))
        pygame.display.update()



        global PposX,PposY,saltar
        if dire==True and saltar==False:
        	#pinta el matio en direccion a derecha
            screen.blit(mario, (PposX, PposY),(xixf[i]))# la funcion blit nos permite pasar por parametro el archivo de imagen y pasar la posicion en X cambia dinamicamente y en Y el ultimo es un array de donde a donde se dibuja la imagen.
        if dire==False and saltar==False:
        	#pinta el mario a la izquierda
            screen.blit(mario_inv, (PposX, PposY),(Rxixf[i]))# carga la imagen de mario en esa posicion.
#=========>>>>>>>>>>>>>>SALTO HACIA ARRIBA
        if saltar==True:
            if dire==True:
                screen.blit(mario, (PposX, PposY),(xixf[4]))
            if dire==False:
                screen.blit(mario_inv, (PposX, PposY),(Rxixf[4]))

	    #para bajar
            if caer==False:
                PposY-=4              
                
            if caer==True:
                PposY+=4              
           
            if PposY==186:
                caer=True
           
            if PposY==318:
                caer=False
                saltar=False
#=========>>>>>>>>>>>>>>SALTO CON CURVA
        if saltar_Cur==True and dire==True:            
           
            screen.blit(mario, ( PposX, PposY),(xixf[4]))
           
            if caer_Cur==False:
                PposY-=3
                PposX+=2
               
            if caer_Cur==True:
                PposY+=3
                PposX+=2
           
            if PposY==246:
                caer_Cur=True
           
            if PposY==318:
                caer_Cur=False
                saltar_Cur=False
        elif saltar_Cur==True and dire==False:            
           
            screen.blit(mario_inv, ( PposX, PposY),(Rxixf[4]))
           
            if caer_Cur==False:
                PposY-=3
                PposX-=2
               
            if caer_Cur==True:
                PposY+=3
                PposX-=2
           
            if PposY==246:
                caer_Cur=True
           
            if PposY==318:
                caer_Cur=False
                saltar_Cur=False  

        pygame.display.flip()
 		#CERRAR PROGRAMA
        for event in pygame.event.get():# Posibles entradas del teclado y mouse
            if event.type == pygame.QUIT:
                sys.exit()
   
    return 0
 
if __name__ == '__main__':#
    main()
