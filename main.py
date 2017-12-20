#NAME: Sing Wong
#ID:   16425491

import pygame

import game_logic

_DEBUG_MODE = False


color_table = {'A':pygame.Color(230,0,0),#Red
               'B':pygame.Color(230,115,0),#Organe
               'C':pygame.Color(230,230,0),#Yellow
               'D':pygame.Color(0,230,0),#Green
               'E':pygame.Color(0,230,230),#Cyan
               'F':pygame.Color(0,0,230),#Blue
               'G':pygame.Color(115,0,115),#Purple
               'H':pygame.Color(230,0,230),#Magenta
               'I':pygame.Color(230,180,190),#Pink
               'J':pygame.Color(130,65,0)}#Brown

gameover_color_table = {'A':pygame.Color(54,54,54),#Red
                        'B':pygame.Color(145,145,145),#Organe
                        'C':pygame.Color(237,237,237),#Yellow
                        'D':pygame.Color(183,183,183),#Green
                        'E':pygame.Color(202,202,202),#Cyan
                        'F':pygame.Color(18,18,18),#Blue
                        'G':pygame.Color(127,127,127),#Purple
                        'H':pygame.Color(36,36,36),#Magenta
                        'I':pygame.Color(206,206,206),#Pink
                        'J':pygame.Color(86,86,86)}#Brown

class ColGame():
    def __init__(self):
        'initializing Column Game'
        self.running = True
        self.cycle = 0

    def run(self) -> None:
        'main function that runs the game'
        pygame.init()
        pygame.display.set_caption('Columns Game')
        gamestate = game_logic.GameState(12,6,None)
        self._resize_surface((200, 400),gamestate)
        if _DEBUG_MODE:
            print(gamestate.board)

        while self.running == True:
            pygame.time.Clock().tick(20)
            self._handle_events(gamestate)
            self._redraw(gamestate)

        pygame.quit()

    def _handle_events(self, gamestate: game_logic.GameState) -> None:
        'handles all user input and converting into related functions'

        if gamestate.running == False:
            if _DEBUG_MODE:
                print('#####################GAME OVER SCREEN')
            self.gameover_screen(gamestate)
        elif gamestate.if_match_exist():
            gamestate.handle_match()
        elif not gamestate.check_faller_exist():
            gamestate.auto_gen_faller()
        elif gamestate.touchdown_check() == True:
            gamestate.check_faller_match()
        else:
            if self.cycle == 20:
                gamestate.move_faller_down_by_1()
                self.cycle = 0
            else:
                self.cycle += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size,gamestate)
            
            elif gamestate.touchdown_check() == False \
                 and gamestate.check_faller_exist\
                 and event.type == pygame.KEYDOWN:

                keys = pygame.key.get_pressed()

                if keys[pygame.K_DOWN]:
                    gamestate.move_faller_down_by_1()
                elif keys[pygame.K_RIGHT]:
                    gamestate.move_faller_right()
                elif keys[pygame.K_LEFT]:
                    gamestate.move_faller_left()
                elif keys[pygame.K_SPACE]:
                    gamestate.rotate_faller()
                elif keys[pygame.K_RETURN]:
                    gamestate.running = False
        
                    
                

    
    def _resize_surface(self, size: (int, int),
                        gamestate :game_logic.GameState) -> None:
        'handles resizing of surface'
        pygame.display.set_mode(size, pygame.RESIZABLE)
        self._redraw(gamestate)

    def _redraw(self,gamestate :game_logic.GameState) -> None:
        'redraw the surface'
        self._draw_board(gamestate)
        pygame.display.flip()

    def _draw_board(self,gamestate) -> None:
        'drawing the whole board'
        surface = pygame.display.get_surface()
        height = surface.get_height()
        width = surface.get_width()
        
        for x in range(6):
            for y in range(12):
                #background
                square = pygame.Rect(x*1/6*width,y*1/12*height,1/6*width+1,1/12*height+1)
                back_color = x*20+y*10
                surface.fill(pygame.Color(back_color,back_color,back_color),square)
                
                if gamestate.board[x][y] != 0 and gamestate.running == True:
                    if gamestate.board[x][y].islower():
                        surface.fill(pygame.Color(255,255,255),square)
                        pygame.draw.ellipse(surface,
                                            color_table[gamestate.board[x][y].upper()],
                                            square)
                    else:
                        pygame.draw.ellipse(surface,
                                            color_table[gamestate.board[x][y].upper()],
                                            square)
                elif gamestate.board[x][y] != 0 and gamestate.running == False:
                    pygame.draw.ellipse(surface,
                                        gameover_color_table[gamestate.board[x][y].upper()],
                                        square)

                if gamestate.running == False:
                    self._gameover_text()

                
                # faller
                for i in range(3):
                    if x == gamestate.faller.col and y == gamestate.faller.bottem_row-i:
                        if gamestate.faller.touchdown == False:
                            pygame.draw.ellipse(surface,
                                                color_table[gamestate.faller.values[i].upper()],
                                                square)
                        else: 
                            surface.fill(pygame.Color(127,127,127),square)
                            pygame.draw.ellipse(surface,
                                                color_table[gamestate.faller.values[i].upper()],
                                                square)
        pygame.font.init()
        font = pygame.font.SysFont("comicsansms",round(0.05*height))
        text = font.render('Columns',True,pygame.Color(200,200,200),None)
        surface.blit(text, (0,0))
        

    def gameover_screen(self,gamestate: game_logic.GameState) -> None:
        'shows after gameover'
        self._gameover_animation(gamestate)
        self._ask_user_quit(gamestate)

    def _gameover_animation(self,gamestate)-> None:
        'the gameover animation that shows in gameover screen'
        surface = pygame.display.get_surface()
        height = surface.get_height()
        width = surface.get_width()

        for cycle in range (18):
            for x in range(6):
                for y in range(12):
                    #background
                    square = pygame.Rect(x*1/6*width,y*1/12*height,1/6*width+1,1/12*height+1)
                    back_color = x*20+y*10
                    surface.fill(pygame.Color(back_color,back_color,back_color),square)
                    
                    if gamestate.board[x][y] != 0 and x+y >= cycle:
                        pygame.draw.ellipse(surface,
                                            color_table[gamestate.board[x][y].upper()],
                                            square)
                
                    elif gamestate.board[x][y] != 0:
                        pygame.draw.ellipse(surface,
                                            gameover_color_table[gamestate.board[x][y].upper()],
                                            square)
            pygame.font.init()
            font = pygame.font.SysFont("comicsansms",round(0.05*height))
            if cycle % 2 == 0:
                text = font.render('GAME OVER',True,
                                   pygame.Color(200,0,0),pygame.Color(200,200,200))
            else:
                text = font.render('GAME OVER',True,
                                   pygame.Color(200,200,200),pygame.Color(200,0,0))
            surface.blit(text, (0,0))
            
            pygame.display.flip()                    
            pygame.time.wait(120)

    def _ask_user_quit(self,gamestate) -> None:
        'quit after user presses any button'
        surface = pygame.display.get_surface()
        height = surface.get_height()
        width = surface.get_width()

        
        self._gameover_text()
        pygame.display.flip()
        
        while self.running == True:
            pygame.time.wait(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._end_game()
                    break
                
                elif event.type == pygame.VIDEORESIZE:
                    self._resize_surface(event.size,gamestate)
                    
                elif event.type == pygame.KEYDOWN:
                    self._end_game()
                    break

    def _gameover_text(self) -> None:
        'just showing "Click any button to quit" on the board'
        surface = pygame.display.get_surface()
        height = surface.get_height()
        
        pygame.font.init()
        font = pygame.font.SysFont("comicsansms",round(0.05*height))
        text1 = font.render('Click Any Button',
                           True,pygame.Color(255,0,0),pygame.Color(200,200,200))
        text2 = font.render('To Quit',
                   True,pygame.Color(255,0,0),pygame.Color(200,200,200))
        surface.blit(text1, (0,round(0.2*height)))
        surface.blit(text2, (0,round(0.3*height)))

        
        

    def _end_game(self) -> None:
        'end game function'
        self.running = False
        

def main() -> None :
    ColGame().run()


if __name__ == '__main__':
    main()
