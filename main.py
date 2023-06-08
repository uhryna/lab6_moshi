import  pygame
import random

class MiniMax:
    def __init__(self, GameBoard):
        self.GameBoard = GameBoard

    def evaluate(self):
        for row in range(3):
            if self.GameBoard[row][0] == self.GameBoard[row][1] and self.GameBoard[row][1] == self.GameBoard[row][2]:
                if self.GameBoard[row][0] == 'x':
                    return 1
                elif self.GameBoard[row][0] == 'o':
                    return -1
        for col in range(3):
            if self.GameBoard[0][col] == self.GameBoard[1][col] and self.GameBoard[1][col] == self.GameBoard[2][col]:
                if self.GameBoard[0][col] == 'x':
                    return 1
                elif self.GameBoard[0][col] == 'o':
                    return -1
        if self.GameBoard[0][0] == self.GameBoard[1][1] and self.GameBoard[2][2] == self.GameBoard[1][1]:
            if self.GameBoard[1][1] == 'x':
                return 1
            elif self.GameBoard[1][1] == 'o':
                return -1
        if self.GameBoard[0][2] == self.GameBoard[1][1] and self.GameBoard[2][0] == self.GameBoard[1][1]:
            if self.GameBoard[1][1] == 'x':
                return 1
            elif self.GameBoard[1][1] == 'o':
                return -1
        for i in range(3):
            for j in range(3):
                if self.GameBoard[i][j] == '-':
                    return 2
        return 0

    def max(self):
        x = None
        y = None
        max_eval = -2
        Eval = self.evaluate()
        if Eval != 2:
            return (Eval, 0, 0)
        for row in range(0, 3):
            for col in range(0, 3):
                if self.GameBoard[row][col] == '-':
                    self.GameBoard[row][col] = 'x'
                    min_eval = self.min()[0]
                    if max_eval < min_eval:
                        max_eval = min_eval
                        x = col
                        y = row
                    self.GameBoard[row][col] = '-'
        return (max_eval, x, y)

    def min(self):
        x = None
        y = None
        min_eval = 2
        Eval = self.evaluate()
        if Eval != 2:
            return (Eval, 0, 0)
        for row in range(0, 3):
            for col in range(0, 3):
                if self.GameBoard[row][col] == '-':
                    self.GameBoard[row][col] = 'o'
                    max_eval = self.max()[0]
                    if min_eval > max_eval:
                        min_eval = max_eval
                        x = col
                        y = row
                    self.GameBoard[row][col] = '-'
        return(min_eval, x, y)

class GameLoop:
    def __init__(self):
        self.GameState = 2
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        background_color = (0, 128, 0)
        self.foreground_color = (255, 255, 255)
        (width, height) = (600, 600)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('tic tac toe')
        self.screen.fill(background_color)
        pygame.display.flip()

    def RenderUI(self, gameboard):
        self.gameboard = gameboard

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    Mouse_x, Mouse_y = pygame.mouse.get_pos()
                    x = round(Mouse_x/200 - 0.49)
                    y = round(Mouse_y/200 - 0.49)
                    self.GameOver()
                    if self.GameState == 2:
                        ValidMove = self.MakeMove(x, y, 'o')
                        if ValidMove:
                            return self.gameboard
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.DrawBoard()
            for row in range(3):
                for col in range(3):
                    if self.gameboard[row][col] == 'x':
                        self.DrawX(col, row)
                    if self.gameboard[row][col] == 'o':
                        self.DrawO(col, row)
            pygame.display.update()

    def DrawBoard(self):
        '''Draws the lines of the GameBoard'''
        self.screen.fill((0, 0, 0))  # Змінюємо фон на чорний кольор

        for xy in range(200, 401, 200):
            pygame.draw.line(self.screen, self.foreground_color,
                             (0, xy), (600, xy), 3)
            pygame.draw.line(self.screen, self.foreground_color,
                             (xy, 0), (xy, 600), 3)

    def DrawX(self, x, y):
        x += 1
        y += 1
        line_thickness = 10  # Set the desired line thickness for the X symbol
        x1 = 200 * x - 200 + 40
        y1 = 200 * y - 200 + 40
        x2 = x * 200 - 40
        y2 = y * 200 - 40
        pygame.draw.line(self.screen, (255, 255, 255), (x1, y1), (x2, y2), line_thickness)
        pygame.draw.line(self.screen, (255, 255, 255), (x1, y2), (x2, y1), line_thickness)
        pygame.draw.line(self.screen, (0, 0, 0), (x1 - 2, y1 - 2), (x2 - 2, y2 - 2), line_thickness - 4)
        pygame.draw.line(self.screen, (0, 0, 0), (x1 - 2, y2 - 2), (x2 - 2, y1 - 2), line_thickness - 4)

    def DrawO(self, x, y):
        x += 1
        y += 1
        line_thickness = 15  # Set the desired line thickness for the outline of the 'O' symbol
        circle_radius = 70  # Set a smaller radius for the 'O' symbol
        circle_center = (x * 200 - 100, y * 200 - 100)
        pygame.draw.circle(self.screen, (255, 255, 255), circle_center, circle_radius)
        pygame.draw.circle(self.screen, (0, 0, 0), circle_center, circle_radius - line_thickness)
        pygame.draw.circle(self.screen, (0, 0, 0), circle_center, circle_radius - line_thickness + line_thickness // 2)
        pygame.draw.circle(self.screen, (0, 0, 0), circle_center,
                           circle_radius - line_thickness + line_thickness // 2 - 2)

    def MakeMove(self, x, y, player):
        if self.gameboard[y][x] == '-':
            self.gameboard[y][x] = player
            return True
        return False

    def GameOver(self):
        self.GameState = MiniMax(self.gameboard).evaluate()
        if self.GameState == 1:
            self.ShowMessage('X Won this Game')
        elif self.GameState == 0:
            self.ShowMessage('None Won')
        elif self.GameState == -1:
            self.ShowMessage('O Won this Game')

    def ShowMessage(self, text):
        background_rect = pygame.Rect(0, 0, self.screen.get_width(),
                                      self.screen.get_height())  # Створення прямокутника фону
        pygame.draw.rect(self.screen, (0, 0, 0), background_rect)  # Заповнення фону чорним кольором

        message = self.font.render(text, True, self.foreground_color)
        message_rect = message.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(message, message_rect)
        pygame.display.flip()
        pygame.time.wait(500)

if __name__ == "__main__":
    Board = [['-', '-', '-'],
             ['-', '-', '-'],
             ['-', '-', '-']]
    pygame.init()  # Ініціалізуємо Pygame
    GL = GameLoop()
    MM = MiniMax(Board)

    bestmove = MM.max()
    Board[bestmove[2]][bestmove[1]] = 'x'

    while True:
        Board = GL.RenderUI(Board)
        bestmove = MM.max()
        Board[bestmove[2]][bestmove[1]] = 'x'