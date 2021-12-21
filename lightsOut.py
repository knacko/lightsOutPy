import pygame

### Globals ###

pygame.init()

adj = [[0, 0], [0, -1], [-1, 0], [0, 1], [1, 0]]

BOARD_SIZE = 5
TILE_HEIGHT = 50
TILE_WIDTH = 50
MARGIN = 2


### LightsOut Class ###

class LightsOut:

    def __init__(self, fname=None):
        self.clear()
        if fname != None:
            self.load_level(fname)

    def clear(self):
        self.grid = [[0 for i in xrange(BOARD_SIZE)] for j in xrange(BOARD_SIZE)]

    def load_level(self, fname):
        lstr = []
        f = open(fname)
        for line in f:
            lstr += [line.split()[0]]
        f.close()
        for y in xrange(len(lstr)):
            for x in xrange(len(lstr[y])):
                self.grid[x][y] = int(lstr[y][x])

    def draw(self):
        for y in xrange(BOARD_SIZE):
            for x in xrange(BOARD_SIZE):
                i = x * TILE_WIDTH + MARGIN
                j = y * TILE_HEIGHT + MARGIN
                h = TILE_HEIGHT - (2 * MARGIN)
                w = TILE_WIDTH - (2 * MARGIN)
                if self.grid[y][x] == 1:
                    pygame.draw.rect(screen, (105, 210, 231), [i, j, w, h])
                else:
                    pygame.draw.rect(screen, (255, 255, 255), [i, j, w, h])

    def get_adjacent(self, x, y):
        adjs = []
        for i, j in adj:
            if (0 <= i + x < BOARD_SIZE) and (0 <= j + y < BOARD_SIZE):
                adjs += [[i + x, j + y]]
        return adjs

    def click(self, pos):
        x = pos[0] / TILE_WIDTH
        y = pos[1] / TILE_HEIGHT
        adjs = self.get_adjacent(x, y)
        for i, j in adjs:
            self.grid[j][i] = (self.grid[j][i] + 1) % 2


### Main ###

if __name__ == "__main__":

    screen = pygame.display.set_mode((BOARD_SIZE * TILE_WIDTH, BOARD_SIZE * TILE_HEIGHT))
    screen.fill((167, 219, 216))
    pygame.display.set_caption("Lights Out")

    game = LightsOut("level.txt")

    clock = pygame.time.Clock()

    keepGoing = True
    while keepGoing:

        clock.tick(30)

        game.draw()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                keepGoing = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.click(pos)

        pygame.display.flip()
    pygame.quit()
