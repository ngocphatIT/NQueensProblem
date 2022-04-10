import pygame
from simulated_annealing import *
pygame.init()
class Button:
    def __init__(self,**kwargs):
        self.bg1=kwargs['bg1']
        self.fg1=kwargs['fg1']
        self.font=kwargs['font']
        self.text=kwargs['text']
        self.sizex=kwargs['sizex']
        self.sizey=kwargs['sizey']
        self.bg2=kwargs['bg2']
        self.fg2=kwargs['fg2']
        self.time=pygame.time.get_ticks()
        self.cooldown=500
    def show(self,surface,x,y):
        pygame.draw.rect(surface,self.bg1,(x,y,self.sizex,self.sizey))
        text=pygame.font.SysFont(self.font[0],self.font[1]).render(self.text,True,self.fg1)
        rectT=text.get_rect()
        rectT.center=(x+self.sizex//2,y+self.sizey//2)
        surface.blit(text,rectT)
        if pygame.mouse.get_pos()[0]>=x and pygame.mouse.get_pos()[1]<=y+self.sizey and pygame.mouse.get_pos()[0]<=x+self.sizex and pygame.mouse.get_pos()[1]>=y:
            pygame.draw.rect(surface,self.bg2,(x,y,self.sizex,self.sizey))
            text=pygame.font.SysFont(self.font[0],self.font[1]).render(self.text,True,self.fg2)
            rectT=text.get_rect()
            rectT.center=(x+self.sizex//2,y+self.sizey//2)
            surface.blit(text,rectT)
            if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks()-self.time>self.cooldown:
                self.time=pygame.time.get_ticks()
                return True
            else:
                return False
        return False
class MainApp:
    def __init__(self,width=880,height=720):
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption("NQueenProblem")
        self.distancex=100
        self.distancey=50
        self.number=15
        self.size=min(width-self.distancex*2,height-self.distancey*2)//self.number
        self.imgQueen=pygame.transform.scale(pygame.image.load("queen.png"),(self.size,self.size))
        self.problem=NQueensProblem(self.number)
        self.problem.solve()  
        self.btnChangeMode=Button(bg1=(128,128,128),fg1=(255,255,255),font=('Times',20),text='Thủ công',sizex=100,sizey=50,bg2=(0,128,128),fg2=(0,255,255))
        self.btnNextStep=Button(bg1=(128,128,128),fg1=(255,255,255),font=('Times',20),text='Bước kế',sizex=100,sizey=50,bg2=(0,128,128),fg2=(0,255,255))
        self.btnPreStep=Button(bg1=(128,128,128),fg1=(255,255,255),font=('Times',20),text='Quay lại',sizex=100,sizey=50,bg2=(0,128,128),fg2=(0,255,255))
    def run(self,FPS=120):
        clock=pygame.time.Clock()
        self.mode='Thủ công'
        self.index=0
        while True:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.display()
            pygame.display.update()  
    def display(self):
        self.surface.fill((255,255,255))
        if self.btnChangeMode.show(self.surface,750,100):
            if self.btnChangeMode.text=='Tự động':
                self.btnChangeMode.text='Thủ công'
                self.mode='Thủ công'
            else:
                self.btnChangeMode.text='Tự động'
                self.mode='Tự động'
        if self.btnNextStep.show(self.surface,750,200) and self.mode=='Thủ công' and self.index<len(self.problem.history)-1:
            self.index+=1
        if self.btnPreStep.show(self.surface,750,300) and self.mode=='Thủ công' and self.index>0:
            self.index-=1
        if self.index>=len(self.problem.history)-1:
            self.drawBoardChess(self.problem.history[len(self.problem.history)-1])  
            self.btnChangeMode.text='Thủ công'
            self.mode='Thủ công'
        else:
            self.drawBoardChess(data=self.problem.history[self.index])
            if self.mode=="Tự động":
                self.index+=1
    def drawBoardChess(self,data=None):
        index=1
        color_list=[(255,255,255),(255,255,0),(0,0,0)]
        for i in range(self.number):
            for j in range(self.number):
                pygame.draw.rect(self.surface,color_list[index],(self.distancex+self.size*j,self.distancey+self.size*i,self.size,self.size))
                index*=-1
            if self.number%2==0:
                index*=-1
        for index,q in enumerate(data):
            self.surface.blit(self.imgQueen,(self.distancex+self.size*q,self.distancey+self.size*index))         
if __name__ == '__main__':
    MainApp().run()