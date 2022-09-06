from math import sqrt
from pygame.math import Vector2

def normalize(vector=Vector2()):
    x = vector.x
    y = vector.y
    if x ==0 and y ==0:
        return vector
    else:
        x_new = x/sqrt(x ** 2 +y ** 2)
        y_new = y/sqrt(x ** 2 + y ** 2)
        return Vector2((x_new,y_new))