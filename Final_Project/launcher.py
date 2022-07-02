# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 09:32:14 2022

@author: XiaoTao
"""
import pygame

from pygame.locals import (
    RLEACCEL,
)


resolution = [800, 600]
screen = pygame.display.set_mode(resolution)

pygame.display.set_caption("Menu")
BG = pygame.image.load("image/Back1.png")
transfer=[0]

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font.ttf", size)

def switch():
    pygame.display.init()
    switch = True
    while switch:
        BackgroundList=["image/B1.png","image/B2.png","image/B3.png"]
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill("black")
        switch_text = get_font(25).render("Select the backgorund and press confirm", True, "White")
        switch_rect = switch_text.get_rect(center=(400,70))
        screen.blit(switch_text, switch_rect)
        
        switch_text = get_font(22).render("press confirm to return to main menu", True, "White")
        switch_rect = switch_text.get_rect(center=(400,100))
        screen.blit(switch_text, switch_rect)
        
        Options_switch = Button(image=None, pos=(700, 300),
            text_input="Switch", font=get_font(25),
            base_color="White", hovering_color="Green"
            )
        Options_switch.changeColor(OPTIONS_MOUSE_POS)
        Options_switch.update(screen)
        
        Options_confirm = Button(image=None, pos=(400, 500),
            text_input="Confirm", font=get_font(25),
            base_color="White", hovering_color="Green"
            )
        Options_confirm.changeColor(OPTIONS_MOUSE_POS)
        Options_confirm.update(screen)
        
        switch = pygame.image.load(BackgroundList[transfer[0]]).convert_alpha()
        switch.set_colorkey([255, 255, 255], RLEACCEL)
        switch_rect = switch.get_rect(center = [400,300])
        screen.blit(switch, switch_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Options_switch.checkForInput(OPTIONS_MOUSE_POS):
                    transfer[0]+=1
                    if transfer[0] == len(BackgroundList):
                        transfer[0]=0
                if Options_confirm.checkForInput(OPTIONS_MOUSE_POS):
                    switch = False
                    show = True
                    main_menu(show)
                    
                    
        pygame.display.update()
    
    


   
def options():
    option = True
    while option:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("White")

        OPTIONS_TEXT = get_font(25).render("Previous game records", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 100))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(
            image=None, pos=(300, 460),
            text_input="BACK", font=get_font(25),
            base_color="Black", hovering_color="Green"
            )

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    option = False
                    show = True
                    main_menu(show)
                    
        pygame.display.update()
    
def main_menu(show):   
    pygame.init()
    while show:
        
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(60).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))


        PLAY_BUTTON = Button(
            image = None, pos = (400, 200),
            text_input = "Start", font = get_font(40), 
            base_color = "#d7fcd4", hovering_color = "White"
            )
        SWITCH_BUTTON = Button(
            image = None, pos = (400, 300),
            text_input = "Map Selction", font = get_font(40), 
            base_color = "#d7fcd4", hovering_color = "White"
            )
        OPTIONS_BUTTON = Button(
            image = None, pos=(400, 400),
            text_input = "RECORD", font = get_font(40),
            base_color = "#d7fcd4", hovering_color = "White"
            )
        QUIT_BUTTON = Button(
            image = None, pos = (400, 500),
            text_input = "QUIT", font = get_font(40),
            base_color = "#d7fcd4", hovering_color = "White"
            )

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, SWITCH_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    show = False
                    
                if SWITCH_BUTTON.checkForInput(MENU_MOUSE_POS):
                    switch()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()      
        pygame.display.update()
    return
