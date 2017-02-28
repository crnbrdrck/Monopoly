import pygame



class Button:

    '''
    surface = surface where Button will be displayed
    x = x position of top left corner
    y = y position of top left corner
    width = width of button in pixels
    height = height of button in pixels
    text = button label
    '''
    def __init__(self,surface,x,y,width,height,text):
        self.rect = pygame.Rect(x,y,width,height)
        pygame.draw.rect(surface,(150,150,255),self.rect)
        font_size = int(width // len(text))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 1, (0,0,0))
        surface.blit(myText, ((x + width / 2) - myText.get_width() / 2, (y + height / 2) - myText.get_height() / 2))

    # Checks if button has been pressed, uses mouse position (x,y)
    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0] and mouse[1] > self.rect.topleft[1] and mouse[0] < self.rect.bottomright[0] \
        and mouse[1] < self.rect.bottomright[1]:
            return True
        else:
            return False
