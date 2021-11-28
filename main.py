import pygame
import sys
import text
import ui
import random


width, height = 1280, 720
window = pygame.display.set_mode((width, height))
window_clock = pygame.time.Clock()  # creates clock to control framerate


class Particles:
    def __init__(self):
        self.particles = []
        self.background_particles = []
        self.engine_color_palette = [(79,11,118), (139,45,116), (199,73,86), (234,116,52), (246,165,11)]

    def particle_render(self, location):
        self.particles.append([location, [-2, round(random.uniform(-1, 1), 1)], random.randint(6, 10)])

        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.2
            pygame.draw.circle(window, (234,116,52) if particle[2] >= 5 else random.choice(self.engine_color_palette), particle[0], particle[2])
            if particle[2] <= 0:
                self.particles.remove(particle)

    def background_render(self):
        self.seconds = pygame.time.get_ticks() // 1000
        if self.seconds <= 14:
            self.background_particles.append([[width, random.randint(0, height)], -10, random.randint(2, 4)])
        else:
            self.background_particles.append([[width, random.randint(0, height)], -50, random.randint(2, 4)])
        for particle in self.background_particles:
            particle[0][0] += particle[1]
            pygame.draw.circle(window, (255, 255, 255), particle[0], particle[2])
            if particle[0][0] <= -10:
                self.background_particles.remove(particle)


# -------------------------------------------------- Start of Ship Stuff
class Gun:
    def __init__(self):
        self.g_broken = False
        self.g_hacked = False


    def gun_hacking(self):
        self.g_hacked = True
        # TODO: add sprite change

    def gun_broken(self):
        self.g_broken = True
        # TODO: add sprite change

    def gun_purged(self):
        self.g_hacked = False

    def gun_fixed(self):
        self.g_broken = False

    def gun_status(self):  # Gun should only be either broken or hacked, never both
        if self.g_broken:
            self.g_status = "Broken"
        elif self.g_hacked:
            self.g_status = "Hacked"
        else:
            self.g_status = "Functional"

        return self.g_status

    def fire(self):
        print("fire")
        pass  # TODO: add firing on click

    def gun_render(self, rect):
        self.gun_pos = rect[0], rect[1], rect[2] - 180, rect[3] - 110
        self.gun_rect = pygame.g

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                self.pos = pygame.mouse.get_pos()
                if self.gun_rect.rect.collidepoint(self.pos):
                    Gun.fire(self)


class Shields:
    def __init__(self):
        self.strength = 3
        self.s_hacked = False
        self.shield1 = pygame.image.load('data/shield1.png')
        self.shield2 = pygame.image.load('data/shield2.png')
        self.shield3 = pygame.image.load('data/shield3.png')
        self.shield1_rect = self.shield1.get_rect()
        self.shield2_rect = self.shield2.get_rect()
        self.shield3_rect = self.shield3.get_rect()

    def shield_hacking(self):  # Should only happen if the shield is on
        self.s_hacked = True
        self.strength -= 1

    def shield_status(self):
        if self.s_hacked:
            self.s_status = f"Hacked: {self.strength - 3}"
        else:
            self.s_status = f"Strength: {self.strength}"
        return self.s_status

    def shield_display(self, sprite):
        if self.strength >= 1:
            self.shield1_rect.center = sprite.center
            window.blit(self.shield1, self.shield1_rect)
        if self.strength >= 2:
            self.shield2_rect.center = sprite.center
            window.blit(self.shield2, self.shield2_rect)
        if self.strength >= 3:
            self.shield3_rect.center = sprite.center
            window.blit(self.shield3, self.shield3_rect)


class Ship(Particles, Gun, Shields):
    def __init__(self):
        self.sprite = pygame.image.load("data/spaceshipmedium.png")
        self.image_width = self.sprite.get_width()
        self.image_height = self.sprite.get_height()
        self.sprite_rect = self.sprite.get_rect()
        self.health = 10  # May be a variable if I add difficulty setting
        self.sprite_rect.centerx, self.sprite_rect.centery = width // 2, height // 2  # Initial position
        self.initial_x, self.initial_y = width // 2, height // 2  # Sloppy code rn but its like 1 am and too lazy
        self.speed = [1, 1]
        Shields.__init__(self)
        Gun.__init__(self)
        Particles.__init__(self)

    def draw(self):
        Ship.idle(self)
        Ship.particle_render(self, [self.sprite_rect.centerx - 170, self.sprite_rect.centery + 10])
        window.blit(self.sprite, self.sprite_rect)
        Ship.shield_display(self, self.sprite_rect)

    def idle(self):

        self.sprite_rect = self.sprite_rect.move(self.speed)
        if self.sprite_rect.centerx <= self.initial_x - 30 or self.sprite_rect.centerx >= self.initial_x + 30:
            self.speed[0] = -self.speed[0]
        if self.sprite_rect.centery <= self.initial_y - 50 or self.sprite_rect.centery >= self.initial_y + 50:
            self.speed[1] = -self.speed[1]

    def mouse_hovering(self):
        self.mouse = pygame.mouse.get_pos()
        self.collide = self.sprite_rect.collidepoint(self.mouse)
        self.ship_menu = ui.ShipMenu()
        Ship.gun_render(self, self.sprite_rect)
        if self.collide:
            self.gun_stat = Ship.gun_status(self)
            self.shield_stat = Ship.shield_status(self)
            self.ship_menu.menu(f"Guns: {self.gun_stat}", f"Shields: {self.shield_stat}", window, self.mouse)

# ------------------------------------------------------------ End of Ship Stuff


class Main:
    def __init__(self):
        self.black = 0, 0, 0
        pygame.init()
        self.main()



    def main(self):
        mainship = Ship()
        progress = ui.ProgressBar()
        particle1 = Particles()
        pygame.mixer.music.load('data/RED_CHAMBER.mp3')
        pygame.mixer.music.play()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            window.fill(self.black)
            particle1.background_render()
            mainship.draw()
            mainship.mouse_hovering()
            progress.render(window, (440, 620))
            pygame.display.flip()
            window_clock.tick(60)  # capped at 60 fps


if __name__ == "__main__":
    Main()
