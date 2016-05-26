#!usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *

#--------------------------------------------
class DragableRect:
	def __init__(self, options):
		"""
		each DragableRect instance is initialised with a dict :
		d = DragableRect({"parent": canvas, "x": 10, "y": 10, ... })

		dict keys are classic options of 
		Canvas's create_rectangle method :
		x, y, width, height, outline, fill, tags

		"parent" is for the container canvas
		"axis" : "both" to drag in evry

		"""
		self.parent = options["parent"] # canvas
		self.x = options["x"]
		self.y = options["y"]
		self.width = options["width"]
		self.height = options["height"]
		self.outline = options["outline"]
		self.fill = options["fill"]
		self.tag = options["tag"]
		self.axis = options["axis"] # 'h', 'v' or 'both'

		self.selected = False

	def display(self):
		"""
		draw rect on parent Canvas
		"""
		self.parent.create_rectangle(
				self.x,
				self.y,
				self.x + self.width,
				self.y + self.height,
				fill = self.fill,
				outline = self.outline,
				tags = self.tag)

	def getPos(self):
		"""
		return self coords as (x0, y0, x1, y1)
		"""
		return self.parent.coords(self.tag)

class DragableCircle:
	pass

#-----------------------------------------------------------------
class DragAndDrop(Tk):
	"""
	Tkinter app based on Tk()

	"""
	def __init__(self):
		Tk.__init__(self)
		self.title("Tkinter drag and drop")
		self.geometry("400x300+400+400")
		self.can = Canvas(self, width=400, height=300, bg="#000233")
		self.can.pack()

		#these attributes are used in click, drag and drop methods
		self.click_flag = False
		self.offset_x = 0
		self.offset_y = 0

		self.items = [
			DragableRect({
				"parent": self.can,
				"x": 100,
				"y": 100,
				"width": 50,
				"height": 50,
				"outline": "red",
				"fill": "red",
				"tag": "red",
				"axis": "both"
				}),
			DragableRect({
				"parent": self.can,
				"x": 250,
				"y": 50,
				"width": 40,
				"height": 60,
				"outline": "#46b96a",
				"fill": "#46b96a",
				"tag": "green",
				"axis": "h"
				})]

		for i in self.items:
			i.display()

		self.bind("<Button-1>", self.click)
		self.bind("<ButtonRelease-1>", self.drop)
		self.bind("<B1-Motion>", self.drag)

	def click(self, evt):
		"""
		if a rect is clicked :
		- switch 'click_flag' to True
		- switch rect's 'selected' attribute to True
		- detect mouse offset from top-left corner of clicked rect
		"""
		x, y = evt.x, evt.y
		for i in self.items:
			coords = i.getPos()
			if x > coords[0] and x < coords[2]:
				if y > coords[1] and y < coords[3]:
					self.click_flag = True
					i.selected = True
					self.offset_x = x - i.x
					self.offset_y = y - i.y
					break

	def drop(self, evt):
		"""
		- switch 'click_flag' and dragged rect's 'selected' attribute to False
		- update rect's 'x' and 'y' attributes
		"""
		if self.click_flag:
			x, y = evt.x, evt.y
			self.click_flag = False
			for i in self.items:
				if i.selected:
					i.x = x - self.offset_x
					i.y = y - self.offset_y
					i.selected = False

	def drag(self, evt):
		if self.click_flag:
			x, y = evt.x, evt.y
			for i in self.items:
				if i.selected:
					self.can.coords(i.tag,
									x - self.offset_x,
									y - self.offset_y,
									(x - self.offset_x) + i.width,
									(y - self.offset_y) + i.height)

#-------------------------------------------------------------------
if __name__ == '__main__':

	app = DragAndDrop()
	app.mainloop()