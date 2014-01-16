import sys,os
import pygame as pg
import lib.db


pg.init()

size = width, height = 320, 240
speed = [2, 2]
black=0,0,0

screen = pg.display.set_mode(size)

running=True
while running:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running=False

	screen.fill(black)
	pg.display.flip()

pg.quit()
sys.exit()


#http://www.slideshare.net/dabeaz/an-introduction-to-python-concurrency 39/168
