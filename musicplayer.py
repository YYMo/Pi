"""
 Show how to run background music in Pygame.
  
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
"""
import pygame
 
class MusicPlayer:
    def __init__(self):
        pygame.init()
        self.done = False
        self.playing = False
        pygame.mixer.music.load('1.mp3')
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
 
    def play(self):
        self.playing = True
        pygame.mixer.music.play()
        '''
        while not self.done:
            # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self.done = True # Flag that we are done so we exit this loop
                elif event.type == pygame.constants.USEREVENT:
                    pygame.mixer.music.load('1.mp3')
                    pygame.mixer.music.play()
                    '''
    def pause(self):
        if(self.playing):
            pygame.music.pause()

    def stop(self):
        if(self.playing):
            pygame.music.stop()


def main():
    mp = MusicPlayer();
    mp.play();

if __name__ == '__main__':
    main()

