#AutoEstrada.Avi

import cv2

ncarros = 0
ncarros_atuais = 0
ncarros_frame_anterior = 0


cap = cv2.VideoCapture("AutoEstrada.avi")

object_detector = cv2.createBackgroundSubtractorMOG2()



def update_ncarros(ncarros,ncarros_atuais,ncarros_frame_anterior):
    
    if(ncarros_atuais == ncarros_frame_anterior):
        ncarros = ncarros;
    elif(ncarros_atuais > ncarros_frame_anterior):
        ncarros = ncarros + (ncarros_atuais - ncarros_frame_anterior);
    return ncarros

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
  
while (cap.isOpened()):
    #lê o frame atual
    ret, frame = cap.read()

    if ret == True:

        #desenha um retângulo na zona de deteção de veículos
        cv2.rectangle(frame,(45,100),(202,202),(255,0,0),2)
        
        #filtro que aplica os contornos apenas nessa região
        filtro = frame[100:202,45:202]

        #máscara que permite a destinção de objetos relativamente ao ambiente
        mask = object_detector.apply(filtro)
        
        
        
        #binarização do frame
        _, mask = cv2.threshold(mask,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        #contornos
        contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        veiculos = []

        id_carros = ncarros
        
        for cnt in contours:
            i = 0
            area = cv2.contourArea(cnt)

           #filtro de contorno
            if area>250:
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(filtro,(x,y),(x+w,y+h),(0,255,0),2)
                veiculos.append([x,y,w,h])
                ncarros_atuais = len(veiculos) - 1
                cv2.putText(frame,str(id_carros+i),(x,y+100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                i = i+1;
        ncarros = update_ncarros(ncarros,ncarros_atuais,ncarros_frame_anterior)
        ncarros_frame_anterior = ncarros_atuais
                
        print("CARROS Atuais")
        print(ncarros_atuais)
        print("CARROS")
        print(ncarros)
        cv2.imshow("Frame", frame)
    
        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else: 
        break

    
print("CARROS")
print(ncarros)
cap.release()
cv2.destroyAllWindows()

