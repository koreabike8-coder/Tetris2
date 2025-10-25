import sys
import numpy as np
import pygame

# Tetris settings
CELL_SIZE = 30
COLS = 10
ROWS = 30
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS
FPS = 60
#SOFT_DROP_FACTOR = 2  # Holding down arrow multiplies gravity by this factor
SOFT_DROP_FACTOR = 4  # Holding down arrow multiplies gravity by this factor

# Colors
BLACK = (0, 0, 0)
#GRAY = (50, 50, 50)
GRAY = (230, 230, 230)
GRAY2 = (248, 248, 248)
GRAY_1 = (20, 20, 20)
GRAY2_1 = (8, 8, 8)

WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # I
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (128, 0, 128),  # T
    (255, 0, 0),    # Z  
]

# Tetromino shapes using small numpy arrays
TETROMINOS = [
    np.array([[1, 1, 1, 1]]),  # I
    np.array([[1, 0, 0], [1, 1, 1]]),  # J
    np.array([[0, 0, 1], [1, 1, 1]]),  # L
    np.array([[1, 1], [1, 1]]),  # O
    np.array([[0, 1, 1], [1, 1, 0]]),  # S
    np.array([[0, 1, 0], [1, 1, 1]]),  # T
    np.array([[1, 1, 0], [0, 1, 1]]),  # Z
]

class Tetris:
    def __init__(self, rows=ROWS, cols=COLS, sfx=None):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=int)
        self.score = 0
        self.game_over = False
        self.locked_pieces = 0
        self.sfx = sfx or {}
        self.next_piece = self.new_piece()
        self.spawn_piece()

    def new_piece(self):
        idx = np.random.randint(len(TETROMINOS))
        shape = TETROMINOS[idx].copy()
        color = idx
        return {'shape': shape, 'r': 0, 'c': self.cols // 2 - shape.shape[1] // 2, 'color': color}

    def spawn_piece(self):
        self.piece = self.next_piece
        self.next_piece = self.new_piece()
        if self.check_collision(self.piece['shape'], self.piece['r'], self.piece['c']):
            self.game_over = True

    def rotate_ccw(self):
        shape = np.rot90(self.piece['shape'], 1)  # rot90 with k=1 is CCW
        # Try wall kicks (simple): if collides, try shifting left/right
        for dc in (0, -1, 1, -2, 2):
            if not self.check_collision(shape, self.piece['r'], self.piece['c'] + dc):
                self.piece['shape'] = shape
                self.piece['c'] += dc
                # play rotate sfx
                snd = self.sfx.get('rotate')
                if snd:
                    snd.play()
                return

    def check_collision(self, shape, r, c):
        h, w = shape.shape
        for i in range(h):
            for j in range(w):
                if shape[i, j]:
                    br = r + i
                    bc = c + j
                    if br < 0 or br >= self.rows or bc < 0 or bc >= self.cols:
                        return True
                    if self.board[br, bc]:
                        return True
        return False

    def lock_piece(self):
        shape = self.piece['shape']
        r = self.piece['r']
        c = self.piece['c']
        h, w = shape.shape
        for i in range(h):
            for j in range(w):
                if shape[i, j]:
                    self.board[r + i, c + j] = self.piece['color'] + 1
        lines = self.clear_lines()
        if lines:
            # line clear sound depending on count
            snd = self.sfx.get(f'clear_{lines}') or self.sfx.get('clear')
            if snd:
                snd.play()
        else:
            snd = self.sfx.get('lock')
            if snd:
                snd.play()
        self.locked_pieces += 1
        self.spawn_piece()

    def clear_lines(self):
        full_rows = [i for i in range(self.rows) if all(self.board[i])]
        lines_cleared = len(full_rows)
        if not lines_cleared:
            return 0

        for row in reversed(full_rows):
            self.board[1:row + 1] = self.board[:row]
            self.board[0] = 0

        score_table = {1: 10, 2: 30, 3: 60, 4: 100}
        self.score += score_table.get(lines_cleared, 0)
        return lines_cleared

    def step_down(self):
        # Try to move down. Return True if moved, False if blocked.
        if not self.check_collision(self.piece['shape'], self.piece['r'] + 1, self.piece['c']):
            self.piece['r'] += 1
            return True
        else:
            return False

    def hard_drop(self):
        while self.step_down():
            pass
        # After hard drop finishes, lock the piece immediately
        snd = self.sfx.get('drop')
        if snd:
            snd.play()
        self.lock_piece()

    def move(self, dc):
        if not self.check_collision(self.piece['shape'], self.piece['r'], self.piece['c'] + dc):
            self.piece['c'] += dc

    def get_board_with_piece(self):
        b = self.board.copy()
        shape = self.piece['shape']
        h, w = shape.shape
        for i in range(h):
            for j in range(w):
                if shape[i, j]:
                    br = self.piece['r'] + i
                    bc = self.piece['c'] + j
                    if 0 <= br < self.rows and 0 <= bc < self.cols:
                        b[br, bc] = self.piece['color'] + 1
        return b

    def get_ghost_cells(self):
        ghost_r = self.piece['r']
        while not self.check_collision(self.piece['shape'], ghost_r + 1, self.piece['c']):
            ghost_r += 1

        if ghost_r == self.piece['r']:
            return []

        cells = []
        shape = self.piece['shape']
        h, w = shape.shape
        for i in range(h):
            for j in range(w):
                if shape[i, j]:
                    cells.append((ghost_r + i, self.piece['c'] + j, self.piece['color']))
        return cells


def draw_grid(surface):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRAY_1, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRAY2_1, (0, y), (WIDTH, y))


def draw_board(surface, board, ghost_cells=None):
    if ghost_cells:
        for r, c, color_idx in ghost_cells:
            rect = (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
#            ghost_color = COLORS[color_idx]
#            ghost_color = tuple(int(COLORS[color_idx][k] * 0.1) for k in range(3))
            ghost_color = (10,20,20, 0.0)
#            fill_color = tuple(int(ghost_color[k] * 0.02 + 255 * 0.98) for k in range(3))
            fill_color = tuple(int(ghost_color[k] ) for k in range(3))
            pygame.draw.rect(surface, fill_color, rect)
            pygame.draw.rect(surface, ghost_color, rect, 1)
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            val = board[i, j]
            if val:
                color = COLORS[val - 1]
                pygame.draw.rect(surface, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(surface, BLACK, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


def draw_next_piece(surface, next_piece):
    if not next_piece:
        return
    preview_cell = CELL_SIZE // 2
    shape = next_piece['shape']
    color = COLORS[next_piece['color']]
    h, w = shape.shape
    preview_width = w * preview_cell
    preview_height = h * preview_cell
    margin = 10
    origin_x = WIDTH - preview_width - margin
    origin_y = margin

    # Draw background box for clarity
    box_rect = pygame.Rect(origin_x - 6, origin_y - 6, preview_width + 12, preview_height + 12)
    pygame.draw.rect(surface, WHITE, box_rect)
    pygame.draw.rect(surface, BLACK, box_rect, 1)

    for i in range(h):
        for j in range(w):
            if shape[i, j]:
                rect = (
                    origin_x + j * preview_cell,
                    origin_y + i * preview_cell,
                    preview_cell,
                    preview_cell,
                )
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, BLACK, rect, 1)




def _make_tone(freq_hz=440, duration_ms=50, volume=0.2):
    """Create a short pygame.Sound tone using NumPy (no external files).
    Ensures dtype, shape and channels match the active mixer to avoid artifacts.
    """
    if not pygame.mixer.get_init():
        # Initialize mixer with safe common defaults if not already active
        pygame.mixer.init(frequency=44100, size=-16, channels=2)
    freq, _size, ch = pygame.mixer.get_init()
    sr = int(freq)
    n = max(1, int(sr * (duration_ms / 1000.0)))
    t = np.arange(n, dtype=np.float32) / float(sr)
    wave = np.sin(2 * np.pi * float(freq_hz) * t) * (32767.0 * float(volume))
    wave = wave.astype(np.int16)
    if ch == 2:
        wave = np.column_stack((wave, wave))
    elif ch != 1:
        # Fallback to mono if mixer reports unexpected channel count
        wave = np.ascontiguousarray(wave)
        return pygame.sndarray.make_sound(wave)
    wave = np.ascontiguousarray(wave)
    return pygame.sndarray.make_sound(wave)


def build_sfx():
    """Construct a small set of synthesized SFX."""
    s = {}
    s['rotate'] = _make_tone(700, 40, 0.15)
    s['lock'] = _make_tone(220, 60, 0.2)
    s['drop'] = _make_tone(880, 70, 0.2)
    s['clear'] = _make_tone(600, 80, 0.3)
    s['clear_1'] = _make_tone(600, 80, 0.3)
    s['clear_2'] = _make_tone(700, 80, 0.35)
    s['clear_3'] = _make_tone(800, 100, 0.35)
    s['clear_4'] = _make_tone(950, 120, 0.4)
    s['game_over'] = _make_tone(130, 500, 0.25)
    # Normalize SFX output a bit to reduce clipping when overlapping
    for snd in s.values():
        snd.set_volume(0.9)
    return s


def main():
    # Configure the mixer before initializing pygame to lock desired audio format
    try:
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=256)
    except Exception:
        # Safe fallback; mixer may still get initialized lazily in _make_tone
        pass
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
    clock = pygame.time.Clock()
    score_font = pygame.font.SysFont(None, 32) # pygame.font.SysFont(None, 32) means creating a Font object using the default system font with a size of 32 points. Here, passing None as the first argument tells pygame to use the built-in default font (which is "freesansbold"). The second argument, 32, specifies the font size.
    sfx = build_sfx()  # 각 사운드에 해당하는, Sound object 딕셔너리
    game = Tetris(sfx=sfx)
    gravity_timer = 0
    base_gravity_interval = 200  # milliseconds per drop (normal)

    running = True
    paused = False
    game_over = False
    p_toggle_locked = False  # prevent repeated toggles while P is held (OS key repeat)
    lock_timer = 0
    lock_delay = 500  # milliseconds allowed to move left/right before locking when blocked
    is_lock_pending = False
    while running:
        dt = clock.tick(FPS)
        gravity_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and not game_over:
                    # Toggle pause on P, but only on initial press (not repeats)
                    if not p_toggle_locked:
                        paused = not paused
                        p_toggle_locked = True
                # When paused, ignore other key actions
                if not paused and not game_over:
                    if event.key == pygame.K_UP:
                        game.rotate_ccw()
                    elif event.key == pygame.K_LEFT:
                        # allow left/right movement even during lock delay
                        game.move(-1)
                        # if there is space below after move, cancel pending lock
                        if not game.check_collision(game.piece['shape'], game.piece['r'] + 1, game.piece['c']):
                            is_lock_pending = False
                            lock_timer = 0
                    elif event.key == pygame.K_RIGHT:
                        game.move(1)
                        if not game.check_collision(game.piece['shape'], game.piece['r'] + 1, game.piece['c']):
                            is_lock_pending = False
                            lock_timer = 0
                    elif event.key == pygame.K_SPACE:
                        game.hard_drop()
            elif event.type == pygame.KEYUP:
                # Release the P toggle lock when P is released
                if event.key == pygame.K_p:
                    p_toggle_locked = False

    # If paused, skip gravity and normal input processing
    # Level-based speed: every 10 locked pieces increases speed by 10%
        if not game_over:
            level = game.locked_pieces // 10
            speed_multiplier = (1.0 - 0.1 * level) if level > 0 else 1.0
            # Don't let multiplier go below a small positive value
            speed_multiplier = max(speed_multiplier, 0.1)

            # If down arrow is held, make pieces fall faster (soft drop)
            keys = pygame.key.get_pressed()
            soft_drop = SOFT_DROP_FACTOR if keys[pygame.K_DOWN] else 1
            # current_interval reduces with speed_multiplier (faster -> smaller interval)
            current_interval = int(base_gravity_interval * speed_multiplier) // soft_drop

            if not paused and gravity_timer >= current_interval:
                moved = game.step_down()
                gravity_timer = 0
                if not moved:
                    # Piece is blocked below; start lock delay
                    if not is_lock_pending:
                        is_lock_pending = True
                        lock_timer = 0

            # If lock is pending, cancel if space opens; otherwise count delay
            if is_lock_pending and not paused:
                if not game.check_collision(game.piece['shape'], game.piece['r'] + 1, game.piece['c']):
                    # Space appeared below (e.g., lines cleared) — cancel lock
                    is_lock_pending = False
                    lock_timer = 0
                else:
                    lock_timer += dt
                    if lock_timer >= lock_delay:
                        game.lock_piece()
                        is_lock_pending = False
                        lock_timer = 0
        else:
            is_lock_pending = False

        #screen.fill(WHITE)
        screen.fill(BLACK)
        draw_grid(screen)
        ghost_cells = game.get_ghost_cells()
        b = game.get_board_with_piece()
        draw_board(screen, b, ghost_cells)
        draw_next_piece(screen, game.next_piece)

        # Draw paused overlay if needed (draw before single flip)
        if paused:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))  # translucent black
            screen.blit(overlay, (0, 0))
            font = pygame.font.SysFont(None, 72)
            text = font.render('PAUSED', True, WHITE)
            tx = (WIDTH - text.get_width()) // 2
            ty = (HEIGHT - text.get_height()) // 2
            screen.blit(text, (tx, ty))

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            font = pygame.font.SysFont(None, 72)
            text = font.render('GAME OVER', True, WHITE)
            tx = (WIDTH - text.get_width()) // 2
            ty = (HEIGHT - text.get_height()) // 2
            screen.blit(text, (tx, ty))

        # Draw score in white to contrast with black background
        score_text = score_font.render(f"Score: {game.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Final flip once per frame
        pygame.display.flip()

        if game.game_over and not game_over:
            print("Game Over. Score:", game.score)
            # play game over sfx once
            snd = game.sfx.get('game_over') if hasattr(game, 'sfx') else None
            if snd:
                snd.play()
            game_over = True
            paused = False
            p_toggle_locked = False
            is_lock_pending = False

    pygame.quit()


if __name__ == '__main__':
#    print("Executed by Ctrl+F5 inside VS Code :  __name__ == '__main__' is true.  ") # 이 부분은 실행이 된다.
    main()
