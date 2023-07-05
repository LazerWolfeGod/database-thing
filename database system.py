import pygame,math,random,sys,os
import PyUI as pyui
pygame.init()
screenw = 800
screenh = 600
screen = pygame.display.set_mode((screenw, screenh),pygame.RESIZABLE)
pygame.scrap.init()
ui = pyui.UI()
done = False
clock = pygame.time.Clock()
ui.defaultcol = (50,120,150)
ui.defaulttextcol = (220,220,240)

class funcmn:
    def __init__(self,param,main):
        self.func = lambda: main.moredetailmenu(param)
class funcem:
    def __init__(self,param,main):
        self.func = lambda: main.editmenu(param)

def completedata(data):
    allitems = ['Forename','Surname','Pronouns','Title','Birth Date','Address','Postcode','Home Telephone','Work Telephone','Mobile Number',
                'Email','Driving License','Owns Vehicle','Interested in volunteer driving','Days can work','Hours available per day',
                'Times unable to complete work','Disability?','Emergency Contacts','Special Needs','Date Started','Active','Staff','ID']
    processed = {}
    for a in allitems:
        if not(a in data):
            if a == 'ID':
                processed[a] = -1
            else:
                processed[a] = ''
        else:
            processed[a] = data[a]
    return processed

class ITEM:
    def __init__(self,data):
        self.data = data
        self.menu = 'info'+str(self.data['ID'])
        self.makegui()
    def makegui(self):
        ## main
        ui.maketext(10,10,'Data for '+self.data['Forename'],80,self.menu,self.menu+'title',backingcol=(63,64,75),scalesize=False,layer=3)
        ui.makebutton(0,0,'back',40,ui.menuback,self.menu,ID=self.menu+'back',anchor=('w-10',10),objanchor=('w',0),roundedcorners=4,scalesize=False,layer=3)
        ui.makerect(0,0,screenw,80,menu=self.menu,layer=2,scalesize=False,col=(63,64,75),ID=self.menu+'rect')
        ui.maketable(0,0,[],[ui.maketext(0,0,'Item',45,self.menu,roundedcorners=4,col=(83,84,100),textcenter=True),
                             ui.maketext(0,0,'Info',45,self.menu,roundedcorners=4,col=(83,84,100),textcenter=True),
                             ui.maketext(0,0,'Edit',45,self.menu,roundedcorners=4,col=(83,84,100),textcenter=True)],self.menu,self.menu+'table',roundedcorners=4,textcenter=False,verticalspacing=4,textsize=30,boxwidth=[200,200,100],anchor=(10,80),col=(63,64,75),scalesize=False,scalex=False,scaley=False)
        ui.makescroller(0,0,screenh-80,self.slidetable,pageheight=screenh-80,anchor=('w',80),objanchor=('w',0),scalesize=False,menu=self.menu,ID=self.menu+'scroller',runcommandat=1,layer=0)
        self.refreshtable()

        ## edit menu
        ui.makewindowedmenu(10,10,400,140,self.menu+'edit',self.menu,(63,64,75),roundedcorners=8,scalesize=False,scalex=False,scaley=False,ID=self.menu+'window')
        ui.maketable(5,5,[['Item',ui.maketextbox(0,0,'',200,2,self.menu+'edit',roundedcorners=4,height=80,textsize=30,verticalspacing=4)]],menu=self.menu+'edit',roundedcorners=4,boxwidth=[184,200],boxheight=80,textsize=35,scalesize=False,scalex=False,scaley=False,col=(63,64,75),ID=self.menu+'editbox')
        ui.makebutton(200,115,'Save',40,self.saveedited,self.menu+'edit',scalesize=False,scalex=False,scaley=False,roundedcorners=10,verticalspacing=3,center=True,ID=self.menu+'save')
    def refreshtable(self):
        ui.IDs[self.menu+'table'].wipe(ui,False)
        data = []
        for a in self.data:
            if a == 'ID':
                obj = ''
            else:
                func = funcem(a,self)
                obj = ui.makebutton(0,0,'{dots}',30,func.func,roundedcorners=4,clickdownsize=2)
            data.append([str(a),str(self.data[a]),obj])
        ui.IDs[self.menu+'table'].data = data
        sc = ui.IDs[self.menu+'scroller']
        if (sc.maxp-sc.minp)>sc.pageheight: ui.IDs[self.menu+'table'].boxwidth = [(screenw-126-15)/2,(screenw-126-15)/2,100]
        else: ui.IDs[self.menu+'table'].boxwidth = [(screenw-126)/2,(screenw-126)/2,100]
        ui.IDs[self.menu+'table'].refresh(ui)
        self.slidetable()
        self.reshiftgui()
    def slidetable(self):
        ui.IDs[self.menu+'table'].y = 80-ui.IDs[self.menu+'scroller'].scroll
        ui.IDs[self.menu+'table'].refreshcords(ui)
    def reshiftgui(self):
        ui.IDs[self.menu+'rect'].width = screenw
        ui.IDs[self.menu+'scroller'].scroll = 0
        ui.IDs[self.menu+'scroller'].height = screenh-80
        ui.IDs[self.menu+'scroller'].pageheight = screenh-80
        ui.IDs[self.menu+'scroller'].maxp = ui.IDs[self.menu+'table'].height
        ui.IDs[self.menu+'scroller'].refresh(ui)
        if self.menu+'window' in ui.IDs:
            ui.IDs[self.menu+'editbox'].boxwidth = [184,screenw-36-184]
            ui.IDs[self.menu+'window'].width = screenw-10
    def editmenu(self,item):
        self.selected = item
        ui.IDs[self.menu+'editbox'].wipe(ui,True)
        ui.IDs[self.menu+'editbox'].data = [[item,ui.maketextbox(0,0,str(self.data[item]),200,2,self.menu+'edit',roundedcorners=4,height=80,textsize=30,verticalspacing=4,command=self.saveedited,commandifenter=True)]]
        ui.IDs[self.menu+'editbox'].refresh(ui)
        ui.IDs[self.menu+'editbox'].refreshcords(ui)
        ui.IDs[self.menu+'table'].refreshcords(ui)
        ui.IDs[self.menu+'editbox'].tableimages[0][1][1].selected = True
        ui.selectedtextbox = ui.textboxes.index(ui.IDs[self.menu+'editbox'].tableimages[0][1][1])
        ui.movemenu(self.menu+'edit','down')
    def saveedited(self):
        self.data[self.selected] = ui.IDs[self.menu+'editbox'].data[0][1].text
        self.refreshtable()
        ui.menuback()
    def wipe(self):
        items = ['title','back','table','scroller','editbox','save','rect']
        for a in items:
             ui.delete(self.menu+a,False)

class MAIN:
    def __init__(self):
        self.data = [{'Surname':'Harris','Forename':'Christian','ID':2},{'Surname':'Winslow','Forename':'Ryan','ID':1}]
        for a in range(len(self.data)):
            self.data[a] = completedata(self.data[a])
        self.data.sort(key=lambda x: x['ID'])

        self.menus = []
        self.generatemenus()
        self.makegui()
    def makegui(self):
        ## title screen
        ui.maketext(0,0,'',250,anchor=('w/2','h/4'),objanchor=('w/2','h/2'),img=pygame.image.load(pyui.resourcepath('make it happen.png')),colorkey=(251,251,251))
        ui.makebutton(0,0,'Users',50,lambda: ui.movemenu('table','up'),roundedcorners=10,clickdownsize=2,verticalspacing=4,anchor=('w/2','h/2'),objanchor=('w/2',0))
        ui.makebutton(0,60,'Add User',50,self.adduser,anchor=('w/2','h/2'),objanchor=('w/2',0),roundedcorners=10,verticalspacing=4,clickdownsize=2,scalex=False,scaley=False)
        
        
        ## main table
        ui.maketable(0,0,[],['ID','Name','More'],anchor=(10,60),boxwidth=[100,300,100],verticalspacing=5,textsize=30,roundedcorners=4,col=(63,65,75),ID='main table',menu='table',scalesize=False)
        self.refreshtable()

        ui.maketextbox(10,10,'',(screenw-20)/2,menu='table',commandifenter=True,height=40,scalesize=False,textsize=23)

        ## add user menu
        self.empty = completedata({})
        self.shiftingitems = []
        yinc = 100
        self.checkboxes = {'Pronouns':['She/Her','He/Him','They/Them','textbox'],'Driving license':['Yes','No'],'Owns Vehicle':['Yes','No'],'Interested in volunteer driving':['Yes','No'],'Disability?':['Yes','No'],'Staff':['Yes','No']}
        for i,a in enumerate(self.empty):
            if a != 'ID':
                ui.maketext(30,yinc,a,35,'add user',ID='add user'+a,maxwidth=200)
                h = ui.IDs['add user'+a].height
                if a in self.checkboxes:
                    xinc = 240
                    disper = 540/len(self.checkboxes[a])
                    exclusive = ['add user checkbox'+a+'*'+b for b in self.checkboxes[a] if b!='textbox']
                    for b in self.checkboxes[a]:
                        if b != 'textbox':
                            ui.maketext(xinc,yinc+h/2,b,30,'add user',ID='add user'+a+'*'+b,objanchor=(0,'h/2'))
                            xinc+=ui.IDs['add user'+a+'*'+b].width+10
                            ui.makecheckbox(xinc,yinc+h/2,40,menu='add user',ID='add user checkbox'+a+'*'+b,objanchor=(0,'h/2'),spacing=-8,clickdownsize=2,toggle=False,bindtoggle=exclusive)
                            if a == 'Pronouns': xinc+=ui.IDs['add user checkbox'+a+'*'+b].width+10
                            else: xinc+=ui.IDs['add user checkbox'+a+'*'+b].width+40
                            ui.IDs['add user checkbox'+a+'*'+b].storeddata = b
                            self.shiftingitems.append('add user'+a+'*'+b)
                            self.shiftingitems.append('add user checkbox'+a+'*'+b)
                        else:
                            ui.maketextbox(xinc,yinc,'',133,height=h,menu='add user',ID='add user inp'+a+'*'+b,textsize=32)
                            self.shiftingitems.append('add user inp'+a+'*'+b)
                else:
                    ui.maketextbox(240,yinc,'',540,height=h,menu='add user',ID='add user inp'+a,textsize=32,spacing=1)
                    self.shiftingitems.append('add user inp'+a)
                self.shiftingitems.append('add user'+a)
                yinc+=h+15
        ui.makescroller(0,100,screenh-100,self.shiftaddmenu,maxp=yinc,pageheight=screenh,anchor=('w',0),objanchor=('w',0),ID='add menu scroller',menu='add user',runcommandat=1,scalesize=False)
        ui.maketext(20,45,'New User',70,'add user',textcol=(240,240,240),layer=3,backingcol=(83,86,100),centery=True)
        ui.makerect(0,86,screenw,4,menu='add user',layer=2,col=(80,150,160))
        ui.makerect(0,0,screenw,86,menu='add user',layer=2,col=(83,86,100))
        ui.makebutton(280,43,'Clear',50,self.clearuser,'add user',layer=3,roundedcorners=6,centery=True,clickdownsize=2,textoffsety=1)
        ui.makebutton(430,43,'Save',50,self.saveuser,'add user',layer=3,roundedcorners=6,centery=True,clickdownsize=2,textoffsety=1)
        
    def generatemenus(self):
        for a in self.menus:
            a.wipe()
        self.menus = []
        for a in self.data:
            self.menus.append(ITEM(a))
            
    def refreshtable(self):
        ui.IDs['main table'].wipe(ui,False)
        data = []
        for a in range(len(self.data)):
            func = funcmn(self.data[a]['ID'],self)
            obj = ui.makebutton(0,0,'{dots}',30,func.func,roundedcorners=4,clickdownsize=2)
            data.append([self.data[a]['ID'],self.data[a]['Forename']+' '+self.data[a]['Surname'],obj])
        ui.IDs['main table'].boxwidth = [100,(screenw-8-20-200),100]
        ui.IDs['main table'].data = data
        ui.IDs['main table'].refresh(ui)
    def moredetailmenu(self,ID):
        self.menuin = ID-1
        self.menus[self.menuin].reshiftgui()
        self.menus[self.menuin].refreshtable()
        ui.movemenu('info'+str(ID),'left')
    def adduser(self):
        ui.movemenu('add user','up')
    def clearuser(self):
        for a in self.shiftingitems:
            if type(ui.IDs[a]) == pyui.TEXTBOX:
                ui.IDs[a].text = ''
                ui.IDs[a].refresh(ui)
            elif type(ui.IDs[a]) == pyui.BUTTON:
                ui.IDs[a].toggle = False
    def saveuser(self):
        data = {'ID':len(self.data)+1}
        empty = completedata({})
        for a in self.shiftingitems:
            if type(ui.IDs[a]) == pyui.TEXTBOX:
                temp = a.removeprefix('add user inp')
                if '*' in temp:
                    data[temp.split('*')[0]] = ui.IDs[a].text
                elif temp in list(empty):
                    data[temp] = ui.IDs[a].text
        for a in self.shiftingitems:
            if type(ui.IDs[a]) == pyui.BUTTON:
                temp = a.removeprefix('add user checkbox')
                items = temp.split('*')
                if ui.IDs[a].toggle:
                    data[items[0]] = ui.IDs[a].storeddata
                
                
                
        self.data.append(completedata(data))
        self.refreshtable()
        self.menus.append(ITEM(completedata(data)))
                    
    def shiftaddmenu(self):
        for a in self.shiftingitems:
            ui.IDs[a].y = ui.IDs[a].starty-ui.IDs[a].objanchor[1]-ui.IDs['add menu scroller'].scroll
            ui.IDs[a].refreshcords(ui)
    def reshiftgui(self):
        ui.IDs['main table'].boxwidth = [100,(screenw-8-20-200),100]
        ui.IDs['main table'].refresh(ui)
        ui.IDs['add menu scroller'].height = screenh-100
        ui.IDs['add menu scroller'].pageheight = screenh/ui.scale
        ui.IDs['add menu scroller'].refresh(ui)
        
main = MAIN()


while not done:
    pygameeventget = ui.loadtickdata()
    for event in pygameeventget:
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.VIDEORESIZE:
            screenw = event.w
            screenh = event.h
            main.reshiftgui()
            if 'info' in ui.activemenu:
                main.menus[main.menuin].reshiftgui()
                main.menus[main.menuin].refreshtable()
    screen.fill((63,65,75))
    
    ui.rendergui(screen)
    pygame.display.flip()
    clock.tick(60)                                               
pygame.quit() 
