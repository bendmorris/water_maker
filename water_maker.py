import pygame
import sys
import random

input_file = sys.argv[1]
output_file = sys.argv[2]

ST = 16
SX = 4
SY = 4
MOVES = 4


def partition(n,k,l=1):
    '''n is the integer to partition, k is the length of partitions'''
    if k < 1:
        raise StopIteration
    elif k == 1:
        if n >= 1:
            yield [n]
        raise StopIteration
    for i in range(l,n+1):
        for result in partition(n-i,k-1, i):
            yield [i]+result


image = pygame.image.load(input_file)
surf = pygame.Surface((SX*ST, SY*ST))
tiles = SX*SY
partitions = [x for x in partition(ST, tiles)]

movement = [[0 for _ in range(tiles)] for _ in range(ST)]

for i in range(ST):
    r = None
    while r is None or min([abs(ri - rj) for ri in r for rj in r if ri != rj]) < ST/MOVES/2:
        r = random.sample(range(tiles), MOVES)
    for n, ri in enumerate(r):
        movement[i][ri] = -1 if n < MOVES/2 else 1

cs = [[image.get_at((xi, yi)) for xi in range(ST)] for yi in range(ST)]

def m(yi, n):
    return sum(movement[yi][:n])

for n in range(tiles):
    px = (n % SX) * ST
    py = (n / SX) * ST
    csi = [cs[yi][m(yi, n):] + cs[yi][:m(yi, n)] for yi in range(ST)]
    for yi in range(ST):
        for xi in range(ST):
            surf.set_at((px+xi, py+yi), csi[yi][xi])

pygame.image.save(surf, output_file)
