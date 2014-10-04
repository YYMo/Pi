import Tkinter
from Tkinter import Tk, BOTH, Label
from ttk import Frame, Button, Style
from PIL import Image, ImageTk
import zmqreply
import pygame
import threading
import musicplayer

class Example(Frame):
  
    def __init__(self, parent, queue, musicplayer, endCommand):
        Frame.__init__(self, parent)   
        self.parent = parent
        self.weight = 500
        self.height = 400
        self.queue = queue
        self.musicplayer = musicplayer
        self.endCommand = endCommand
        self.initUI()
        self.centerWindow()

    def initUI(self):
        self.parent.title("Example")
        self.pack(fill=BOTH, expand = 1)

        self.style = Style()
        self.style.theme_use("default")

        frame = Frame(self, relief=Tkinter.RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=1)

        self.contentHeight = 250
        padding1 = 20

        label_text_area = Tkinter.Label(self, text = "Message received:")
        label_text_area.place(x = 10, y = self.contentHeight )

        self.text_area = Tkinter.Text(self, height = 10, width = 50)
        self.text_area.place(x = 10, y = self.contentHeight + padding1)
        '''
        okButton = Button(self, text = "OK")
        okButton.place(x = self.weight - 200, y = self.contentHeight + padding1)

        quitButton = Button(self.parent, text = "QUIT", command = self.endCommand)
        quitButton.place(x=self.weight - 100, y = self.contentHeight + padding1)
        '''
        self.wow_pic = Image.open("wow.jpg")
        self.wow_pic = self.wow_pic.resize((320, 240))
        self.wow_pic_tk = ImageTk.PhotoImage(self.wow_pic)

    def centerWindow(self):
      
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - self.weight)/2
        y = (sh - self.height)/2
        self.parent.geometry('%dx%d+%d+%d' % (sw, sh, 0, 0))

    def insertText(self, str):
        self.text_area.insert(Tkinter.INSERT, "\n" + str)

    def showPicture(self):
        label_wow_pic = Label(self, image = self.wow_pic_tk)
        label_wow_pic.image = self.wow_pic_tk
        label_wow_pic.place(x = 10, y = 10)

    def playMusic(self):
        pygame.mixer.init()
        pygame.mixer.music.load("1.mp3")
        pygame.mixer.music.play()

    def pauseMusic(self):
        self.musicthread = threading.Thread(target = self.musicplayer.play)
        self.musicthread.start()

    def processIncoming(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                print "From queue, get msg:", msg
                if(msg == "show_text"):
                    self.insertText("I need to show a text")
                elif(msg == "show_picture"):
                    self.showPicture()
                elif(msg == "play_music"):
                    self.playMusic()
                elif(msg == "pause_music"):
                    self.pauseMusic()
                else:
                    self.insertText(msg)
            except Queue.Empty:
                pass