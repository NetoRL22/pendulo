import cv2
import os
from datetime import datetime, timezone
import numpy as np
import ga

def mass_center(shape,minA,maxA):
     if cv2.contourArea(shape) < minA:
          return ["ERRO","ERRO"]
     if cv2.contourArea(shape) > maxA:
          return ["ERRO","ERRO"]
     M = cv2.moments(shape)
     if M["m00"] != 0:
        X = int(M["m10"] / M["m00"])
        Y = int(M["m01"] / M["m00"])
     return [X,Y]

def extract_pixel_data (i,frame):
    r = [i]
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    green = []
    green.append(np.array([0,76,0]))
    green.append(np.array([91,255,255]))
    red = []
    red.append(np.array([151,59,56]))
    red.append(np.array([179,255,255]))
    apple_mask = cv2.inRange(frame,green[0],green[1])
    nodes_mask = cv2.inRange(frame,red[0],red[1])
    if frame is not None:
        apple_mask = cv2.inRange(frame,green[0],green[1])
        nodes_mask = cv2.inRange(frame,red[0],red[1])
        cv2.imshow("Teste", nodes_mask)
        g_contours, _ = cv2.findContours(apple_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        g_contours = sorted(g_contours, key=cv2.contourArea, reverse=True)
       
        r.append(mass_center(g_contours[0],10,9999999))
        r_contours, _ = cv2.findContours(nodes_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        r_contours = sorted(r_contours, key=cv2.contourArea, reverse=True)
        if len(r_contours)>0:
            r0=mass_center(r_contours[0],2,999999)
        else:
             r0=['ERRO','ERRO']
        if len(r_contours)>1:
            r1=mass_center(r_contours[1],2,999999)
        else:
             r1=['ERRO','ERRO']
        if r0[0] != 'ERRO':
             if r1[0] != 'ERRO':
                  r.append(ga.norma(ga.diferenca(r0,r1)))
             else:
                  r.append(-1)
             H = ga.diferenca(r[maca],r0)
             r.append(ga.norma(H))
             r.append(np.arctan2(H[0],H[1]))
        else:
             r.append(-1) ##r0
             r.append(-1) ##r1
             r.append(-4) ##theta 

    return r
### return [frame,[x_px,y_px],l_entre_nós,l_cm,theta]

def convert(data, size):
    print('tell me video fps')
    fps = int(input())
    print('size of the string (node to node in cm)')
    corda = float(input())
    l_n2n = [0,0]
    l_full = [0,0]
    center_i = 0
    for i in range(size):
         data[i][0] = data[i][0]/fps

         if data[i][1][1] > data[center_i][1][1]:
              center_i = i

         if data[i][3] != -1:
              l_full[0]+=data[i][3]
              l_full[1]+=1
              if data[i][2] != -1:
                   l_n2n[0]+=data[1][2]
                   l_n2n[1]+=1

         print(data[i][4])

    l_n2n = l_n2n[0]/l_n2n[1]
    l_full = l_full[0]/l_full[1]

    cm_per_px = corda/l_n2n

    centro = data[center_i][1]

    for i in range(size):
         data[i][1] = ga.diferenca(data[i][1],centro)
         data[i][1] = ga.produto_escalar(cm_per_px,data[i][1])

         data[i][2] = corda

         data[i][3] = l_full * cm_per_px

         print(data[i])

def getOHS(data,size):
     A = 0
     for i in range(size):
          if abs(data[i][4])>A:
               A=abs(data[i][4])
     constFase = np.arccos(data[i][4]/A)
     freqAng = np.sqrt(9.79/data[0][3]) 
     for i in range(1000*1000):
        if abs(abs(data[60][4]/(A*np.cos(freqAng*data[60][0]+constFase)))-abs(np.power(2.72,-data[60][0]*i*0.001))) < 0.1:
             b=i*0.001

     if b is None:
          b='nan'
     print('')
     print('ang = A*e^(-bt)*cos(wt+c)')
     print('ang = '+str(A)+'(e^(-'+str(b)+'t))cos('+str(freqAng)+'t+'+str(constFase)+')')
         

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print('write the path of the pendulum mp4 file:')
vid = cv2.VideoCapture(str(input()))

curr_frame = 0

pixel_data = []

while(True):
    success, frame=vid.read()
    ##cv2.imshow("Output",frame)
    if(frame is not None):
        ##cv2.imwrite(BASE_DIR+'/frames/'+str(curr_frame)+'.jpg',frame)
        aux = extract_pixel_data(curr_frame,frame)
        pixel_data.append(aux)
        ##print(aux)
    else:
         break
    curr_frame+=1
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break



cv2.destroyAllWindows

convert(pixel_data,len(pixel_data))
getOHS(pixel_data,len(pixel_data))






