import pygame
import time
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import messagebox

# necessary
pygame.init()

# define constants for the pixel field
pixel_field_width = 500
pixel_field_height = 500

# color picker goes to right of the pixel field
color_picker_field_width = 100
color_picker_field_height = pixel_field_height

# screen width is the pixel field + the color picker
screen_width = pixel_field_width + color_picker_field_width
screen_height = pixel_field_height

# background color and starting color for painting
screen_color = (100, 100, 100)
current_color = (0, 255, 0)

# define the number of pixels
pixels_x = 5
pixels_y = 5

# define the dimensions of the pixels
pixel_width = pixel_field_width / pixels_x
pixel_height = pixel_field_height / pixels_y

# the window is the pixel field plus the color picker
class window():
	def __init__(self):
		self.screen = pygame.display.set_mode((screen_width, screen_height))
		self.clock = time.time()
		self.pixels = []
		self.fill_pixels()
		self.draw_mode = True
		self.color_picker = color_picker(pixel_field_width, 0)
		
		# infinite game loop
		self.run()

	# def fill_fields(self):


	def fill_pixels(self):
		for i in range(pixels_x):
			for j in range(pixels_y):
				self.pixels.append(cell(i*pixel_width, j*pixel_height, pixel_width, pixel_height))

	def update(self):
		# paint the background before every frame
		self.screen.fill(screen_color)

		# draw the pixels on the left of the screen
		for p in self.pixels:
			if self.draw_mode:
				p.update(current_color)
			else:
				p.update(screen_color)

			self.screen.blit(p.get_surface(), p.get_pos())

		# draw the color picker on the right of the screen
		self.color_picker.update()
		self.screen.blit(self.color_picker.get_surface(), self.color_picker.get_pos())

		# draw the fields onto the color picker
		for f in self.color_picker.get_fields():
			self.screen.blit(f.get_surface(), f.get_pos())

		# final step, update the actual screen
		pygame.display.update()

	def export_pixels(self):
		file = open("pixels.csv","w") 
		for p in self.pixels:
			file.write("" + str(p.x) + "," + 
				str(p.y) + "," + 
				str(p.get_width()) + "," + 
				str(p.get_height()) + "," +
				str(p.get_color()) + "\n")

		file.close()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				if event.type == pygame.KEYDOWN:
					if event.key == ord('e'):
						self.draw_mode = not self.draw_mode
					if event.key == ord('p'):
						self.export_pixels()

			current_time = time.time()
			if current_time - self.clock > 1.0/60.0:
				self.clock = time.time()
				self.update()

class cell():
	def __init__(self, x, y, w, h):
		self.color = screen_color
		self.activated_color = (0, 255, 0)
		self.activated = False
		self.listening = False
		self.width = w
		self.height = h
		self.x = x
		self.y = y
		self.surface = pygame.Surface((self.width, self.height))
		self.surface.fill(self.color)
		self.rect = pygame.Rect(x, y, w, h)

	def get_width(self):
		return self.width

	def get_height(self):
		return self.height

	def get_surface(self):
		return self.surface

	def get_pos(self):
		return (self.x, self.y)

	def contains(self, pos):
		return self.rect.collidepoint(pos)

	def update(self, color):
		self.check_mouse(color)
		self.set_color()

	def check_mouse(self, color):
		if pygame.mouse.get_pressed()[0]:
			if self.rect.collidepoint(pygame.mouse.get_pos()):
				self.color = color
				
	def set_color(self):
		self.surface.fill(self.color)

	def get_color(self):
		return self.color

class color_picker():
	def __init__(self, x, y):
		self.width = 100
		self.height = screen_height
		self.x = x
		self.y = y
		self.color = (0, 0, 0)
		self.surface = pygame.Surface((self.width, self.height))
		self.surface.fill(self.color)
		self.padding = 10
		self.fields_x_offset = pixel_field_width + self.padding
		self.fields_y_offset = self.padding
		self.field_width = 20
		self.field_height = 255
		self.fields = []
		self.add_fields()

	def update(self):
		global current_color
		self.fields[0].update()
		self.fields[1].update()
		self.fields[2].update()

		r = self.fields[0].get_value()
		g = self.fields[1].get_value()
		b = self.fields[2].get_value()
		self.color = (r, g, b)
		current_color = self.color
		self.surface.fill(self.color)


	def set_color(self, color):
		self.color = color

	def get_color(self):
		return self.color

	def get_fields(self):
		return self.fields

	def add_fields(self):
		self.fields.append(field(self.field_width, self.field_height, self.fields_x_offset, self.fields_y_offset, (255, 0, 0), 255))
		self.fields.append(field(self.field_width, self.field_height, self.fields_x_offset + 30, self.fields_y_offset, (0, 255, 0), 255))
		self.fields.append(field(self.field_width, self.field_height, self.fields_x_offset + 60, self.fields_y_offset, (0, 0, 255), 255))

	def get_surface(self):
		return self.surface

	def get_pos(self):
		return (self.x, self.y)

class field():
	def __init__(self, w, h, x, y, color, value):
		self.width = w
		self.height = h
		self.x = x
		self.y = y
		self.color = color
		self.surface = pygame.Surface((self.width, self.height))
		self.surface.fill(self.color)
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.value = value

	def update(self):
		self.check_mouse()
		# self.set_color()

	def check_mouse(self):
		if pygame.mouse.get_pressed()[0]:
			if self.rect.collidepoint(pygame.mouse.get_pos()):
				self.value = (pygame.mouse.get_pos()[1] - self.y) 

	def set_color(self):
		self.surface.fill(self.color)

	def get_value(self):
		return self.value

	def get_surface(self):
		return self.surface

	def get_pos(self):
		return (self.x, self.y)

w = window()