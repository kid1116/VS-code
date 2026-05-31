import pygame
import random

# 游戏配置
COLS = 10
ROWS = 20
CELL_SIZE = 30
GAME_WIDTH = COLS * CELL_SIZE
GAME_HEIGHT = ROWS * CELL_SIZE
SIDEBAR_WIDTH = 200
WINDOW_WIDTH = GAME_WIDTH + SIDEBAR_WIDTH
WINDOW_HEIGHT = GAME_HEIGHT

# 颜色定义 (R, G, B)
COLORS = {
    'I': (0, 255, 255),    # 青色
    'O': (255, 255, 0),    # 黄色
    'T': (160, 32, 240),   # 紫色
    'S': (0, 255, 0),      # 绿色
    'Z': (255, 0, 0),      # 红色
    'J': (0, 0, 255),      # 蓝色
    'L': (255, 165, 0),    # 橙色
}
BG_COLOR = (20, 20, 20)
GRID_COLOR = (40, 40, 40)
TEXT_COLOR = (255, 255, 255)

# 定义所有方块形状（使用旋转状态）
SHAPES = {
    'I': [[(0, 0), (1, 0), (2, 0), (3, 0)],
          [(0, 0), (0, 1), (0, 2), (0, 3)]],
    'O': [[(0, 0), (1, 0), (0, 1), (1, 1)]],
    'T': [[(0, 0), (1, 0), (2, 0), (1, 1)],
          [(0, 0), (0, 1), (0, 2), (1, 1)],
          [(1, 0), (0, 1), (1, 1), (2, 1)],
          [(1, 0), (0, 1), (1, 1), (1, 2)]],
    'S': [[(1, 0), (2, 0), (0, 1), (1, 1)],
          [(0, 0), (0, 1), (1, 1), (1, 2)]],
    'Z': [[(0, 0), (1, 0), (1, 1), (2, 1)],
          [(1, 0), (0, 1), (1, 1), (0, 2)]],
    'J': [[(0, 0), (0, 1), (1, 1), (2, 1)],
          [(0, 0), (1, 0), (0, 1), (0, 2)],
          [(0, 0), (1, 0), (2, 0), (2, 1)],
          [(1, 0), (1, 1), (0, 2), (1, 2)]],
    'L': [[(2, 0), (0, 1), (1, 1), (2, 1)],
          [(0, 0), (0, 1), (0, 2), (1, 2)],
          [(0, 0), (1, 0), (2, 0), (0, 1)],
          [(0, 0), (1, 0), (1, 1), (1, 2)]],
}


class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('俄罗斯方块')
        self.clock = pygame.time.Clock()
        # 安全加载字体，pygame 2.6.1 在 Win11 上 SysFont 可能因系统字体异常而崩溃
        try:
            self.font = pygame.font.SysFont('simhei', 24)
        except Exception:
            self.font = pygame.font.Font(None, 28)
        try:
            self.small_font = pygame.font.SysFont('simhei', 18)
        except Exception:
            self.small_font = pygame.font.Font(None, 20)
        self.reset()

    def reset(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.current_piece = None
        self.next_piece = None
        self.spawn_piece()
        self.fall_time = 0
        self.fall_speed = 800  # 毫秒，随等级加快

    def spawn_piece(self):
        if self.next_piece is None:
            self.next_piece = self.random_piece()
        self.current_piece = self.next_piece
        self.next_piece = self.random_piece()
        self.current_x = COLS // 2 - 1
        self.current_y = 0
        self.current_rotation = 0
        if self.collides(self.current_piece, self.current_x, self.current_y, self.current_rotation):
            self.game_over = True

    def random_piece(self):
        shape_name = random.choice(list(SHAPES.keys()))
        return shape_name

    def get_blocks(self, shape_name, rotation):
        return SHAPES[shape_name][rotation % len(SHAPES[shape_name])]

    def collides(self, shape_name, px, py, rotation):
        for bx, by in self.get_blocks(shape_name, rotation):
            x = px + bx
            y = py + by
            if x < 0 or x >= COLS or y >= ROWS:
                return True
            if y >= 0 and self.board[y][x] is not None:
                return True
        return False

    def lock_piece(self):
        shape_name = self.current_piece
        for bx, by in self.get_blocks(shape_name, self.current_rotation):
            x = self.current_x + bx
            y = self.current_y + by
            if y >= 0:
                self.board[y][x] = COLORS[shape_name]
        self.clear_lines()
        self.spawn_piece()

    def clear_lines(self):
        full_rows = [r for r in range(ROWS) if all(self.board[r][c] is not None for c in range(COLS))]
        if full_rows:
            for r in sorted(full_rows, reverse=True):
                del self.board[r]
                self.board.insert(0, [None for _ in range(COLS)])
            cleared = len(full_rows)
            self.lines_cleared += cleared
            # 计分：单消100，双消300，三消500，四消800
            scores = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += scores.get(cleared, cleared * 200) * self.level
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(50, 800 - (self.level - 1) * 70)

    def move_down(self):
        if not self.collides(self.current_piece, self.current_x, self.current_y + 1, self.current_rotation):
            self.current_y += 1
            return True
        return False

    def drop(self):
        while self.move_down():
            pass
        self.lock_piece()

    def move(self, dx):
        if not self.collides(self.current_piece, self.current_x + dx, self.current_y, self.current_rotation):
            self.current_x += dx

    def rotate(self):
        new_rot = (self.current_rotation + 1) % len(SHAPES[self.current_piece])
        # 踢墙：尝试基本旋转，然后尝试左移/右移
        for dx in (0, -1, 1, -2, 2):
            if not self.collides(self.current_piece, self.current_x + dx, self.current_y, new_rot):
                self.current_x += dx
                self.current_rotation = new_rot
                return

    def update(self, dt):
        if self.game_over or self.paused:
            return
        self.fall_time += dt
        while self.fall_time >= self.fall_speed:
            self.fall_time -= self.fall_speed
            if not self.move_down():
                self.lock_piece()
                if self.game_over:
                    break

    def draw_cell(self, x, y, color, alpha=255):
        rect = pygame.Rect(x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2)
        s = pygame.Surface((CELL_SIZE - 2, CELL_SIZE - 2), pygame.SRCALPHA)
        s.fill((*color, alpha))
        # 高光效果
        highlight = pygame.Surface((CELL_SIZE - 2, 4), pygame.SRCALPHA)
        highlight.fill((255, 255, 255, 80))
        s.blit(highlight, (0, 0))
        shadow = pygame.Surface((CELL_SIZE - 2, 4), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 80))
        s.blit(shadow, (0, CELL_SIZE - 6))
        self.screen.blit(s, rect)

    def draw_ghost(self):
        """绘制落点预览"""
        gy = self.current_y
        while not self.collides(self.current_piece, self.current_x, gy + 1, self.current_rotation):
            gy += 1
        if gy != self.current_y:
            for bx, by in self.get_blocks(self.current_piece, self.current_rotation):
                x = self.current_x + bx
                y = gy + by
                if y >= 0:
                    self.draw_cell(x, y, COLORS[self.current_piece], alpha=60)

    def draw_board(self):
        self.screen.fill(BG_COLOR, (0, 0, GAME_WIDTH, GAME_HEIGHT))

        # 网格线
        for x in range(COLS):
            for y in range(ROWS):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)

        # 已锁定的方块
        for y in range(ROWS):
            for x in range(COLS):
                if self.board[y][x] is not None:
                    self.draw_cell(x, y, self.board[y][x])

        # 落点预览
        if self.current_piece and not self.game_over:
            self.draw_ghost()

        # 当前方块
        if self.current_piece and not self.game_over:
            for bx, by in self.get_blocks(self.current_piece, self.current_rotation):
                x = self.current_x + bx
                y = self.current_y + by
                if y >= 0:
                    self.draw_cell(x, y, COLORS[self.current_piece])

    def draw_sidebar(self):
        x_offset = GAME_WIDTH + 10
        y = 20
        gap = 35

        texts = [
            f'分数: {self.score}',
            f'等级: {self.level}',
            f'行数: {self.lines_cleared}',
        ]
        for text in texts:
            surf = self.font.render(text, True, TEXT_COLOR)
            self.screen.blit(surf, (x_offset, y))
            y += gap

        # 下一个方块预览
        y += 10
        label = self.font.render('下一个:', True, TEXT_COLOR)
        self.screen.blit(label, (x_offset, y))
        y += 35

        if self.next_piece:
            blocks = self.get_blocks(self.next_piece, 0)
            preview_size = 22
            for bx, by in blocks:
                rect = pygame.Rect(
                    x_offset + bx * preview_size,
                    y + by * preview_size,
                    preview_size - 2,
                    preview_size - 2
                )
                color = COLORS[self.next_piece]
                s = pygame.Surface((preview_size - 2, preview_size - 2), pygame.SRCALPHA)
                s.fill((*color, 255))
                self.screen.blit(s, rect)

        # 控制说明
        y = WINDOW_HEIGHT - 260
        controls = [
            '← →  移动',
            '↑    旋转',
            '↓    软降',
            '空格  硬降',
            'P    暂停',
            'R    重新开始',
            'ESC  退出',
        ]
        header = self.small_font.render('操作:', True, TEXT_COLOR)
        self.screen.blit(header, (x_offset, y))
        y += 25
        for line in controls:
            surf = self.small_font.render(line, True, (180, 180, 180))
            self.screen.blit(surf, (x_offset, y))
            y += 22

    def draw_game_over(self):
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        text = self.font.render('游戏结束', True, TEXT_COLOR)
        sub = self.small_font.render('按 R 重新开始', True, (180, 180, 180))
        self.screen.blit(text, (GAME_WIDTH // 2 - 50, GAME_HEIGHT // 2 - 30))
        self.screen.blit(sub, (GAME_WIDTH // 2 - 60, GAME_HEIGHT // 2 + 5))

    def draw_pause(self):
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        text = self.font.render('已暂停', True, TEXT_COLOR)
        self.screen.blit(text, (GAME_WIDTH // 2 - 40, GAME_HEIGHT // 2 - 15))

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60)
            self.update(dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.reset()
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    elif not self.paused and self.current_piece:
                        if event.key == pygame.K_LEFT:
                            self.move(-1)
                        elif event.key == pygame.K_RIGHT:
                            self.move(1)
                        elif event.key == pygame.K_DOWN:
                            if self.move_down():
                                self.score += 1
                        elif event.key == pygame.K_UP:
                            self.rotate()
                        elif event.key == pygame.K_SPACE:
                            self.drop()

            self.draw_board()
            self.draw_sidebar()

            if self.game_over:
                self.draw_game_over()
            elif self.paused:
                self.draw_pause()

            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    Tetris().run()
