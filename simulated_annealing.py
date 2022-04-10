import random
import time
from math import exp
from copy import deepcopy
class NQueensProblem:
    def __init__(self,num=15,temperature=4000):
        self.N_QUEENS=num
        self.temperature=temperature
        self.history=[]
    def threat_calculate(self,n):
        #tính cách chọn 2 quân hậu
        if n < 2:
            return 0
        if n == 2:
            return 1
        return (n - 1) * n / 2
    def create_board(self,n):
        #Tạo bàn cờ và đặt tất cả quân hậu trên cùng 1 hàng
        chess_board = {}
        temp = list(range(n))
        random.shuffle(temp)  # trộn mảng temp
        column = 0
        while len(temp) > 0:
            row = random.choice(temp)
            chess_board[column] = row
            temp.remove(row)
            column += 1
        del temp
        return chess_board
    def cost(self,chess_board):
        #tính số cặp hậu không hợp lệ
        threat = 0
        m_chessboard = {}
        a_chessboard = {}
        for column in chess_board:
            temp_m = column - chess_board[column]
            temp_a = column + chess_board[column]
            if temp_m not in m_chessboard:
                m_chessboard[temp_m] = 1
            else:
                m_chessboard[temp_m] += 1
            if temp_a not in a_chessboard:
                a_chessboard[temp_a] = 1
            else:
                a_chessboard[temp_a] += 1
        for i in m_chessboard:
            threat += self.threat_calculate(m_chessboard[i])
        del m_chessboard
        for i in a_chessboard:
            threat += self.threat_calculate(a_chessboard[i])
        del a_chessboard
        return threat
    def simulated_annealing(self):
        solution_found = False #khởi tạo kết quả tìm kiếm là false, chưa tìm thấy giải pháp
        answer = self.create_board(self.N_QUEENS) #tạo bảng gồm n quân hậu
        self.history.append(list(answer.values()))
        cost_answer = self.cost(answer) # tính số cặp quân hậu ko hợp lệ
        t = self.temperature
        sch = 0.99
        while t > 0:
            t *= sch
            successor =deepcopy(answer) #copy bàn cờ ban đầu
            while True:
                index_1 = random.randrange(0, self.N_QUEENS - 1) #tìm ngẫu nhiên quân hậu thứ nhất
                index_2 = random.randrange(0, self.N_QUEENS - 1) #tìm ngẫu nhiên quân hậu thứ 2
                if index_1 != index_2: # đảm bảo, 2 quân hậu không cùng 1 con
                    break
            successor[index_1], successor[index_2] = successor[index_2], \
                successor[index_1]  # đổi chổ 2 quân hậu
            delta = self.cost(successor) - cost_answer # tính delta
            if delta < 0 or random.uniform(0, 1) < exp(-delta / t): #kiểm tra xem, delta có hợp lệ (theo thuật toán simulated_annealing) không
                answer = deepcopy(successor)
                self.history.append(list(answer.values()))
                cost_answer = self.cost(answer)
            if cost_answer == 0:
                solution_found = True
                self.print_chess_board(answer)
                break
        if solution_found is False: #sau giới hạn lần thực hiện thao tác nhưng ko tìm thấy kết quả thì xuất ra 'Failed'
            print("Failed")
    def print_chess_board(self,board):
        #xuất ra vị trí các quân hậu
        for column, row in board.items():
            print(f"{column} => {row}")
    def solve(self):
        self.simulated_annealing()
if __name__ == "__main__":
    NQueensProblem(8).solve()
    