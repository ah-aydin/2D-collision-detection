import pygame as pg
import math

pg.init()
pg.font.init()

WHITE = (255, 255, 255)

font = pg.font.SysFont("Consolas", 16)
t1 = font.render("0", False, WHITE)
t2 = font.render("1", False, WHITE)
t3 = font.render("2", False, WHITE)
t4 = font.render("3", False, WHITE)

t = [t1, t2, t3, t4]

surface = pg.display.set_mode((800, 600))

class Rectangle():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pg.Rect(
            x - width // 2,
            y - height // 2,
            width,
            height
        )
        self.color = color
        self.update_verticies()
    
    def render(self):
        pg.draw.rect(
            surface,
            self.color,
            self.rect,
        )
    
    def move(self, x, y):
        self.x += x
        self.y += y
        self.rect = pg.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )

        self.update_verticies()
    
    def update_verticies(self):
        self.verticies = [
            (self.rect.x, self.rect.y),
            (self.rect.x + self.rect.width, self.rect.y),
            (self.rect.x + self.rect.width, self.rect.y + self.rect.height),
            (self.rect.x, self.rect.y + self.rect.height)
        ]
    
    def get_pos(self):
        return (self.x, self.y)

r = Rectangle(400, 300, 200, 100, (255, 0, 0))
r2 = Rectangle(500, 300, 100, 50, (0, 255, 0))

def get_vector(p1, p2):
    return [- p1[1] + p2[1], p1[0] - p2[0]]

def get_magnitude(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2)

def get_axes(verts):
    v0 = get_vector(verts[0], verts[1])
    v1 = get_vector(verts[1], verts[2])
    v2 = get_vector(verts[2], verts[3])
    v3 = get_vector(verts[3], verts[0])
    return [
        (v0[0] / get_magnitude(v0), v0[1] / get_magnitude(v0)),
        (v1[0] / get_magnitude(v1), v1[1] / get_magnitude(v1)),
        (v2[0] / get_magnitude(v2), v2[1] / get_magnitude(v2)),
        (v3[0] / get_magnitude(v3), v3[1] / get_magnitude(v3))
    ]

def get_dot_product(p1, p2):
    return p1[0] * p2[0] + p1[1] * p2[1]

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                r2.move(0, -10)
            if event.key == pg.K_DOWN:
                r2.move(0, 10)
            if event.key == pg.K_RIGHT:
                r2.move(10, 0)
            if event.key == pg.K_LEFT:
                r2.move(-10, 0)

    axes = get_axes(r.verticies)
    
    colliding = True

    counter = 0
    for axis in axes:
        mn1 = get_dot_product(axis, r.verticies[0])
        mx1 = get_dot_product(axis, r.verticies[1])
        for vertex in r.verticies[1:]:
            dot = get_dot_product(axis, vertex)
            mn1 = min(mn1, dot)
            mx1 = max(mx1, dot)
        
        mn2 = get_dot_product(axis, r2.verticies[0])
        mx2 = get_dot_product(axis, r2.verticies[0])
        for vertex in r2.verticies[1:]:
            dot = get_dot_product(axis, vertex)
            mn2 = min(mn2, dot)
            mx2 = max(mx2, dot)

        yep = False
        if mn1 - mx2 > 0 or mn2 - mx1 > 0:
            colliding = False
            yep = False
        else:
            yep = True
        text = f"V_R1_{counter}_m: {mn1} V_R1_{counter}_M: {mx1} | V_R2_{counter}_m: {mn2} V_R2_{counter}_M: {mx2}"
        if yep:
            text += " | NO GAP"
        else:
            text += " | GAP"
        t[counter] = font.render(
            text,
            False,
            WHITE
        )
        counter += 1

    if colliding:
        r2.color = (0, 255, 0)
    else:
        r2.color = (0, 0, 255)

    # Rendering part
    surface.fill((0, 0, 0))
    r.render()
    r2.render()
    surface.blit(t[0], (0, 0))
    surface.blit(t[1], (0, 50))
    surface.blit(t[2], (0, 100))
    surface.blit(t[3], (0, 150))
    pg.display.update()

pg.quit()
