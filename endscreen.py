from math import sin
from time import time

import pygame

import asset

def endscreen(surface: pygame.Surface, text: str):
    s = pygame.Surface(surface.get_size(), pygame.SRCALPHA, 32)
    
    s.fill((0, 0, 0, 127)) # darken overlay

    surface.blit(s, (0, 0)) # hm.
    s.blit(surface, (0, 0))

    font = pygame.font.Font(asset.get_asset_path(asset.AssetType.FONT, asset.FontType.VT323), 100)

    another_font = pygame.font.Font(asset.get_asset_path(asset.AssetType.FONT, asset.FontType.VT323), 40)

    game_over_text = font.render("Game Over", True, (255, 255, 255))

    other_text = another_font.render(text, True, (255, 255, 255))

    click_nadsfaiasdjf = pygame.transform.smoothscale_by(another_font.render("Click anywhere to return to the menu...", True, (255, 255, 255)), 0.65)

    # last frame of prev level
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        surface.blit(s, (0, 0))
        surface.blit(game_over_text, ((surface.get_width() - game_over_text.get_width()) // 2, 100))
        
        scale = sin(time())/20 + 1 # just a little fun effect
        trans = pygame.transform.smoothscale_by(other_text, scale)

        surface.blit(trans, (
            (surface.get_width() - trans.get_width()) // 2,
            (surface.get_height() - trans.get_height()) // 2
        ))

        surface.blit(click_nadsfaiasdjf, ((surface.get_width() - click_nadsfaiasdjf.get_width()) // 2, surface.get_height() - click_nadsfaiasdjf.get_height() - 20))


        pygame.display.update()