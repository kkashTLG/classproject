import pygame as pg
import math
from settings import *


class RayCasting:
    # Ray casting will use the field of view of player to determine distance between player and objects in view (
    # intersecdtion point).
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []    # clears results for raycasting before starting
        ox, oy = self.game.player.pos  # dependent on WASD input, the camera angle will change and either make
        # positive or negative change determines left or right FOV change.
        x_map, y_map = self.game.player.map_pos

        texture_vert, texture_hor = 1, 1 # initialize of texture value

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        # Loop below determined angles of each ray
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # horizontal and vertical make up for 2 points of intersection with wall. Dependening upon approach and
            # angle, one of the 2 will be shorter. The shorter one will be what is closest to the player.

            # horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # depth and texture offset
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # projection
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # Ray casting result
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            # draw walls (NO LONGER NECESSARY AFTER ADDING TEXTURES)
            # color = [255 / (1 + depth ** 5 * 0.00002)] * 3  # Adds darkness to further away walls
            # pg.draw.rect(self.game.screen, color,
            #              (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))

            # draw for debug (SHOWS YELLOW FOV FROM RAYCASTING)
            # pg.draw.line(self.game.screen, 'yellow', (100 * ox, 100 * oy),
            #              (100 * ox + 100 * depth * cos_a, 100 * oy + 100 * depth * sin_a), 2)

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()
