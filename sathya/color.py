import time

class Block:
    def __init__(self,coor,color):
        self.x = color[0]
        self.y = 0
        self.color = color
        self.visible = True
        pass
    def move(self, parameter_list):
        self.y += 5
        pass
    def blast(self):
        self.visible = False
        pass

class data:
    def __init__(self,file):
        self.blocks = []
        self.colors = {
        (0,100):(0,0,255),
        (75,125):(0,255,0),
        (100,200):(255,0,0),
        (175,225):(122,122,122),
        (200,300):(150,240,255),
        (300,400):(100,240,255),
        (375,425):(120,200,255),
        (400,500):(200,140,200),
        (475,525):(190,200,100),
        (500,600):(250,200,100),
        (575,625):(130,0,170),
        (600,700):(100,170,255),
        (700,800):(60,255,0),
        (775,825):(100,255,0),
        (800,900):(255,0,255),
        (875,925):(70,255,180),
        (900,1000):(240,100,255),
        (1000,1100):(200,200,30)
    }
    pass

Data = data("")
clock = time.time()

def colorplay(data):

    if len(data.blocks)==0:
        print("good job")
    else:
        color = colors[listPlay[-1]]
        cv2.rectangle(img,(listPlay[-1][0],350),(listPlay[-1][1],400),color,thickness=cv2.FILLED)
        if len(coordinates)==0:
            print("start playing")
        elif coordinates[-1] == listPlay[-1]:
            print("Last coordinate:" + str(coordinates[-1]))
            print("Last listPlay:" + str(listPlay[-1]))
            listPlay.pop()
        else:
            print("Last coordinate:" + str(coordinates[-1]))
            print("Last listPlay:" + str(listPlay[-1]))
        print(listPlay)