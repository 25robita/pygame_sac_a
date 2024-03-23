from typing import Literal

import pygame

import asset

def player_selector(surface: pygame.Surface) -> Literal[0, 1, 2, 3]:

    area = (600, 500)

    size = (area[0] // 2, area[1] // 2)

    chars: list[pygame.Surface] = []

    paths = [
        (asset.AssetType.CHARACTER, asset.CharacterType.MASK_DUDE, asset.CharacterVariant.FALL),
        (asset.AssetType.CHARACTER, asset.CharacterType.NINJA_FROG, asset.CharacterVariant.JUMP),
        (asset.AssetType.CHARACTER, asset.CharacterType.PINK_MAN, asset.CharacterVariant.FALL),
        (asset.AssetType.CHARACTER, asset.CharacterType.VIRTUAL_GUY, asset.CharacterVariant.JUMP)
    ]

    for path in paths:
        chars.append(
            pygame.transform.scale(pygame.image.load(asset.get_asset_path(*path)), size)
        )

    font = pygame.font.Font(asset.get_asset_path(asset.AssetType.FONT, asset.FontType.VT323), 68)

    text = font.render("Select Your Character:", True, (255, 255, 255))

    active_i = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and active_i is not None:
                return active_i

        surface.fill((0, 0, 0))

        i = 0
        
        active_i = None

        for y in (90, 90 + area[1] // 2):
            for x in (0, area[0] // 2):
                chars[i].set_alpha(127)

                if chars[i].get_rect(x=x, y=y).collidepoint(pygame.mouse.get_pos()):
                    chars[i].set_alpha(255)
                    active_i = i

                surface.blit(chars[i], (x, y))

                i += 1

        surface.blit(text, ((area[0] - text.get_width()) // 2, 17))
        
        pygame.display.update()