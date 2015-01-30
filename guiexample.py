import Tkinter
from Tkinter import Tk, BOTH, Label
from ttk import Frame, Button, Style
from PIL import Image, ImageTk
import zmqreply
import pygame
import threading
import musicplayer
import time
import commander
import db_connector

class Example(Frame):
  
    def __init__(self, parent, queue, musicplayer, endCommand):
        Frame.__init__(self, parent)   
        self.parent = parent
        self.weight = 500
        self.height = 400
        self.queue = queue
        self.musicplayer = musicplayer
        self.endCommand = endCommand
        self.pictures = ["hd_1.jpg", "hd_2.jpg", "hd_3.jpg", "hd_4.jpg", "hd_5.jpg"];
        self.centerWindow()
        self.initUI()
        self.commander = commander.Commander()
        self.db_con = db_connector.DBconnector()
        '''
        self.showPic = 1
        self.playSlides()
        '''
    
    def initUI(self):
        self.parent.title("Example")
        self.pack(fill=BOTH, expand = 1)

        self.style = Style()
        self.style.theme_use("default")

        frame = Frame(self, relief=Tkinter.RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=1)
     
        okButton = Button(self, text = "OK")
        okButton.place(x = self.width - 300, y = self.height - 200)

        quitButton = Button(self.parent, text = "QUIT", command = self.endCommand)
        quitButton.place(x = self.width - 200, y = self.height - 200)
       
        scale = 0.6
        self.wow_pic = Image.open("hd_1.jpg")
        self.wow_pic = self.wow_pic.resize((int(self.width*scale), int(self.height*scale)))
        self.wow_pic_tk = ImageTk.PhotoImage(self.wow_pic)
        self.label_wow_pic = Label(self, image = self.wow_pic_tk)
        self.label_wow_pic.image = self.wow_pic_tk
        self.label_wow_pic.place(x = 10, y = 10)

        info_x = int(self.width*scale) + 20

        label_text_area = Tkinter.Label(self, text = "Message received:")
        label_text_area.place(x = info_x, y = 10)

        self.text_area = Tkinter.Text(self, height = 10, width = 40)
        self.text_area.place(x = info_x, y = 30)

    def centerWindow(self):      
        self.width = self.parent.winfo_screenwidth()
        self.height = self.parent.winfo_screenheight()
        self.queue.put("Width: " + str(self.width))
        self.queue.put("Height: " + str(self.height))
        self.parent.geometry('%dx%d+%d+%d' % (self.width, self.height, 0, 0))

    def insertText(self, str):
        self.text_area.insert(Tkinter.INSERT, "\n" + str)

    def showPicture(self, img_name):
        self.label_wow_pic.destroy()
        scale = 0.75
        self.wow_pic = Image.open(img_name)
        self.wow_pic = self.wow_pic.resize((int(self.width*scale), int(self.height*scale)))
        self.wow_pic_tk = ImageTk.PhotoImage(self.wow_pic)
        self.label_wow_pic = Label(self, image = self.wow_pic_tk)
        self.label_wow_pic.image = self.wow_pic_tk
        self.label_wow_pic.place(x = 10, y = 10)

    def playMusic(self):
        pygame.mixer.init()
        pygame.mixer.music.load("1.mp3")
        pygame.mixer.music.play()

    def pauseMusic(self):
        pygame.mixer.music.pause()
        '''
        self.musicthread = threading.Thread(target = self.musicplayer.play)
        self.musicthread.start()

        '''
        
    def playSlides(self):
        self.showPic = 1
        self.currentSlideNo = 0;
        self.showSlidesThread = threading.Thread(target = self.playSlidesClock)
        self.showSlidesThread.start()

    def playSlidesClock(self):
        #self.queue.put("next_picture");
        while True:
            if(self.showPic == 0):
                break;
            self.queue.put("next_picture");
            time.sleep(5);
            
    def nextSlide(self):
        self.currentSlideNo = (self.currentSlideNo + 1) % len(self.pictures)
        self.showPicture(self.pictures[self.currentSlideNo])

    def processIncoming(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                print "From queue, get msg:", msg
                if(msg == "show_text"):
                    self.insertText("I need to show a text")
                elif(msg == "show_picture"):
                    self.showPic = 1
                    self.playSlides()
                elif(msg == "play_music"):
                    self.playMusic()
                elif(msg == "pause_music"):
                    self.pauseMusic()
                elif(msg == "next_picture"):
                    self.nextSlide()
                elif(msg == "json_request"):
                    self.insertText("Get JSON request")
                    device = self.queue.get(0)
                    cmd_json = self.queue.get(0)
                    print 'get json', device, cmd_json
                    self.commander.parseCmd(device, cmd_json)
                elif(msg == "get_health_info"):
                    msg = self.queue.get(0)
                    output = self.query(msg)
                    self.insertText(str(output))

                else:
                    self.insertText(msg)
            except:
                pass
