#NAME: Sing Wong
#ID:   16425491

import random

_DEBUG_MODE = False

class Faller:
    def __init__(self,col,bottem_row,touchdown,values)-> None:
        'faller class, that contains location, state and values'
        self.col = col
        self.bottem_row = bottem_row
        self.touchdown = touchdown
        self.values = values

    def _move_down_by_1(self)-> None:
        'move faller down by 1'
        self.bottem_row += 1

    def _move_right(self)-> None:
        'move faller right'
        self.col += 1

    def _move_left(self)-> None:
        'move faller left'
        self.col -= 1

    def _rotate(self)-> None:
        'rotate the faller'
        self.values = [self.values[1], self.values[2], self.values[0]]

    def _touchdown(self)-> None:
        'set faller to touchdown'
        self.touchdown = True


class GameState:

    def __init__(self, num_of_rows: int, num_of_cols: int,
                 content: list) -> None:

        '''the Gamestate contains all information of the game,
        including gameboard, faller info and running status'''
        gameboard = []
        for col in range(num_of_cols):
            gameboard.append([])                
            for row in range(num_of_rows):
                if content == None or content[row][col] == ' ':
                    gameboard[-1].append(0)
                else:
                    gameboard[-1].append(content[row][col])
        self.board = gameboard
        self.faller = Faller(-1, None, None, None)
        self.running = True

#faller handling section

    def auto_gen_faller(self) -> None:
        colors = []
        for i in range(3):
            color = chr(random.randint(0,9)+65)
            colors.append(color)
        drop_list = self._check_avalible_space_for_create_faller()
        if len(drop_list) == 0:
            self.game_over()
        else:
            drop_col = int(drop_list[random.randint(0,len(drop_list)-1)])
            if _DEBUG_MODE:
                print(drop_list)
                print (colors)
                print(drop_col)
            self._create_faller(drop_col,colors)

    def handle_create_faller(self, user_input: str) -> None:
        '''directly feed in user_input sting and creats
        the faller accordingly'''
        user_input = user_input.strip()
        drop_col = int(user_input[2])-1
        self._create_faller(drop_col,[user_input[-1],
                                     user_input[-3],
                                     user_input[-5]])


    def _create_faller(self, drop_col: int, values: list) -> bool:
        '''the actual function that creates the faller and
        returns True if the faller is created successfully
        returns False if the colume is full
        and calls game over if every colume is full'''
        if not self.check_faller_exist():
            if self._check_space_for_create_faller(drop_col):
                self.faller = Faller(int(drop_col),0,False,values)
                return True
            else:
                if _DEBUG_MODE:
                    print('faller creation rejected: colume full')
                if len(self._check_avalible_space_for_create_faller()) == 0:
                    self.game_over()
                else:
                    return False
        else:
            if _DEBUG_MODE:
                print('faller creation rejected: faller exist')
            return False

    def _check_space_for_create_faller(self, drop_col: int) -> None:
        'a check for creating faller, see if the colume have space to create one'
        if self.board[int(drop_col)][0] == 0:
            return True
        else:
            return False
    def _check_avalible_space_for_create_faller(self) -> list:
        'returns all avalible col for creating faller as a list'
        avalible_space = []
        for col in range(len(self.board)):
            if self._check_space_for_create_faller(col):
                avalible_space.append(col)

        return avalible_space

    def move_faller_down_by_1(self) -> None:
        '''move faller down by one, or for time pass
        if space under is have jew or is the bottem,
        turn faller into touch down state'''
        if self.check_faller_exist():
            if self._move_down_check():
                self.faller._move_down_by_1()
            else:
                self._comfirm_touchdown()

    def move_faller_right(self) -> None:
        'move faller right by 1 col, do nothing if not allowed'
        if self.check_faller_exist() and self._move_right_check():
            self.faller._move_right()
            
    def move_faller_left(self) -> None:
        'move faller ledt by 1 col, do nothing if not allowed'
        if self.check_faller_exist() and self._move_left_check():
            self.faller._move_left()

    def rotate_faller(self) -> None:
        'rotates the faller, do nothing id no faller'
        if self.check_faller_exist():
            self.faller._rotate()

    def check_faller_exist(self) -> bool:
        'return True if faller exist, False if not'
        if self.faller == None:
            return False
        elif self.faller.col == -1:
            return False
        else:
            return True

    def _move_down_check(self) -> bool:
        '''a pre-check for moving faller down, see if there is space
        return True if there is space and False if not'''
        col = self.faller.col
        row = self.faller.bottem_row

        if row == len(self.board[0])-1:
            return False
        elif self.board[col][row+1] != 0:
            return False
        else:
            return True

    def _comfirm_touchdown(self) -> None:
        'change faller into touch down state'
        self.faller.touchdown = True

    def _move_left_check(self) -> bool:
        '''a pre-check for moving faller left, see if there is space
        return True if there is space and False if not'''
        col = self.faller.col
        row = self.faller.bottem_row
        
        if col == 0:
            return False
        elif self.board[col-1][row] != 0:
            return False
        else:
            return True

    def _move_right_check(self) -> bool:
        '''a pre-check for moving faller left, see if there is space
        return True if there is space and False if not'''
        col = self.faller.col
        row = self.faller.bottem_row
        
        if col == len(self.board)-1:
            return False
        elif self.board[col+1][row] != 0:
            return False
        else:
            return True

    def faller_check(self) -> bool:
        '''check if there is a faller
        return True is if faller exist and false if not'''
        if self.faller == None:
            return False
        elif self.faller.col == -1:
            return False
        else:
            return True

#touchdown section

    def touchdown_check(self) -> bool:
        'returns the faller touchdown state'
        return self.faller.touchdown

    def froze_touchdown(self) -> None:
        '''transfer the faller to gameboard and set faller to non-existing'''
        gameboard = self.board
        col = int(self.faller.col)
        row = self.faller.bottem_row
        gameboard[col][row] = self.faller.values[0]
        gameboard[col][row-1] = self.faller.values[1]
        gameboard[col][row-2] = self.faller.values[2]
        
        self.board = gameboard
        self.faller = Faller(-1, None, None, None)

#match checking section

    def check_faller_match(self) -> None:
        '''checks all matches and set matching state to all mathing jews
        originating from the 3 faller jews'''
        if self.faller.bottem_row <= 1:
            self.game_over()
            
        for i in range(3):
            if _DEBUG_MODE:
                print('i : '+str(i))
            self._check_cell_match\
            (self.faller.bottem_row-i,self.faller.col, self.faller.values[i])

        self.froze_touchdown()

    def _check_cell_match(self, row:int, col:int, jew:str) -> None:
        '''checks all matches and set matching state to all mathing jews
        originating from a given location'''
        self._check_hori_match(row,col,jew)
        self._check_vert_match(row,col,jew)
        self._check_diag_up_match(row,col,jew)
        self._check_diag_down_match(row,col,jew)


    def _check_hori_match(self, row: int, col: int, jew: str) -> None:
        'checks for horizontal matches and set them to matching state'
        pos_jew_link = self._get_jew_link(row,col,jew,0,1)
        neg_jew_link = self._get_jew_link(row,col,jew,0,-1)

        self._handle_jew_link(row,col,pos_jew_link,neg_jew_link,0,1)
            
    def _check_vert_match(self, row: int, col: int, jew: str) -> None:
        'checks for vertical matches and set them to matching state'
        pos_jew_link = self._get_jew_link(row,col,jew,1,0)
        neg_jew_link = self._get_jew_link(row,col,jew,-1,0) + self._special_vert_jew_link_check(row, col, jew)

        self._handle_jew_link(row,col,pos_jew_link,neg_jew_link,1,0)

    def _special_vert_jew_link_check(self, row: int, col: int, jew: str) -> int:
        '''hanles a vertical special case on checking jew link,
        where the faller is not written to the board, but still needs to
        be accounted for the upward jew link'''
        jew_link = 0
        if self.check_faller_exist():
            if self.faller.bottem_row - row == 0:   #i==0
                if self.faller.values[0] == self.faller.values[1]:
                    jew_link += 1
                    if self.faller.values[1] == self.faller.values[2]:
                        jew_link += 1
        return jew_link
                            

    def _check_diag_up_match(self, row: int, col: int, jew: str) -> None:
        'checks for diagonal that goes upward matches and set them to matching state'
        pos_jew_link = self._get_jew_link(row,col,jew,-1,1)
        neg_jew_link = self._get_jew_link(row,col,jew,1,-1)

        self._handle_jew_link(row,col,pos_jew_link,neg_jew_link,-1,1)
        
    def _check_diag_down_match(self, row: int, col: int, jew: str) -> None:
        'checks for diagonal that goes downward matches and set them to matching state'
        pos_jew_link = self._get_jew_link(row,col,jew,1,1)
        neg_jew_link = self._get_jew_link(row,col,jew,-1,-1)

        self._handle_jew_link(row,col,pos_jew_link,neg_jew_link,1,1)

    def _set_match(self, row: int, col: int) -> None:
        'set a giving location match state to match'
        self.board[col][row] = self.board[col][row].lower()

    def _get_jew_link(self, row: int, col: int, jew: str,
                      row_delta:int, col_delta:int) -> int:

        '''with the given location and row/col delta and value of jew
        returns number of the same jew that is facing at the given direction
         originating from the given location'''
        
        jew_link = 1
        num = 0
        while True:
            num += 1
            if col+(num*col_delta) < 0 or row+(num*row_delta) < 0 \
               or col+num*col_delta > len(self.board)-1\
               or row+num*row_delta > len(self.board[0])-1:
                if _DEBUG_MODE:
                    print('wall_hit_break',end=' ')
                break
            elif self.board[col+(num*col_delta)][row+(num*row_delta)] == 0:
                if _DEBUG_MODE:
                    print('empty_break',end=' ')
                break
            elif self.board[col+(num*col_delta)][row+(num*row_delta)].upper() == jew.upper():
                jew_link += 1
                if _DEBUG_MODE:
                    print(self.board[col+(num*col_delta)][row+(num*row_delta)].upper())
                    print('match',end=' ')
            else:
                if _DEBUG_MODE:
                    print('not_mathch_break',end=' ')
                break
        return int(jew_link) - 1

    def _handle_jew_link(self, row: int, col: int,
                         pos_jew_link: int, neg_jew_link: int,
                         row_delta:int, col_delta: int) -> None:
        '''given location, pos and neg jew link,
        then set the jews on board to match state accordingly,
        if the link is > 3
        this funcation also handles the vertical jew link case automaticaly'''

        jew_link = pos_jew_link + neg_jew_link + 1
            
        if jew_link >= 3:
            if row_delta == 1 and col_delta == 0 and self.faller_check(): #vertical case with faller
                self._handle_vert_jew_link_special_case(row, col, pos_jew_link,
                                                        neg_jew_link)
                
            else: self._set_jew_link_match(row, col, pos_jew_link, neg_jew_link,
                                     row_delta, col_delta)

    def _handle_vert_jew_link_special_case(self, row: int, col: int,
                                           pos_jew_link: int, neg_jew_link: int) -> None:
        '''handles seting upward vertial link to match state,
        where the faller is not writen in the board yet,
        but still need to be changed to match state'''
        
        self._set_jew_link_match(row, col, pos_jew_link, 0 , 1 , 0 )

        for i in range(neg_jew_link+1):
            self.faller.values[i] = self.faller.values[i].lower()

    def _set_jew_link_match(self, row: int, col: int,
                            pos_jew_link: int, neg_jew_link: int,
                            row_delta:int, col_delta:int) -> None:
        '''given details of the jew link,
        then it will set the whole jew link into match state'''
        
        for num in range(1,pos_jew_link+1):
            self._set_match(row + num*row_delta, col + num*col_delta)
        for num in range(1,neg_jew_link+1):
            self._set_match(row - num*row_delta, col - num*col_delta)

        if self.faller_check():
            loc_of_jew_in_faller = self.faller.bottem_row - row
            self.faller.values[loc_of_jew_in_faller] = \
                    self.faller.values[loc_of_jew_in_faller].lower()

        else:
            self._set_match(row, col)


#handling with matches section
    
    def if_match_exist(self) -> bool:
        '''returns True if there is at least one jew that is in match state
        returns False if no jew is in match state'''
        for row in range(len(self.board[0])):
            for col in range(len(self.board)):
                if self.board[col][row] != 0:
                    if self.board[col][row].islower():
                        return True
        return False
    
    def handle_match(self) -> None:
        '''handles all exisiting matches,
        including moving canceling all exiting matches
        and move all the floating jews down'''
        self._delete_all_exiting_matches()
        self._move_all_jew_down()

    def _delete_all_exiting_matches(self)-> None:
        for row in range(len(self.board[0])):
            for col in range(len(self.board)):
                if self.board[col][row] != 0:
                    if self.board[col][row].islower():
                        self.board[col][row] = 0


    def _move_all_jew_down(self) -> None:
        'move all floating jews down'
        for col in range(len(self.board)):
            top_most_jew = len(self.board[0])
            empty_space = 0
            for row in range(len(self.board[0])-1,-1,-1):
                if self.board[col][row] != 0 and empty_space == 0:
                    top_most_jew = row
                elif self.board[col][row] == 0:
                    empty_space += 1
                elif self.board[col][row] != 0 and empty_space > 0:
                    self.board[col][top_most_jew - 1] = self.board[col][row]
                    self.board[col][row] = 0
                    top_most_jew -= 1
                    self._check_cell_match(top_most_jew ,col,
                                    self.board[col][top_most_jew])

    def quit_game(self) -> None:
        'quite game by setting game running state to False'
        self.running = False

    def game_over(self) -> None:
        'print game over and quit game'
        if _DEBUG_MODE:
            print('GAME OVER')
        self.quit_game()




