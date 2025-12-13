"""
main.py: menu and basic functionality to run the simulation.

This module provides:
- Button UI for a simple menu.
- run_sample_terrain() that uses your terrain module's generator + renderer.
- show_popup() simple blocking modal (keeps existing behavior).
- run() main menu loop.

Assumes `from src.simulation.terrain import *` exposes:
  TileImageCache, TerrainGenerator, TerrainRenderer
and that pygame is available/initialized by project bootstrap.
"""

import pygame
import random
from src.simulation.terrain import *  # keep your project import style

# NOTE: project __init__.py is expected to call pygame.init() if required.
# but we ensure pygame is initialized here if not already.
if not pygame.get_init():
    pygame.init()


class Button:
    """Simple rectangular button with centered text.

    Methods
    -------
    draw(surface)
        Draws the button on the given surface.
    is_clicked(event) -> bool
        Returns True for left-button MOUSEBUTTONDOWN inside rect.
    """

    def __init__(self, rect, color, text='', text_color=(255, 255, 255)):
        """Initialize the button.

        Parameters
        ----------
        rect : tuple[int, int, int, int]
            x, y, w, h rectangle for the button.
        color : tuple[int, int, int]
            RGB fill color.
        text : str
            Optional label text.
        text_color : tuple[int, int, int]
            Color for the label.
        """
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        """Draw the button on the given surface."""
        pygame.draw.rect(surface, self.color, self.rect)
        if self.text:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        """Return True when the left mouse button was pressed inside the button."""
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


def run_sample_terrain(screen: pygame.Surface, map_size=(50, 50), tile_size=10) -> bool:
    """Generate and display a sample terrain until the user returns.

    Parameters
    ----------
    screen : pygame.Surface
        The main display surface (menu surface will remain intact).
    map_size : tuple[int,int]
        Size of the generated tilemap in tiles (width, height).
    tile_size : int
        Pixel size of each tile for the renderer.

    Returns
    -------
    bool
        True to continue main menu loop, False to exit application (user quit).
    """
    # Ensure display surface exists and images are loaded AFTER display init.
    if pygame.display.get_surface() is None:
        raise RuntimeError("Display surface not initialized before calling run_sample_terrain()")

    # Load tile images (must be done after display init)
    TileImageCache.load_images(tile_size, "assets/tiles")

    seed = random.randint(0, 100_000)
    generator = TerrainGenerator(seed, map_size)
    tilemap = generator.generate_tilemap()

    renderer = TerrainRenderer(tile_size)
    # Build background scaled to the current screen size
    screen_size = screen.get_size()
    bg = renderer.build_background(tilemap, screen_size, f"cache/sample_terrain_{seed}.png")

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # user closed window -> signal main to exit
                return False
            if event.type == pygame.KEYDOWN:
                # ESC to return to menu
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Right click to return quickly
                if event.button == 3:
                    running = False

        screen.blit(bg, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    # returned to menu
    return True


def show_popup(text: str, width=400, height=200):
    """Show a blocking popup centered on the current display surface.

    Closes on any keypress, mouse click, or window close.
    """
    screen = pygame.display.get_surface()
    if screen is None:
        raise RuntimeError("No Pygame display surface found!")

    popup = pygame.Surface((width, height))
    popup.fill((40, 40, 40))
    popup_rect = popup.get_rect(center=screen.get_rect().center)

    font = pygame.font.Font(None, 32)
    lines = text.split("\n")
    y_offset = 40
    for line in lines:
        rendered = font.render(line, True, (255, 255, 255))
        r = rendered.get_rect(center=(width // 2, y_offset))
        popup.blit(rendered, r)
        y_offset += 40

    pygame.draw.rect(popup, (200, 200, 200), popup.get_rect(), 3)

    # modal loop
    blocking = True
    clock = pygame.time.Clock()
    while blocking:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                blocking = False

        screen.fill((0, 0, 0))
        screen.blit(popup, popup_rect)
        pygame.display.flip()
        clock.tick(60)


def run():
    """Run the main menu loop.

    Menu flow:
      - Start: placeholder popup (keeps original behavior)
      - Sample Terrain: launches run_sample_terrain() and returns to menu
                       unless the user closed the window (then exit).
    """
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Terrashark Main Module")

    buttons = [
        Button((350, 275, 100, 50), (0, 200, 0), 'Start'),
        Button((300, 350, 200, 50), (200, 0, 0), 'Sample Terrain'),
    ]

    clock = pygame.time.Clock()
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
                        # run sample; if it returns False, the user closed window -> exit app
                        cont = run_sample_terrain(screen, map_size=(50, 50), tile_size=10)
                        if not cont:
                            running = False
                        # if cont is True, we continue the menu loop without recreating display

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    # advice: better run from project entrypoint so project __init__ can bootstrap
    run()
"""
main.py: menu and basic functionality to run the simulation.

This module provides:
- Button UI for a simple menu.
- run_sample_terrain() that uses your terrain module's generator + renderer.
- show_popup() simple blocking modal (keeps existing behavior).
- run() main menu loop.

Assumes `from src.simulation.terrain import *` exposes:
  TileImageCache, TerrainGenerator, TerrainRenderer
and that pygame is available/initialized by project bootstrap.
"""

import pygame
import random
from src.simulation.terrain import *  # keep your project import style

# NOTE: project __init__.py is expected to call pygame.init() if required.
# but we ensure pygame is initialized here if not already.
if not pygame.get_init():
    pygame.init()


class Button:
    """Simple rectangular button with centered text.

    Methods
    -------
    draw(surface)
        Draws the button on the given surface.
    is_clicked(event) -> bool
        Returns True for left-button MOUSEBUTTONDOWN inside rect.
    """

    def __init__(self, rect, color, text='', text_color=(255, 255, 255)):
        """Initialize the button.

        Parameters
        ----------
        rect : tuple[int, int, int, int]
            x, y, w, h rectangle for the button.
        color : tuple[int, int, int]
            RGB fill color.
        text : str
            Optional label text.
        text_color : tuple[int, int, int]
            Color for the label.
        """
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        """Draw the button on the given surface."""
        pygame.draw.rect(surface, self.color, self.rect)
        if self.text:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        """Return True when the left mouse button was pressed inside the button."""
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


def run_sample_terrain(screen: pygame.Surface, map_size=(50, 50), tile_size=10) -> bool:
    """Generate and display a sample terrain until the user returns.

    Parameters
    ----------
    screen : pygame.Surface
        The main display surface (menu surface will remain intact).
    map_size : tuple[int,int]
        Size of the generated tilemap in tiles (width, height).
    tile_size : int
        Pixel size of each tile for the renderer.

    Returns
    -------
    bool
        True to continue main menu loop, False to exit application (user quit).
    """
    # Ensure display surface exists and images are loaded AFTER display init.
    if pygame.display.get_surface() is None:
        raise RuntimeError("Display surface not initialized before calling run_sample_terrain()")

    # Load tile images (must be done after display init)
    TileImageCache.load_images(tile_size, "assets/tiles")

    seed = random.randint(0, 100_000)
    generator = TerrainGenerator(seed, map_size)
    tilemap = generator.generate_tilemap()

    renderer = TerrainRenderer(tile_size)
    # Build background scaled to the current screen size
    screen_size = screen.get_size()
    bg = renderer.build_background(tilemap, screen_size, f"cache/sample_terrain_{seed}.png")

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # user closed window -> signal main to exit
                return False
            if event.type == pygame.KEYDOWN:
                # ESC to return to menu
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Right click to return quickly
                if event.button == 3:
                    running = False

        screen.blit(bg, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    # returned to menu
    return True


def show_popup(text: str, width=400, height=200):
    """Show a blocking popup centered on the current display surface.

    Closes on any keypress, mouse click, or window close.
    """
    screen = pygame.display.get_surface()
    if screen is None:
        raise RuntimeError("No Pygame display surface found!")

    popup = pygame.Surface((width, height))
    popup.fill((40, 40, 40))
    popup_rect = popup.get_rect(center=screen.get_rect().center)

    font = pygame.font.Font(None, 32)
    lines = text.split("\n")
    y_offset = 40
    for line in lines:
        rendered = font.render(line, True, (255, 255, 255))
        r = rendered.get_rect(center=(width // 2, y_offset))
        popup.blit(rendered, r)
        y_offset += 40

    pygame.draw.rect(popup, (200, 200, 200), popup.get_rect(), 3)

    # modal loop
    blocking = True
    clock = pygame.time.Clock()
    while blocking:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                blocking = False

        screen.fill((0, 0, 0))
        screen.blit(popup, popup_rect)
        pygame.display.flip()
        clock.tick(60)


def run():
    """Run the main menu loop.

    Menu flow:
      - Start: placeholder popup (keeps original behavior)
      - Sample Terrain: launches run_sample_terrain() and returns to menu
                       unless the user closed the window (then exit).
    """
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Terrashark Main Module")

    buttons = [
        Button((350, 275, 100, 50), (0, 200, 0), 'Start'),
        Button((300, 350, 200, 50), (200, 0, 0), 'Sample Terrain'),
    ]

    clock = pygame.time.Clock()
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
                        # run sample; if it returns False, the user closed window -> exit app
                        cont = run_sample_terrain(screen, map_size=(50, 50), tile_size=10)
                        if not cont:
                            running = False
                        # if cont is True, we continue the menu loop without recreating display

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    # advice: better run from project entrypoint so project __init__ can bootstrap
    run()
