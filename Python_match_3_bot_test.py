import cv2 as cv
import numpy as np
#from matplotlib import pyplot as plt
import pyautogui
import time #sleep()
cols = 8
rows = 8
MyFilename = "./screenshots/dupa solo.png"

BlockIDsPreference = [5,3,2,4,1,7,8]

debug = False



mainArray = []
for i in range(rows):
  row = []
  for j in range(cols):
    row.append(0)
  mainArray.append(row)

def printMainArray():
    for i in range(rows):
        print(mainArray[i])

def getGridLocation():

    gridX1 = input("X of top left corner ")
    gridY1 = input("Y of top left corner ")
    gridX2 = input("X of botton right corner ")
    gridY2 = input("Y of botton right corner ")
    #pos1 = gridX1,gridY1
    #pos2 = gridX2,gridY2
    return int(gridX1),int(gridY1),int(gridX2),int(gridY2)

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def find_all_occurences_into_mainArray(filename,id,color=(0,0,255)):
    #assume template is smaller than single "block"/rectangle with desired object
    #modifies given image
    FullGridImage = FullGridImageOriginal #given this image  | full grid

    global dim
    dim = FullGridImage.shape
    img_gray = cv.cvtColor(FullGridImage, cv.COLOR_BGR2GRAY)

    cellW = dim[0]//rows
    cellH = dim[1]//cols
    tempArrayW=[]
    tempArrayH=[]
    for i in range(cols):
        tempArrayW.append( (cellW * i) + (cellW//2) )
    for j in range(rows):
         tempArrayH.append( (cellH * j) + (cellH//2) )

    template = cv.imread(filename,0) #find this
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    threshold = 0.80 #threshold
    loc = np.where( res >= threshold)
    if(debug):
        print(tempArrayW)
        print(tempArrayH)
    for pt in zip(*loc[::-1]):
        if(debug):
            cv.rectangle(FullGridImage, pt, (pt[0] + w, pt[1] + h), color, 2)
            cv.rectangle(FullGridImage, ((pt[0] + w//2)-1, (pt[1] + h//2)-1), ((pt[0] + w//2)+1, (pt[1] + h//2)+1), color, 2)
        #pt is top left point eg.(106, 5)
        #print(pt)
        #print((pt[0] + w//2, pt[1] + h//2)) #print "center" of found
        nearestW = find_nearest(tempArrayW,(pt[0] + w//2))
        nearestH = find_nearest(tempArrayH,(pt[1] + h//2))
        if(debug):
            print(pt[0] + w//2 , pt[1] + h//2, "    |   ",nearestW,nearestH,"   ",id)
        mainArray[nearestH][nearestW]=id #what is it
    if(debug):
        cv.imwrite('./screenshots/ress.png',FullGridImage)
#print(tempArrayW)

def check5moves(x,y):
    myBlock = mainArray[y][x]
    
    #check 1 
    # --X-- \/
    # OO-OO
    if(y+1<=rows-1 and x-2>=0 and x+2<=cols-1):
        if(mainArray[y+1][x-2] == mainArray[y+1][x-1] == mainArray[y+1][x+1] == mainArray[y+1][x+2] == myBlock):
            print("legal 5 move down")
            LegalMoves.append((x,y,"down",5,myBlock))
    
    #check 2 
    # OO-OO /\
    # --X--
    if(y-1>=0 and x-2>=0 and x+2<=cols-1):
        if(mainArray[y-1][x-2] == mainArray[y-1][x-1] == mainArray[y-1][x+1] == mainArray[y-1][x+2] == myBlock):
            print("legal 5 move up")
            LegalMoves.append((x,y,"up",5,myBlock))
    
    #check 3 
    # O---- <
    # O----
    # -X---
    # O----
    # O----
    if(x-1>=0 and y-2>=0 and y+2<=rows-1):
        if(mainArray[y-1][x-1] == mainArray[y-2][x-1] == mainArray[y+1][x-1] == mainArray[y+2][x-1] == myBlock):
            print("legal 5 move left")
            LegalMoves.append((x,y,"left",5,myBlock))

    
    #check 4 
    # -O-- >
    # -O--
    # X---
    # -O--
    # -O--
    if(x+1<=cols-1 and y-2>=0 and y+2<=rows-1):
        if(mainArray[y-1][x+1] == mainArray[y-2][x+1] == mainArray[y+1][x+1] == mainArray[y+2][x+1] == myBlock):
            print("legal 5 move right")
            LegalMoves.append((x,y,"right",5,myBlock))

def check4moves(x,y):
    myBlock = mainArray[y][x]
    
    #check 1 
    # --X- \/
    # OO-O
    if(y+1<=rows-1 and x-2>=0 and x+1<=cols-1):
        if(mainArray[y+1][x-2] == mainArray[y+1][x-1] == mainArray[y+1][x+1] == myBlock):
            print("legal 4 move down (left)")
            LegalMoves.append((x,y,"down",4,myBlock))
    #check 2 
    # -X-- \/
    # O-OO
    if(y+1<=rows-1 and x-1>=0 and x+2<=cols-1):
        if(mainArray[y+1][x-1] == mainArray[y+1][x+1] == mainArray[y+1][x+2] == myBlock):
            print("legal 4 move down (right)")
            LegalMoves.append((x,y,"down",4,myBlock))
    
    #check 3
    # OO-O /\
    # --X-
    if(y-1>=0 and x-2>=0 and x+1<=cols-1):
        if(mainArray[y-1][x-2] == mainArray[y-1][x-1] == mainArray[y-1][x+1] == myBlock):
            print("legal 4 move up (left)")
            LegalMoves.append((x,y,"up",4,myBlock))
    #check 4
    # O-OO /\
    # -X--
    if(y-1>=0 and x-1>=0 and x+2<=cols-1):
        if(mainArray[y-1][x-1] == mainArray[y-1][x+1] == mainArray[y-1][x+2] == myBlock):
            print("legal 4 move up (right)")
            LegalMoves.append((x,y,"up",4,myBlock))
    
    #check 5 
    # O---- <
    # -X---
    # O----
    # O----
    if(x-1>=0 and y-1>=0 and y+2<=rows-1):
        if(mainArray[y-1][x-1] == mainArray[y+1][x-1] == mainArray[y+2][x-1]== myBlock):
            print("legal 4 move left (down)")
            LegalMoves.append((x,y,"left",4,myBlock))
    #check 6 
    # O---- <
    # O----
    # -X---
    # O----
    if(x-1>=0 and y-2>=0 and y+1<=rows-1):
        if(mainArray[y-1][x-1] == mainArray[y-2][x-1] == mainArray[y+1][x-1]== myBlock):
            print("legal 4 move left (up)")
            LegalMoves.append((x,y,"left",4,myBlock))

    #check 7 
    # -O-- >
    # -O--
    # X---
    # -O--
    if(x+1<=cols-1 and y-2>=0 and y+1<=rows-1):
        if(mainArray[y-1][x+1] == mainArray[y-2][x+1] == mainArray[y+1][x+1]== myBlock):
            print("legal 4 move right (up)")
            LegalMoves.append((x,y,"right",4,myBlock))
    #check 8 
    # -O-- >
    # X---
    # -O--
    # -O--
    if(x+1<=cols-1 and y-1>=0 and y+2<=rows-1):
        if(mainArray[y-1][x+1] == mainArray[y+2][x+1] == mainArray[y+1][x+1]== myBlock):
            print("legal 4 move right (down)")
            LegalMoves.append((x,y,"right",4,myBlock))

def check3moves(x,y):
    myBlock = mainArray[y][x]
    
    #check 1
    # O-O /\
    # -X-
    if(y-1>=0 and x-1>=0 and x+1<=cols-1):
        if(mainArray[y-1][x-1] == mainArray[y-1][x+1] == myBlock):
            print("legal 3 move up")
            LegalMoves.append((x,y,"up",3,myBlock))

    #check 2
    # -X- \/
    # O-O
    if(y+1<=rows-1 and x-1>=0 and x+1<=cols-1):
        if(mainArray[y+1][x-1] == mainArray[y+1][x+1] == myBlock):
            print("legal 3 move down")
            LegalMoves.append((x,y,"down",3,myBlock))
            
    #check 3
    # O- <
    # -X
    # O-
    if(y+1<=rows-1 and y-1>=0 and x-1>=0):
        if(mainArray[y+1][x-1] == mainArray[y-1][x-1] == myBlock):
            print("legal 3 move left")
            LegalMoves.append((x,y,"left",3,myBlock))
    #check 4
    # -O >
    # X-
    # -O
    if(y+1<=rows-1 and y-1>=0 and x+1<cols-1):
        if(mainArray[y+1][x+1] == mainArray[y-1][x+1] == myBlock):
            print("legal 3 move right")
            LegalMoves.append((x,y,"right",3,myBlock))
    
    #check 5
    # O /\
    # O
    # -
    # X
    if(y-3>=0):
        if(mainArray[y-1][x] == mainArray[y-2][x] == myBlock):
            print("legal 3 move up (double)")
            LegalMoves.append((x,y,"up",3,myBlock))

    #check 6
    # X \/
    # -
    # O
    # O
    if(y+3<=rows-1):
        if(mainArray[y+2][x] == mainArray[y+3][x] == myBlock):
            print("legal 3 move down (double)")
            LegalMoves.append((x,y,"down",3,myBlock))

    #check 7
    # X-OO >
    if(x+3<=cols-1):
        if(mainArray[y][x+2] == mainArray[y][x+3] == myBlock):
            print("legal 3 move right (double)")
            LegalMoves.append((x,y,"right",3,myBlock))
    #check 8
    # OO-X <
    if(x-3>=0):
        if(mainArray[y][x-2] == mainArray[y][x-3] == myBlock):
            print("legal 3 move left (double)")
            LegalMoves.append((x,y,"left",3,myBlock))

    #check 9
    # X-- \/
    # -OO 
    if(y+1<=rows-1 and x+2<=cols-1):
        if(mainArray[y+1][x+1] == mainArray[y+1][x+2] == myBlock):
            print("legal 3 move down (double)(right)")
            LegalMoves.append((x,y,"down",3,myBlock))
    #check 10
    # --X \/
    # OO- 
    if(y+1<=rows-1 and x-2>=0):
        if(mainArray[y+1][x-1] == mainArray[y+1][x-2] == myBlock):
            print("legal 3 move down (double)(left)")
            LegalMoves.append((x,y,"down",3,myBlock))

    #check 11
    # OO- /\
    # --X 
    if(y-1>=0 and x-2>=0):
        if(mainArray[y-1][x-1] == mainArray[y-1][x-2] == myBlock):
            print("legal 3 move up (double)(left)")
            LegalMoves.append((x,y,"up",3,myBlock))
            
    #check 12
    # -OO /\
    # X-- 
    if(y-1>=0 and x+2<=cols-1):
        if(mainArray[y-1][x+1] == mainArray[y-1][x+2] == myBlock):
            print("legal 3 move up (double)(right)")
            LegalMoves.append((x,y,"up",3,myBlock))

    #check 13
    # X- >
    # -O 
    # -O
    if(y+2<=rows-1 and x+1<=cols-1):
        if(mainArray[y+1][x+1] == mainArray[y+2][x+1] == myBlock):
            print("legal 3 move right (double)(down)")
            LegalMoves.append((x,y,"right",3,myBlock))

    #check 14
    # -O >
    # -O 
    # X-
    if(y-2>=0 and x+1<=cols-1):
        if(mainArray[y-2][x+1] == mainArray[y-1][x+1] == myBlock):
            print("legal 3 move right (double)(up)")
            LegalMoves.append((x,y,"right",3,myBlock))

    #check 15
    # -X <
    # O- 
    # O-
    if(y+2<=rows-1 and x-1>=0):
        if(mainArray[y+2][x-1] == mainArray[y+1][x-1] == myBlock):
            print("legal 3 move left (double)(down)")
            LegalMoves.append((x,y,"left",3,myBlock))

    #check 16
    # O- <
    # O- 
    # -X
    if(y-2>=0 and x-1>=0):
        if(mainArray[y-2][x-1] == mainArray[y-1][x-1] == myBlock):
            print("legal 3 move left (double)(up)")
            LegalMoves.append((x,y,"left",3,myBlock))

def searchMoves():
    x = 0
    y = 0
    for y in range(rows):
        for x in range(cols):
            print(x,y)
            check5moves(x,y)
            check4moves(x,y)
            check3moves(x,y)

def gridScreenshot(filename,gridX1,gridY1,gridX2,gridY2):
    
    width = gridX2 - gridX1
    height = gridY2 - gridY1

    final = gridX1,gridY1,width,height
    im = pyautogui.screenshot(region=(final))
    return im
    #im.save(filename)

def chooseBestMove(order):
    for y in order:
        for x in LegalMoves:
            if(x[3]==5 and x[4]==y):
                #print(x)
                return x
    for y in order:
        for x in LegalMoves:
            if(x[3]==4 and x[4]==y):
                #print(x)
                return x
    for y in order:
        for x in LegalMoves:
            if(x[4]==y):
                #print(x)
                return x

def makeMove(move,x1,y1):
    x = move[0]
    y = move[1]
    dir = move[2]

    #copied bullshit
    #dim is global
    cellW = dim[0]//rows
    cellH = dim[1]//cols
    centerPointW=[]
    centerPointH=[]
    for i in range(cols):
        centerPointW.append( (cellW * i) + (cellW//2) )
    for j in range(rows):
         centerPointH.append( (cellH * j) + (cellH//2) )

    print("dupa")
    #print(centerPointW)
    #print(centerPointH)
    pyautogui.moveTo(centerPointW[x]+x1,centerPointH[y]+y1)
    if(dir == 'down'):
        pyautogui.dragTo(centerPointW[x]+x1,centerPointH[y+1]+y1,0.3, button='left')
    if(dir == 'up'):
        pyautogui.dragTo(centerPointW[x]+x1,centerPointH[y-1]+y1,0.3, button='left')
    if(dir == 'left'):
        pyautogui.dragTo(centerPointW[x-1]+x1,centerPointH[y]+y1,0.3, button='left')
    if(dir == 'right'):
        pyautogui.dragTo(centerPointW[x+1]+x1,centerPointH[y]+y1,0.3, button='left')

def main():
    gridX1,gridY1,gridX2,gridY2 = getGridLocation()
    while True:
        gridImage = gridScreenshot(MyFilename,gridX1,gridY1,gridX2,gridY2)
        global FullGridImageOriginal
        #FullGridImageOriginal = cv.imread(MyFilename)
        #FullGridImageOriginal = cv.imread('./screenshots/dupa solo.png')
        FullGridImageOriginal = cv.cvtColor(np.array(gridImage), cv.COLOR_RGB2BGR)

        global LegalMoves # x,y,"move",howBig,BlockID
        LegalMoves = []


    
        find_all_occurences_into_mainArray('./screenshots/1.png',1,(0,0,255))
        find_all_occurences_into_mainArray('./screenshots/2.png',2,(0,255,0))
        find_all_occurences_into_mainArray('./screenshots/3.png',3,(255,0,255))
        find_all_occurences_into_mainArray('./screenshots/4.png',4,(255,0,0))
        find_all_occurences_into_mainArray('./screenshots/5.png',5,(255,0,0))
        find_all_occurences_into_mainArray('./screenshots/6.png',5,(255,0,0))
        find_all_occurences_into_mainArray('./screenshots/7.png',7,(255,0,0))
        find_all_occurences_into_mainArray('./screenshots/8.png',8,(255,0,0))

        searchMoves()
        print('---------')
        Move = chooseBestMove(BlockIDsPreference)
        print(Move)
        makeMove(Move,gridX1,gridY1)
        #input("Press Enter to continue...")
        LegalMoves.clear()
        time.sleep(7)

if __name__ == "__main__":
    main()