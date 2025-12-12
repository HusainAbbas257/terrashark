'''

'''

import pygame
import random
from src.simulation.terrain import TerrainGenerator

pygame.init()

class Button:
    """A simple button class."""

    def __init__(self, rect, color, text='', text_color=(255,255,255)):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        if self.text:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN and
            self.rect.collidepoint(event.pos)
        )


def run_sample_terrain():
    """Show a generated terrain and return to menu when quitting."""
    seed = random.randint(0, 100000)
    generator = TerrainGenerator(seed, (50, 50), tile_size=10)
    terrain = generator.generate_terrain().get_list()

    screen = pygame.display.set_mode((500, 500))

    for y, row in enumerate(terrain):
        for x, tile in enumerate(row):
            pygame.draw.rect(
                screen,
                tile.get_colour(),
                (x * generator.tile_size, y * generator.tile_size,
                 generator.tile_size, generator.tile_size)
            )
    pygame.display.flip()

    # Wait for quit
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


def show_popup(text: str, width=400, height=200):
    """Shows a simple blocking popup window."""
    screen = pygame.display.get_surface()
    if screen is None:
        raise RuntimeError("No Pygame display surface found!")

    popup = pygame.Surface((width, height))
    popup.fill((40, 40, 40))

    popup_rect = popup.get_rect(center=screen.get_rect().center)

    font = pygame.font.Font(None, 32)
    lines = text.split("\n")

    # --- Render text and put it on popup ---
    y_offset = 40
    for line in lines:
        rendered = font.render(line, True, (255, 255, 255))
        r = rendered.get_rect(center=(width // 2, y_offset))
        popup.blit(rendered, r)
        y_offset += 40

    # border
    pygame.draw.rect(popup, (200, 200, 200), popup.get_rect(), 3)

    # --- Popup loop ---
    running = True
    while running:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                running = False

        screen.fill((0, 0, 0))
        screen.blit(popup, popup_rect)
        pygame.display.flip()


def run():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Terrashark Main Module")

    buttons = [
        Button((350, 275, 100, 50), (0, 255, 0), 'Start'),
        Button((300, 350, 200, 50), (255, 0, 0), 'Sample Terrain')
    ]

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            for button in buttons:
                if button.is_clicked(event):
                    if button.text == 'Start':
                        show_popup("You discovered an\nunimplemented feature!")
                    elif button.text == 'Sample Terrain':
                        run_sample_terrain()
                        screen = pygame.display.set_mode((800, 600))

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    '''advice: better run it from terrashark/__init__.py to avoid import errors'''
    run()
