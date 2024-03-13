import time
from copy import deepcopy
import heapq
import pygame
import psutil

class State:
    #Esta classe define o jogo em si: o tabuleiro, moves e peças.
    def __init__(self,board,dic,move_history=[]):
        self.board=deepcopy(board)
        self.dic=dic
        self.move_history = [] + move_history + [self]
       
    def __str__(self):
        return convert_board_to_str(self.board)
    
    def __hash__(self):
        # to be able to use the state in a set
        return hash(str(self.board))
    def __eq__(self, other):
        # compara os tabuleiros
        return self.board == other.board
    
    def blanks(self):
        #função que retorna as posições dos espaços em branco bem como se estão juntos e em que posição
        blanks=[]
        state =State(self.board,self.dic,self.move_history)
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j]==0:
                    blanks.append((i,j))
        if (blanks[0][0]==blanks[1][0] and blanks[0][1]==blanks[1][1]-1):
            return (blanks,1)
        elif (blanks[0][1]==blanks[1][1] and blanks[0][0]==blanks[1][0]-1):
            return (blanks,2)
        else:
            return (blanks,0)
    
    def children(self):
        #função que retorna os moves possíveis dada um estado do tabuleiro
        blanks, forma = self.blanks()
        children = []
        if forma == 1:
            funcs = [self.up_blank_h, self.down_blank_h]
        elif forma == 2:
            funcs = [self.left_blank_v, self.right_blank_v]
        else:
            funcs = [self.up_blank, self.down_blank, self.left_blank, self.right_blank]
        for i in range(len(blanks)):
            for func in funcs:
                state=State(self.board,self.dic,self.move_history)
                child = func(i,blanks,state)
                if child:
                    children.append(child)
        return children

        
    def up_blank_h(self,i,espacos,state):
        #espaço em branco junto na horizontal sobe
        if espacos[i][0] == 0:
            return None
        if i==0:
            if self.dic[state.board[espacos[i][0]-1][espacos[i][1]]][0]=='grande' and self.dic[state.board[espacos[i][0]-1][espacos[i][1]+1]][0]=='grande':
                state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]-2][espacos[i][1]]
                state.board[espacos[i][0]][espacos[i][1]+1]=state.board[espacos[i][0]-2][espacos[i][1]]
                state.board[espacos[i][0]-2][espacos[i][1]] = 0
                state.board[espacos[i][0]-2][espacos[i][1]+1] = 0
                return state

            elif self.dic[state.board[espacos[i][0]-1][espacos[i][1]]][0]=='recth' and self.dic[state.board[espacos[i][0]-1][espacos[i][1]+1]][0]=='recth':
                state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]-1][espacos[i][1]]
                state.board[espacos[i][0]][espacos[i][1]+1]=state.board[espacos[i][0]-1][espacos[i][1]]
                state.board[espacos[i][0]-1][espacos[i][1]] = 0
                state.board[espacos[i][0]-1][espacos[i][1]+1] = 0
                return state
        elif self.dic[state.board[espacos[i][0]-1][espacos[i][1]]][0]=='rectv':
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]-1][espacos[i][1]]
            state.board[espacos[i][0]-2][espacos[i][1]] = 0
            return state
        elif self.dic[state.board[espacos[i][0]-1][espacos[i][1]]][0]=='sqr':
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]-1][espacos[i][1]]
            state.board[espacos[i][0]-1][espacos[i][1]]=0
            return state
        else:
            return None
        
    def down_blank_h(self,i,espacos,state):
        #espaço em branco junto na horizontal desce
        if espacos[i][0] == len(state.board) - 1:
            return None
        if i==0:
            if self.dic[state.board[espacos[i][0]+1][espacos[i][1]]][0]=='grande' and self.dic[state.board[espacos[i][0]+1][espacos[i][1]+1]][0]=='grande':
                state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]+2][espacos[i][1]]
                state.board[espacos[i][0]][espacos[i][1]+1]=state.board[espacos[i][0]+2][espacos[i][1]]
                state.board[espacos[i][0]+2][espacos[i][1]] = 0
                state.board[espacos[i][0]+2][espacos[i][1]+1] = 0
                return state

            elif self.dic[state.board[espacos[i][0]+1][espacos[i][1]]][0]=='recth' and self.dic[state.board[espacos[i][0]+1][espacos[i][1]+1]][0]=='recth':
                state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]+1][espacos[i][1]]
                state.board[espacos[i][0]][espacos[i][1]+1]=state.board[espacos[i][0]+1][espacos[i][1]]
                state.board[espacos[i][0]+1][espacos[i][1]] = 0
                state.board[espacos[i][0]+1][espacos[i][1]+1] = 0
                return state
        elif self.dic[state.board[espacos[i][0]+1][espacos[i][1]]][0]=='rectv':
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]+1][espacos[i][1]]
            state.board[espacos[i][0]+2][espacos[i][1]] = 0
            return state
        elif self.dic[state.board[espacos[i][0]+1][espacos[i][1]]][0]=='sqr':
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]+1][espacos[i][1]]
            state.board[espacos[i][0]+1][espacos[i][1]]=0
            return state
        else:
            return None
    def left_blank_h(self,i,espacos,state):
        #espaço em branco junto na horizontal para a esquerda
        if espacos[i][1] == 0:
                return None
        elif self.dic[state.board[espacos[i][0]][espacos[i][1]-1]][0]=='sqr':
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]][espacos[i][1]-1]
            state.board[espacos[i][0]][espacos[i][1]-1]=0
            return state
        elif self.dic[state.board[espacos[i][0]][espacos[i][1]-1]][0]=='recth':
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]][espacos[i][1]-1]
            state.board[espacos[i][0]][espacos[i][1]-2] = 0
            return state
        else:
            return None
        
    def right_blank_h(self,i,espacos,state):
        #espaço em branco junto na horizontal para a direita
        if espacos[i][1]>=len(state.board[0]) - 2 :
            return None
        if self.dic[state.board[espacos[i][0]][espacos[i][1]+2]][0]=='sqr':
            state.board[espacos[i][0]][espacos[i][1]+1] = state.board[espacos[i][0]][espacos[i][1]+2]
            state.board[espacos[i][0]][espacos[i][1]+2]=0
            return state
        if self.dic[state.board[espacos[0][0]][espacos[0][1]+2]][0]=='recth':
            state.board[espacos[i][0]][espacos[i][1]+1]=state.board[espacos[i][0]][espacos[i][1]+2]
            state.board[espacos[i][0]][espacos[i][1]+3] = 0
            return state
        else:
            return None
    def up_blank_v(self,i,espacos,state):
        #espaço em branco junto na vertical sobe
        if espacos[i][0] == 0:
            return None
        if self.dic[state.board[espacos[i][0]-1][espacos[i][1]]][0]=='rectv':
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]-1][espacos[i][1]]
            state.board[espacos[i][0]-2][espacos[i][1]] = 0
            return state
        elif self.dic[state.board[espacos[i][0]-1][espacos[i][1]]][0]=='sqr':
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]-1][espacos[i][1]]
            state.board[espacos[i][0]-1][espacos[i][1]]=0
            return state
        else:
            return None
        
    def down_blank_v(self,i,espacos,state):
        #espaço em branco junto na vertical desce
        if espacos[i][0] >= len(state.board) - 2:
            return None
        elif self.dic[state.board[espacos[i][0]+2][espacos[i][1]]][0]=='rectv':
            state.board[espacos[i][0]+1][espacos[i][1]] = state.board[espacos[i][0]+2][espacos[i][1]]
            state.board[espacos[i][0]+3][espacos[i][1]] = 0
            return state
        elif self.dic[state.board[espacos[i][0]+2][espacos[i][1]]][0]=='sqr':
            state.board[espacos[i][0]+1][espacos[i][1]] = state.board[espacos[i][0]+2][espacos[i][1]]
            state.board[espacos[i][0]+2][espacos[i][1]]=0
            return state
        else:
            return None
    def left_blank_v(self,i,espacos,state):
        #espaço em branco junto na vertical vai p esquerda
        if espacos[i][1] == 0:
                return None
        if i==0:
            if self.dic[state.board[espacos[i][0]][espacos[i][1]-1]][0]=='grande' and self.dic[state.board[espacos[i][0]+1][espacos[i][1]-1]][0]=='grande':
                state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]][espacos[i][1]-2]
                state.board[espacos[i][0]+1][espacos[i][1]]=state.board[espacos[i][0]][espacos[i][1]-2]
                state.board[espacos[i][0]][espacos[i][1]-2] = 0
                state.board[espacos[i][0]+1][espacos[i][1]-2] = 0
                return state
            if self.dic[state.board[espacos[i][0]][espacos[i][1]-1]][0]=='rectv' and self.dic[state.board[espacos[i][0]+1][espacos[i][1]-1]][0]=='rectv':
                state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]][espacos[i][1]-1]
                state.board[espacos[i][0]+1][espacos[i][1]]=state.board[espacos[i][0]][espacos[i][1]-1]
                state.board[espacos[i][0]][espacos[i][1]-1] = 0
                state.board[espacos[i][0]+1][espacos[i][1]-1] = 0
                return state
        if self.dic[state.board[espacos[i][0]][espacos[i][1]-1]][0]=='recth':
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]][espacos[i][1]-1]
            state.board[espacos[i][0]][espacos[i][1]-2] = 0
            return state
        elif self.dic[state.board[espacos[i][0]][espacos[i][1]-1]][0]=='sqr':
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]][espacos[i][1]-1]
            state.board[espacos[i][0]][espacos[i][1]-1]=0
            return state
        else:
            return None
    def right_blank_v(self,i,espacos,state):
        #espaço em branco junto na vertical vai p direita
        if espacos[i][1]==len(state.board[0]) - 1 :
            return None
        if i==0:
            if self.dic[state.board[espacos[i][0]][espacos[i][1]+1]][0]=='grande' and self.dic[state.board[espacos[i][0]+1][espacos[i][1]+1]][0]=='grande':
                state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]][espacos[i][1]+2]
                state.board[espacos[i][0]+1][espacos[i][1]]=state.board[espacos[i][0]][espacos[i][1]+2]
                state.board[espacos[i][0]][espacos[i][1]+2] = 0
                state.board[espacos[i][0]+1][espacos[i][1]+2] = 0
                return state
            if self.dic[state.board[espacos[i][0]][espacos[i][1]+1]][0]=='rectv' and self.dic[state.board[espacos[i][0]+1][espacos[i][1]+1]][0]=='rectv':
                state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]][espacos[i][1]+1]
                state.board[espacos[i][0]+1][espacos[i][1]]=state.board[espacos[i][0]][espacos[i][1]+1]
                state.board[espacos[i][0]][espacos[i][1]+1] = 0
                state.board[espacos[i][0]+1][espacos[i][1]+1] = 0
                return state
        if self.dic[state.board[espacos[i][0]][espacos[i][1]+1]][0]=='recth':
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]][espacos[i][1]+1]
            state.board[espacos[i][0]][espacos[i][1]+2] = 0
            return state
        elif self.dic[state.board[espacos[i][0]][espacos[i][1]+1]][0]=='sqr':
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]][espacos[i][1]+1]
            state.board[espacos[i][0]][espacos[i][1]+1]=0
            return state
        else:
            return None
        
    
    def up_blank(self,i,espacos,state):
        #espaço em branco isolado sobe
        if espacos[i][0] == 0:
            return None
        if state.board[espacos[i][0]-1][espacos[i][1]]==0:                
            return None
        if self.dic[state.board[espacos[i][0]-1][espacos[i][1]]][0]=='grande':
            return None
        if self.dic[state.board[espacos[i][0]-1][espacos[i][1]]][0]=='recth':
            return None
        if self.dic[state.board[espacos[i][0]-1][espacos[i][1]]][0]=='rectv':
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]-1][espacos[i][1]]
            state.board[espacos[i][0]-2][espacos[i][1]] = 0
            return state
        else:
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]-1][espacos[i][1]]
            state.board[espacos[i][0]-1][espacos[i][1]]=0
            return state
        
    def down_blank(self,i,espacos,state):
        #espaço em branco isolado desce
        if espacos[i][0] == len(state.board) - 1:
            return None
        if self.dic[state.board[espacos[i][0]+1][espacos[i][1]]][0]=='grande':
            return None
        if self.dic[state.board[espacos[i][0]+1][espacos[i][1]]][0]=='recth':
            return None
        if self.dic[state.board[espacos[i][0]+1][espacos[i][1]]][0]=='rectv':
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]+1][espacos[i][1]]
            state.board[espacos[i][0]+2][espacos[i][1]] = 0
            return state
        else:
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]+1][espacos[i][1]]
            state.board[espacos[i][0]+1][espacos[i][1]] = 0
            return state
    def left_blank(self,i,espacos,state):
        #espaço em branco isolado vai p esquerda
        if espacos[i][1] == 0:
            return None
        if self.dic[state.board[espacos[i][0]][espacos[i][1]-1]][0]=='grande':
            return None
        if self.dic[state.board[espacos[i][0]][espacos[i][1]-1]][0]=='rectv':
            return None
        if self.dic[state.board[espacos[i][0]][espacos[i][1]-1]][0]=='recth':
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]][espacos[i][1]-2]
            state.board[espacos[i][0]][espacos[i][1]-2] = 0
            return state
        else:
            state.board[espacos[i][0]][espacos[i][1]]= state.board[espacos[i][0]][espacos[i][1]-1]
            state.board[espacos[i][0]][espacos[i][1]-1] = 0
            return state
    def right_blank(self,i,espacos,state):
        #espaço em branco isolado vai p esquerda
        if espacos[i][1]==len(state.board[0]) - 1 :
            return None
        if self.dic[state.board[espacos[i][0]][espacos[i][1]+1]][0]=='grande':
            return None
        if self.dic[state.board[espacos[i][0]][espacos[i][1]+1]][0]=='rectv':
            return None
        if self.dic[state.board[espacos[i][0]][espacos[i][1]+1]][0]=='recth':
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]][espacos[i][1]+2]
            state.board[espacos[i][0]][espacos[i][1]+2] = 0
            return state
        else:
            state.board[espacos[i][0]][espacos[i][1]] = state.board[espacos[i][0]][espacos[i][1]+1]
            state.board[espacos[i][0]][espacos[i][1]+1] = 0
            return state
    def up(self,num):
        #função que faz subir uma peça 'num' e retorna o estado 
        state =State(self.board,self.dic,self.move_history)
        if state.dic[num][1][0] == 0:
            return None
        if state.dic[num][0]=='sqr':
            if state.board[state.dic[num][1][0]-1][state.dic[num][1][1]]!=0:    
                return None
            else:
                state.board[state.dic[num][1][0]-1][state.dic[num][1][1]] = state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]][state.dic[num][1][1]] = 0
                state.dic[num][1][0]-=1
                return state
        elif state.dic[num][0]=='recth':
            if state.board[state.dic[num][1][0]-1][state.dic[num][1][1]]!=0 or state.board[state.dic[num][1][0]-1][state.dic[num][1][1]+1]!=0:
                return None
            else:
                state.board[state.dic[num][1][0]-1][state.dic[num][1][1]] = state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]-1][state.dic[num][1][1]+1] = state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]][state.dic[num][1][1]] = 0
                state.board[state.dic[num][1][0]][state.dic[num][1][1]+1] = 0
                state.dic[num][1][0]-=1
                return state
        elif state.dic[num][0]=='rectv':
            if state.board[state.dic[num][1][0]-1][state.dic[num][1][1]]!=0:
                return None
            else:
                state.board[state.dic[num][1][0]-1][state.dic[num][1][1]] = state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]+1][state.dic[num][1][1]] = 0
                state.dic[num][1][0]-=1
                return state
        elif state.dic[num][0]=='grande':
            if state.board[state.dic[num][1][0]-1][state.dic[num][1][1]]!=0 or state.board[state.dic[num][1][0]-1][state.dic[num][1][1]+1]!=0:
                return None
            else:
                state.board[state.dic[num][1][0]-1][state.dic[num][1][1]] = state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]-1][state.dic[num][1][1]+1]=state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]+1][state.dic[num][1][1]] = 0
                state.board[state.dic[num][1][0]+1][state.dic[num][1][1]+1] = 0
                state.dic[num][1][0]-=1
                return state
                
        
    def down(self,num):
        #função que faz descer uma peça 'num' e retorna o estado 
        state =State(self.board,self.dic,self.move_history)
        if state.dic[num][1][0] == len(state.board) - 1:
                return None
        if state.dic[num][0]=='sqr':
            if state.board[state.dic[num][1][0]+1][state.dic[num][1][1]]!=0:
                return None
            else:
                state.board[state.dic[num][1][0]+1][state.dic[num][1][1]] = state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]][state.dic[num][1][1]] = 0
                state.dic[num][1][0]+=1
                return state
        elif state.dic[num][0]=='recth':
            if state.board[state.dic[num][1][0]+1][state.dic[num][1][1]]!=0 or state.board[state.dic[num][1][0]+1][state.dic[num][1][1]+1]!=0:
                return None
            else:
                state.board[state.dic[num][1][0]+1][state.dic[num][1][1]] = state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]+1][state.dic[num][1][1]+1] = state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]][state.dic[num][1][1]] = 0
                state.board[state.dic[num][1][0]][state.dic[num][1][1]+1] = 0
                state.dic[num][1][0]+=1
                return state
        elif state.dic[num][0]=='rectv':
            if state.dic[num][1][0] == len(state.board) - 2:
                return None
            if state.board[state.dic[num][1][0]+2][state.dic[num][1][1]]!=0:
                return None
            else:
                state.board[state.dic[num][1][0]+2][state.dic[num][1][1]] = state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]][state.dic[num][1][1]] = 0
                state.dic[num][1][0]+=1
                return state
        elif state.dic[num][0]=='grande':
            if state.dic[num][1][0] == len(state.board) - 2:
                return None
            if state.board[state.dic[num][1][0]+2][state.dic[num][1][1]]!=0 or state.board[state.dic[num][1][0]+2][state.dic[num][1][1]+1]!=0:
                return None
            else:
                state.board[state.dic[num][1][0]+2][state.dic[num][1][1]] = state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]+2][state.dic[num][1][1]+1]=state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]][state.dic[num][1][1]] = 0
                state.board[state.dic[num][1][0]][state.dic[num][1][1]+1] = 0
                state.dic[num][1][0]+=1
                return state
    
    def left(self,num):
        #função que faz ir p esquerda uma peça 'num' e retorna o estado 
        state =State(self.board,self.dic,self.move_history)
        if state.dic[num][1][1] == 0:
                return None
        if state.dic[num][0]=='sqr':
            if state.board[state.dic[num][1][0]][state.dic[num][1][1]-1]!=0:
                return None
            else:
                state.board[state.dic[num][1][0]][state.dic[num][1][1]-1]= state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]][state.dic[num][1][1]] = 0
                state.dic[num][1][1]-=1
                return state
        elif state.dic[num][0]=='recth':
            if state.board[state.dic[num][1][0]][state.dic[num][1][1]-1]!=0:
                return None
            else:
                state.board[state.dic[num][1][0]][state.dic[num][1][1]-1] = state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]][state.dic[num][1][1]+1] = 0
                state.dic[num][1][1]-=1
                return state
        elif state.dic[num][0]=='rectv':
            if state.board[state.dic[num][1][0]][state.dic[num][1][1]-1]!=0 or state.board[state.dic[num][1][0]+1][state.dic[num][1][1]-1]!=0:
                return None
            else:
                state.board[state.dic[num][1][0]][state.dic[num][1][1]-1] = state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]+1][state.dic[num][1][1]-1]= state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]][state.dic[num][1][1]] = 0
                state.board[state.dic[num][1][0]+1][state.dic[num][1][1]] = 0
                state.dic[num][1][1]-=1
                return state
        elif state.dic[num][0]=='grande':
            if state.board[state.dic[num][1][0]][state.dic[num][1][1]-1]!=0 or state.board[state.dic[num][1][0]+1][state.dic[num][1][1]-1]!=0:
                return None
            else:
                state.board[state.dic[num][1][0]][state.dic[num][1][1]-1] = state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]+1][state.dic[num][1][1]-1]=state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]][state.dic[num][1][1]+1] = 0
                state.board[state.dic[num][1][0]+1][state.dic[num][1][1]+1] = 0
                state.dic[num][1][1]-=1
                return state
        
    def right(self,num):
        #função que faz ir p direita uma peça 'num' e retorna o estado 
        state =State(self.board,self.dic,self.move_history)
        if state.dic[num][1][1]==len(state.board[0]) - 1 :
                return None
        if state.dic[num][0]=='sqr':
            if state.board[state.dic[num][1][0]][state.dic[num][1][1]+1]!=0:
                return None
            else:
                state.board[state.dic[num][1][0]][state.dic[num][1][1]+1] = state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]][state.dic[num][1][1]] = 0
                state.dic[num][1][1]+=1
                return state
        elif state.dic[num][0]=='recth':
            if state.board[state.dic[num][1][0]][state.dic[num][1][1]+2]!=0:
                return None
            else:
                state.board[state.dic[num][1][0]][state.dic[num][1][1]+2] = state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]][state.dic[num][1][1]] = 0
                state.dic[num][1][1]+=1
                return state
        elif state.dic[num][0]=='rectv':
            if state.board[state.dic[num][1][0]][state.dic[num][1][1]+1]!=0 or state.board[state.dic[num][1][0]+1][state.dic[num][1][1]+1]!=0:
                return None
            else:
                state.board[state.dic[num][1][0]][state.dic[num][1][1]+1] = state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]+1][state.dic[num][1][1]+1] = state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]][state.dic[num][1][1]] = 0
                state.board[state.dic[num][1][0]+1][state.dic[num][1][1]] = 0
                state.dic[num][1][1]+=1
                return state
        elif state.dic[num][0]=='grande':
            if state.dic[num][1][1]==len(state.board[0]) - 2 :
                return None
            if state.board[state.dic[num][1][0]][state.dic[num][1][1]+2]!=0 or state.board[state.dic[num][1][0]+1][state.dic[num][1][1]+2]!=0:
                return None
            else:
                state.board[state.dic[num][1][0]][state.dic[num][1][1]+2]= state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]+1][state.dic[num][1][1]+2]=state.board[state.dic[num][1][0]][state.dic[num][1][1]]
                state.board[state.dic[num][1][0]][state.dic[num][1][1]] = 0
                state.board[state.dic[num][1][0]+1][state.dic[num][1][1]] = 0
                state.dic[num][1][1]+=1
                return state
        

    def Win(self):
        #vê se o estado é final/vencedor
        return(self.board[4][1] ==2 and self.board[4][2]==2 and self.board[3][1]==2 and self.board[3][2]==2)
    
def convert_board_to_str(board):
        #converte o board para string
        board_str = ""
        for row in range(len(board)):
            board_str += "| "
            for col in range(len(board[0])):
                if board[row][col] == 0:
                    board_str += '  '
                else:
                    if board[row][col]>9:
                        board_str += str(board[row][col])
                    else:
                        board_str += (str(board[row][col]) + ' ')
                board_str += " | "
            board_str += "\n---------------------\n"
        return board_str

def print_sequence(state):
    #escreve a sequência
    print("Steps:", len(state.move_history) - 1)
    for move in state.move_history.board:
        print(convert_board_to_str(move))
        print()

#NÍVEIS DO JOGO
Dim1={1:('sqr',[0,0]),2:('grande',[2,1]),3:('sqr',[0,3]),4:('sqr',[1,0]),5:('sqr',[1,3]),6:('rectv',[2,0]),7:('sqr',[0,1]),8:('sqr',[0,2]),9:('rectv',[2,3]),10:('sqr',[1,1]),11:('sqr',[1,2]),12:('sqr',[4,0]),13:('sqr',[4,3])}
Nivel1=State([[1,7,8,3],[4,10,11,5],[6,2,2,9],[6,2,2,9],[12,0,0,13]],Dim1)
Dim2={1:('sqr',[0,0]),2:('grande',[2,1]),3:('sqr',[0,3]),4:('sqr',[1,0]),5:('sqr',[1,3]),6:('rectv',[3,0]),7:('sqr',[0,1]),8:('sqr',[0,2]),9:('rectv',[3,3]),10:('sqr',[1,1]),11:('sqr',[1,2]),12:('sqr',[4,1]),13:('sqr',[4,2])}
Nivel2=State([[1,7,8,3],[4,10,11,5],[0,2,2,0],[6,2,2,9],[6,12,13,9]],Dim2)
Dim3={1:('sqr',[0,0]),2:('grande',[2,1]),3:('sqr',[0,3]),4:('sqr',[2,0]),5:('sqr',[2,3]),6:('rectv',[3,0]),7:('sqr',[0,1]),8:('sqr',[0,2]),9:('rectv',[3,3]),10:('sqr',[1,1]),11:('sqr',[1,2]),12:('sqr',[4,1]),13:('sqr',[4,2])}
Nivel3=State([[1,7,8,3],[0,10,11,0],[4,2,2,5],[6,2,2,9],[6,12,13,9]],Dim3)
Dim4={1:('sqr',[0,0]),2:('grande',[2,1]),3:('sqr',[0,3]),4:('sqr',[2,0]),5:('sqr',[2,3]),6:('rectv',[3,0]),7:('sqr',[0,1]),8:('sqr',[0,2]),9:('rectv',[4,3]),10:('sqr',[1,1]),11:('sqr',[1,2]),12:('sqr',[4,1]),13:('sqr',[4,2])}
Nivel4=State([[1,7,8,3],[0,10,11,0],[4,2,2,5],[6,2,2,9],[6,12,13,9]],Dim4)
Dim5={1:('sqr',[0,0]),2:('grande',[1,1]),3:('sqr',[0,3]),4:('sqr',[1,0]),5:('sqr',[1,3]),6:('rectv',[2,0]),7:('sqr',[0,1]),8:('sqr',[0,2]),9:('rectv',[2,3]),10:('sqr',[3,1]),11:('sqr',[3,2]),12:('sqr',[4,0]),13:('sqr',[4,3])}
Nivel5=State([[1,7,8,3],[4,2,2,5],[6,2,2,9],[6,10,11,9],[12,0,0,13]],Dim5)
Dim6={1:('sqr',[0,0]),2:('grande',[0,1]),3:('sqr',[0,3]),4:('sqr',[1,0]),5:('sqr',[1,3]),6:('rectv',[2,0]),7:('sqr',[2,1]),8:('sqr',[2,2]),9:('rectv',[2,3]),10:('sqr',[3,1]),11:('sqr',[3,2]),12:('sqr',[4,0]),13:('sqr',[4,3])}
Nivel6=State([[1,2,2,3],[4,2,2,5],[6,7,8,9],[6,10,11,9],[12,0,0,13]],Dim6)

def jogar_nivel(nivel):
    #jogar no terminal
    print(nivel)
    n=0
    while nivel.Win()==False:
        x=int(input())
        move=str(input())
        if move=='u':
            nivel=nivel.up(x)
        elif move=='d':
            nivel=nivel.down(x)
        elif move=='l':
            nivel=nivel.left(x)
        elif move=='r':
            nivel=nivel.right(x)
        print(nivel)
        n+=1
    print ("GANHASTE em %d moves" % (n))


def bfs(problem):
    #função breadth-first search
    queue = [problem]
    visited=set()
    while queue:
        current = queue.pop(0)
        visited.add(current)
        if current.Win():
            return current
        for child in current.children():
            if child not in visited:
                queue.append(child)
    return None

visitado_dfs=set()
def dfs(problema, visitado_dfs):
    if problema.Win():
        return problema
    visitado_dfs.add(problema)
    for child in problema.children():
        if child not in visitado_dfs:
            solucao = dfs(child, visitado_dfs)
            if solucao is not None:
                return solucao
    return None

    

def h1(state):
    #manhattan distance
    dic=state.dic
    dist = 0
    posicao=dic[2][1]
    dist=abs(posicao[0]-3)+abs(posicao[1]-1)
    return dist

def h2(state):
    #number of pieces blocking the way
    n=0
    num=set()
    dic=state.dic
    board=state.board
    for i in range(dic[2][1][0]+1,len(board)):
        for j in range(0,len(board[0])):
            if board[i][j]!=2 and board[i][j]!=0:
                if board[i][j] not in num:
                    n+=1
                num.add(board[i][j])
    return n

def h3(state):
    #possibilidade de mover quadrado grande para baixo
    if state.down(2):
        return 2
    else:
        return 0

def h4(state):
    #Sum of the two heuristics
    return (h1(state)+h3(state))

def astar(state,heuristic):
    return (heuristic(state) + len(state.move_history) - 1)

def greedy_search(problem, heuristic):
    #função greedy-search
    setattr(State, "__lt__", lambda self, other: heuristic(self) < heuristic(other))
    states = [problem]
    visited = set() 
    while states:
        current = heapq.heappop(states)
        visited.add(current)
        if current.Win():
            return current
        for child in current.children():
            if child not in visited:
                heapq.heappush(states, child)
    return None

def a_star_search(problem, heuristic):
    #função a-star-search
    return greedy_search(problem, lambda state: heuristic(state) + (len(state.move_history) - 1))

def dica_jogo(problem, heuristic):
    #função retorna dica
    setattr(State, "__lt__", lambda self, other: heuristic(self) < heuristic(other))
    states = [problem]
    current = heapq.heappop(states)
    for child in current.children():
        heapq.heappush(states, child)
        current=heapq.heappop(states)
    return current




def test(title, fun, *args):
    start_time = time.time()
    res = fun(*args)
    end_time = time.time()
    time_elapsed = round(end_time - start_time, 4)
    process = psutil.Process()
    start_mem_usage = process.memory_info().rss / 1024 / 1024
    res = fun(*args)
    end_mem_usage = process.memory_info().rss / 1024 / 1024
    memory_used = end_mem_usage - start_mem_usage
    
    print(f"{title}:\t{len(res.move_history) - 1} rounds\t {time_elapsed}s\t {memory_used} MiB")

pygame.init()

WIDTH = 600
HEIGHT = 700
fps = 10
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('KLOTSKI')
main_menu = False
font = pygame.font.Font('freesansbold.ttf', 50)
font1 = pygame.font.Font('freesansbold.ttf', 20)
menu_command = 0
SQUARE_SIZE = 100

def draw_blocks(nivel):
    #função desenha blocos
    pygame.draw.rect(screen, 'white', (90, 90, 410, 520))
    sqr_y = 95
    for i in range(5):
        sqr_x = 95
        for j in range(4):
            sqr_pos = [sqr_x, sqr_y]
            id_peca = nivel.board[i][j]
            if id_peca==0:
                color='white'
            elif id_peca==1:
                color = 'deepskyblue1'
            elif id_peca==2:
                color = 'gold'
            elif id_peca==3:
                color = 'deepskyblue3'
            elif id_peca==4:
                color = 'deepskyblue4'
            elif id_peca==5:
                color='lightblue'
            elif id_peca==6:
                color='olivedrab3'
            elif id_peca==7:
                color='lightblue2'
            elif id_peca==8:
                color='lightblue3'
            elif id_peca==9:
                color='olivedrab4'
            elif id_peca==10:
                color='deepskyblue2'
            elif id_peca==11:
                color='cadetblue1'
            elif id_peca==12:
                color='cyan'
            elif id_peca==13:
                color='cadetblue3'
            pygame.draw.rect(screen, color, (sqr_x, sqr_y, SQUARE_SIZE, SQUARE_SIZE))
            sqr_x += SQUARE_SIZE 
        sqr_y += SQUARE_SIZE 
    pygame.display.update()
    
selected_id_peca=None
move = None


def select_piece1(nivel):
    #vê a peça que está a ser selecionada
    global selected_id_peca,event
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        col = (mouse_pos[0] - 95) // SQUARE_SIZE
        row = (mouse_pos[1]-95) // SQUARE_SIZE
        id_peca = nivel.board[row][col]
        if id_peca != 0:
            selected_id_peca=id_peca

def jogar_klotski(nivel):
    #jogar o jogo
    global event         
    run = True
    n = 0
    while run:
        screen.fill('light blue')
        timer.tick(fps)
        txt1=font1.render(f"MOVES: {n}",True,'black')
        txt_dica=font1.render(f"PRESS h TO HAVE A HINT",True,'black')
        txt_restart=font1.render(f"PRESS r TO RESTART THE GAME",True,'black')
        screen.blit(txt1,(10, 10))
        screen.blit(txt_dica,(10, 625))
        screen.blit(txt_restart,(10, 660))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    print('a')
                    nivel = dica_jogo(nivel,h1)
                    if nivel:
                        n += 1
                    else:
                        nivel = nivelA
                if event.key==pygame.K_r:
                    jogar_klotski(nivel)
                elif selected_id_peca is not None:
                    nivelA = nivel
                    if event.key == pygame.K_DOWN:
                        nivel = nivel.down(selected_id_peca)
                        if nivel:
                            n += 1
                        else:
                            nivel = nivelA
                    elif event.key == pygame.K_UP:
                        nivel = nivel.up(selected_id_peca)
                        if nivel:
                            n += 1
                        else:
                            nivel = nivelA
                    elif event.key == pygame.K_LEFT:
                        nivel = nivel.left(selected_id_peca)
                        if nivel:
                            n += 1
                        else:
                            nivel = nivelA
                    elif event.key == pygame.K_RIGHT:
                        nivel = nivel.right(selected_id_peca)
                        if nivel:
                            n += 1
                        else:
                            nivel = nivelA

        
        select_piece1(nivel)
        nivelA = nivel
        
        draw_blocks(nivel)  
        
        if nivel.Win():
            txt=font.render(f"WON IN {n} MOVES",True,'black')
            screen.fill('white')
            screen.blit(txt,(600//2 - 200, 700//2 ))
            
            run = False
            
        pygame.display.flip()
        
    pygame.time.wait(500)
    pygame.quit()

def escolher_nivel():
    a = int(input("CHOOSE THE LEVEL YOU WANT TO PLAY: "))
    if a == 1:
        nivel = Nivel1
    elif a == 2:
        nivel = Nivel2
    elif a == 3:
        nivel = Nivel3
    elif a == 4:
        nivel = Nivel4
    elif a == 5:
        nivel = Nivel5
    elif a == 6:
        nivel = Nivel6
    return jogar_klotski(nivel)


def jogar_klotski_bfs(nivel):
    #AI joga klotski com recurso ao bfs  
    run = True
    queue = [nivel]
    visited=set()
    draw_blocks(nivel)
    clock = pygame.time.Clock()
    history=bfs(nivel).move_history
    print(history)
    i=0
    while run:
        screen.fill('light blue')
        timer.tick(fps)
        current=history[i]
        draw_blocks(current)
        if current.Win():
            n=len(current.move_history) - 1
            txt=font.render(f"WON IN {n} MOVES",True,'black')
            screen.fill('white')
            screen.blit(txt,(600//2 - 200, 700//2 ))
            run = False
        pygame.display.flip()
        i+=1
    pygame.time.wait(2000)
    pygame.quit()

def jogar_klotski_dfs(nivel):
    run=True
    visited=set()
    draw_blocks(nivel)
    clock = pygame.time.Clock()
    history=dfs(nivel,visitado_dfs).move_history
    i=0
    while run:
        screen.fill('light blue')
        timer.tick(fps)
        current=history[i]
        draw_blocks(current)
        if current.Win():
            n=len(current.move_history) - 1
            txt=font.render(f"WON IN {n} MOVES",True,'black')
            screen.fill('white')
            screen.blit(txt,(600//2 - 200, 700//2 ))
            
            run = False
        pygame.time.wait(500)
        pygame.display.flip()
        i+=1
    pygame.time.wait(2000)
    pygame.quit()


def jogar_klotski_greedy(nivel,heuristic):
    #AI joga klotski com recurso ao greedy-search
    run=True
    setattr(State, "__lt__", lambda self, other: heuristic(self) < heuristic(other))
    states = [nivel]
    screen.fill('light blue')
    draw_blocks(nivel)
    clock = pygame.time.Clock()
    history=greedy_search(nivel,heuristic).move_history
    i=0
    while run:
        screen.fill('light blue')
        timer.tick(fps)
        current=history[i]
        draw_blocks(current)
        if current.Win():
            n=len(current.move_history) - 1
            txt=font.render(f"WON IN {n} MOVES",True,'black')
            screen.fill('white')
            screen.blit(txt,(600//2 - 200, 700//2 ))
            
            run = False
        pygame.time.wait(500)
        pygame.display.flip()
        i+=1
    pygame.time.wait(2000)
    pygame.quit()

def jogar_klotski_astar(nivel,heuristic):
    #AI joga klotski com recurso ao a-star-search
    jogar_klotski_greedy(nivel,lambda state: heuristic(state) + (len(state.move_history) - 1))

escolher_nivel()