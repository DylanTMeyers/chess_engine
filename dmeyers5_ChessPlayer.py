from chess_player import ChessPlayer
import random
import copy
import math
import time
class dmeyers5_ChessPlayer(ChessPlayer):

    def __init__(self, board, color):
        super().__init__(board, color)
        self.values_dict = {"queen":9, "princess":6, "rook": 5, "fool":3, "bishop": 3, "knight": 3, "pawn": 1, "king":0}
        self.num = 0
        self.all_moves = []

    def get_move(self, your_remaining_time, opp_remaining_time, prog_stuff):
        
        ##print("number 2 program")
        my_color = self.color
        ##print(self.color)
        colors  = {}
        if my_color =="white":
            colors["max"] = 'white'
            colors["min"] = "black"
            
        else:
            colors["max"] = 'black'
            colors["min"] = "white"
       
        
        copy_board = copy.deepcopy(self.board)
        ##print("grade")
        ##print(self.grade_min_grade_max(self.board,colors))
        

        max_moves = copy_board.get_all_available_legal_moves(colors["max"])
        checkmate = self.check_if_checkmate(max_moves, copy_board, colors)

        if checkmate[0] == True:
            return checkmate[1]
        min_moves = copy_board.get_all_available_legal_moves(colors["min"])
        
        for i in range(len(max_moves)):

            if copy_board[max_moves[i][0]].name == "pawn" and max_moves[i][1] in copy_board and copy_board[max_moves[i][1]].name == "pawn":
                #print("pawn taken")
                return max_moves[i]    

        ##print("beginning max")
        ##print(max_moves)
        if len(max_moves) == 1:
            return max_moves[0]
        ##print("beginning min")
        ##print(min_moves)

        total = len(max_moves) * len(min_moves)
        if len(min_moves) == 0:
            total = len(max_moves)

        ##print("totals")
        ##print(total)
        max_depth = math.trunc(100/total) * 2
        if max_depth < 2:
            max_depth = 2
        elif max_depth>4:
            max_depth =3
            if self.board.is_king_in_check(colors["max"]) and total> 10:
                max_depth == 2
        ##print("DEPTHHHHH")
        ##print(max_depth)

        start_time = time.time()
        if your_remaining_time >300:
            max = 3
        elif your_remaining_time >100:
            max = 2
            max_depth = 2
        else:
            max = 1
            max_depth = 1
        
        move =  list(self.miniMax(colors,0,True,copy_board,max_depth, {},{0:1000000000}, {0:-1000000000}, start_time, None,max ).items())
        self.all_moves.append(move[0][0])
        # #print(move[0][0])
        #print(move)
        print(self.all_moves[:10])
        return move[0][0]

    def miniMax(self, color_dict, depth, maxTurn, board, targetDepth, move, currLow, currHigh,start_time,last_move_type,absolute_max ):

        if (depth == targetDepth):
            
            if targetDepth<absolute_max  and last_move_type != "pawn" and self.piece_under_attack(board,color_dict,move):
                #####print  (self.num)
                targetDepth = targetDepth + 1
            else:
                game_board = board.get_all_available_legal_moves(color_dict["min"])
                if targetDepth == 3:
                    return {("deep", move[0], move[1]):self.evaluate(board, color_dict,move,currLow)}
                return {(move[0], move[1]):self.evaluate(board, color_dict,move,currLow)}
        
        if (maxTurn):
            temp_dict = {}
            # game_board = board.get_all_available_legal_moves(color_dict["max"])
            game_board = self.reorder_board(board,color_dict["max"])
            min_num = {(0,0):1000000000}
            new_dict = {(0,0):1000000000}
            
            for i in range(len(game_board)):
                next_board = copy.deepcopy(board)
                if self.all_moves[:20].count(game_board[i]) >=4:
                    
                    continue
                next_board.make_move(game_board[i][0],game_board[i][1])
                
                if next_board.is_king_in_check(color_dict["min"]) == False and len(next_board.get_all_available_legal_moves(color_dict["min"])) == 0:
                    
                    continue
                
                #print("new_dict1")
                #print(new_dict)
                


                last_move_type = next_board[game_board[i][1]].name
                new_dict = self.miniMax(color_dict, depth + 1,
                        False, next_board, targetDepth, game_board[i], min_num, currHigh,start_time, last_move_type, absolute_max)

                if new_dict != None and list(new_dict.keys())[0][0] == "deep" and list(new_dict.values())[0]+5< self.evaluate(self.board,color_dict,0,0):

                    return {game_board[i]: list(new_dict.values())[0]}
                if  new_dict != None and list(new_dict.values())[0]<= list(currHigh.values())[0]:
                    #print("breakkkk max")
                    min_num = {game_board[i]:list(new_dict.values())[0]}
                    break
                if new_dict != None and list(new_dict.keys())[0][0] != 0  and  list(new_dict.values())[0]< list(min_num.values())[0]:
                    min_num = {game_board[i]:list(new_dict.values())[0]}
                
            
            return min_num
        
        else:
            temp_dict = {}
            
            high_num = {(0,0):-1000000000}
            new_dict  = {(0,0):-1000000000}

            game_board = self.reorder_board(board,color_dict["min"])
            
            
            for i in range(len(game_board)):
                next_board = copy.deepcopy(board)
                next_board.make_move(game_board[i][0],game_board[i][1])
                

                last_move_type = next_board[game_board[i][1]].name

                new_dict = self.miniMax(color_dict, depth + 1,
                        True, next_board, targetDepth, game_board[i], currLow, high_num,start_time, last_move_type, absolute_max)
                if new_dict != None and list(new_dict.values())[0]>=  list(currLow.values())[0]:
                    high_num = new_dict
                    break
                if new_dict != None and list(new_dict.keys())[0][0] != 0  and list(new_dict.values())[0]>list(high_num.values())[0]:
                    high_num = new_dict
                
            return high_num

    def evaluate(self, board,colors, move,low):
        beg_min_num = self.grade_min_grade_max(self.board, colors)[1] - self.grade_min_grade_max(self.board, colors)[0]
        

        now_min_num = self.grade_min_grade_max(board, colors)[1] - self.grade_min_grade_max(board, colors)[0]
        eval = ( now_min_num -beg_min_num )*10
        if move != 0:
            if colors["min"] == "white" and ord(move[0][1]) <3 and ord(move[1][1])>2 and  ord(move[1][1])<5:
                eval = eval + 30
            elif colors["min"] == "black" and ord(move[0][1]) >4 and ord(move[1][1])<5 and  ord(move[1][1])>2:
                eval = eval + 30

        if self.board.is_king_in_checkmate(colors["max"]):
            eval = eval +20

        if self.board.is_king_in_checkmate(colors["min"]):
            eval = eval - 20
        if self.board.is_king_in_checkmate(colors["max"]):
            eval = 10000000000000

        if self.board.is_king_in_checkmate(colors["min"]):
            eval = -1000000000000
    

        return len(board.get_all_available_legal_moves(colors["min"])) + eval


    def grade_min_grade_max(self,board, colors):
        white = 0
        black = 0
        for val in board.values():
            
            if val.color == "white":
                
                white = white + self.values_dict[val.name]

            if val.color == "black":
                black = black + self.values_dict[val.name]

        if colors["max"] == "white":
            return(white,black)

        else:
            return(black,white)
    def piece_under_attack(self,board,colors,min_move):
        moves = board.get_all_available_legal_moves(colors["max"])

        for move in moves:
            if move[1] == min_move[1]:
                return True

        return False
    def check_if_checkmate(self, board,copyboard,color):
        for move in board:
            copyboard = copy.deepcopy(self.board)
            copyboard.make_move(move[0], move[1])
            if copyboard.is_king_in_checkmate(color["min"]):
                return (True, move)
        return (False, None)
            
    def reorder_board(self,board,color):
        ordered_dict = {}
        for move in board.get_all_available_legal_moves(color):
            if move[1] in board:
                new_val = self.values_dict[board[move[0]].name] - self.values_dict[board[move[1]].name]
                ordered_dict[move] = new_val
            else:
                ordered_dict[move] = 0
        return list({k: v for k, v in sorted(ordered_dict.items(), key=lambda item: item[1],reverse=True)}.keys())


