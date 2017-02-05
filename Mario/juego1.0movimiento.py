import sys, pygame
from pygame.locals import *
##from Tkconstants import FALSE
import winsound
from time import clock

#Constantes
#Tamaño  la pantalla
WIDTH = 900
HEIGHT = 400

PposX =70 #posicion de mario
PposY =335

cont=6
dire=True#direccion 
i=0#guardara la posicion del arreglo
 
caer=False
saltar = False

##xixf={}#xinicio y xfin movimiento derecha
##Rxixf={}#xinicio y Xfin movimiento izquierda 
##Scurva={}


##===================>>>>incio<<<<===============================
def Incio():
    global screen, clock,xixf,Rxixf
    pygame.init()    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))# tamaño de pantalla
    pygame.display.set_caption("Juego Mario")
    clock = pygame.time.Clock()
    xixf={}
    Rxixf={}
    #tamaño en bits de la imagen (donde,inicia,donde,termina)
    xixf[0]=(0,0,20,41)#primer dibujo
    xixf[1]=(22,0,25,41)#segundo dibujo
    xixf[2]=(47,0,25,41)
    xixf[3]=(73,0,20,41)
    xixf[4]=(93,0,27,41)
    xixf[5]=(120,0,27,41)
    #medidas al reves para que se de la vuelta la imagen.
    Rxixf[0]=(122,0,22,41)
    Rxixf[1]=(96,0,25,41)
    Rxixf[2]=(74,0,22,41)
    Rxixf[3]=(50,0,23,41)
    Rxixf[4]=(24,0,26,41)
    Rxixf[5]=(0,0,25,41)
   
 
def Fondo():
    global fondo, mario,mario_inv,enemig 
    fondo = imagen("imagenes/escenario1.png")#llamar imagen fondo
    ##    winsound.PlaySound("Mario.wav", winsound.SND_FILENAME)
    mario = imagen("imagenes/sprites_mario.png",True)#llamar imagen del mario, el true indica que el mario tiene transparencia
    mario_inv=pygame.transform.flip(mario,True,False);# se crea un mario a la inversa ya que transforma la imagen con valores boleanos para invertir en el true en el eje x
    fondo = pygame.transform.scale(fondo, (1000, 400))#transformacion del tamaño de la imagen.
    
 
def Llamado():   
    teclado()    
    SpriteMario()  
    

def Pos():
    global saltar,saltar_Par, saltar,caer_Par,caer
    screen.blit(fondo, (0, 0))
    global PposX,PposY
    if dire==True and saltar==False :
        #pinta el mario en direccion a derecha
        screen.blit(mario, ( PposX, PposY),(xixf[i]))# la funcion blit nos permite pasar por parametro el archivo de imagen y pasar la posicion en X cambia dinamicamente y en Y el ultimo es un array de donde a donde se dibuja la imagen.
    if dire==False and saltar==False :
        #pinta el mario a la izquierda
        screen.blit(mario_inv, ( PposX, PposY),(Rxixf[i]))# carga la imagen de mario en esa posicion.
       
       
#=========>>>>>>>>>>>>>>SALTO HACIA ARRIBA
    if saltar==True:            
           
        if dire==True:
            screen.blit(mario, ( PposX, PposY),(xixf[4]))
        if dire==False:
            screen.blit(mario_inv, ( PposX, PposY),(Rxixf[4]))  
           
        if caer==False:
            PposY-=8              
               
        if caer==True:
            PposY+=8              
           
        if PposY<=186:
            caer=True
           
        if PposY>=335:
            caer=False
            saltar=False

   
#=================>>>>IMAGEN<<<<====================================
def imagen(n_archivo, transparencia=False):# parametros el nombre de la imagen y su tipo.
        try: image = pygame.image.load(n_archivo)#detecta el error de archivos
        except pygame.error as message:
                raise SystemExit(message)
        image = image.convert()#convierte la imagen para python
        if transparencia:
                color = image.get_at((0,0))#Obtiene el color de la parte sup izquierda de la imagen
                image.set_colorkey(color, RLEACCEL)#le damos la orden para que ese color no aparesca
        return image
 
#======================>>>>TECLADO<<<<===================================
def teclado():
    global cont, dire,saltar,PposX
    teclado = pygame.key.get_pressed()
    if teclado[K_UP]:
       saltar=True
       sonido= pygame.mixer.Sound("Salto.wav")
       sonido.play();
       
    if teclado[K_RIGHT]:
        if PposX<=810:
            PposX+=2
        cont+=1
        dire=True
        
    elif teclado[K_LEFT]:
        if PposX>10:
            PposX-=2
            print(PposX)
        cont+=1
        dire=False
     
    else :
         cont=6
         
    #CERRAR PROGRAMA
    for event in pygame.event.get():# Posibles entradas del teclado y mouse
        if event.type == pygame.QUIT:
            sys.exit()
         
#===================SPRITE===============================
def SpriteMario():
    global cont  # aqui se guarda el valor 
    p=6#inicio del contador  
    # este es un contador para que cuando llegue a 6 el contador cambie la imagen
    global i# aqui se guarda el valor
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

#==================>>>>>MAIN<<<<<<=====================================    
def main():
    Incio()
    Fondo()
    pygame.mixer.music.load("Mario.wav")#llamada a la musica
    pygame.mixer.music.play(-1)
# Bucle principal
    while True:# revisa eventos del teclado.
        time = clock.tick(60)
        Llamado()
        Pos()
        Fondo()


        pygame.display.flip()
##    global saltar_Cur  
##    caer=False
##    caer_Cur=False
 

        
        
        

###=========>>>>>>>>>>>>>>SALTO CON CURVA
##        if saltar_Cur==True and dire==True:            
##           
##            screen.blit(mario, ( PposX, PposY),(xixf[4]))
##           
##            if caer_Cur==False:
##                PposY-=3
##                PposX+=2
##               
##            if caer_Cur==True:
##                PposY+=3
##                PposX+=2
##           
##            if PposY==246:
##                caer_Cur=True
##           
##            if PposY==318:
##                caer_Cur=False
##                saltar_Cur=False
##        elif saltar_Cur==True and dire==FALSE:            
##           
##            screen.blit(mario_inv, ( PposX, PposY),(Rxixf[4]))
##           
##            if caer_Cur==False:
##                PposY-=3
##                PposX-=2
##               
##            if caer_Cur==True:
##                PposY+=3
##                PposX-=2
##           
##            if PposY==246:
##                caer_Cur=True
##           
##            if PposY==318:
##                caer_Cur=False
##                saltar_Cur=False  

       

##   
##    return 0
   


         
##        return
 
#if __name__ == '__main__':#
        
 
main()

 
