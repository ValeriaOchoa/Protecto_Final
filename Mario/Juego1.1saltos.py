import sys, pygame
from pygame.locals import *
from Tkconstants import FALSE
 
# Constantes
WIDTH = 900
HEIGHT = 500
PposX=300#posicion de mario
PposY=318#
cont=6
dire=True#direccion 
i=0#guardara la posicion del arreglo 
xixf={}#xinicio y xfin movimiento derecha
Rxixf={}#xinicio y Xfin movimiento izquierda 
Scurva={}
saltar = False 
saltar_Cur=False

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
#==================>>>>>MAIN<<<<<<=====================================
 
def main():
    pygame.init()  #inicializar las variables de pygame y sus clases  
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) # tamaño de pantalla 
    pygame.display.set_caption("JuegoMario_YOSHI")#nombre en la ventana
 
   
    fondo = imagen("imagenes/fondo.png")#llamar imagen fondo      
    mario = imagen("imagenes/sprites_mario.png",True)#llamarimagen del mario, el true indica que el mario tiene transparencia
    mario_inv=pygame.transform.flip(mario,True,False);# se crea un mario a la inversa ya que transforma la imagen con valores boleanos para invertir en el true en el eje x
    reloj= pygame.time.Clock()#reloj para detener el while
    
    global saltar_Cur  
    caer=False
    caer_Cur=False
 
    # Bucle principal 
    while True:# revisa eventos del teclado.
        spriteMARIO()
        teclado()
        time= reloj.tick(60)
        fondo = pygame.transform.scale(fondo, (1000, 400))#transformacion del tamaño de la imagen.
        screen.blit(fondo, (0, 0))# carga la imagen en el filo superior izquierdo de la imagen.
        
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
