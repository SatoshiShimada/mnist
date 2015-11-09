#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
	import Image
except:
	from PIL import Image
import math

class image:
	"""Image processing class"""

	def __init__(self, filename):
		self.img = Image.open(filename)
		self.filename = filename
		self.width, self.height = self.img.size
	
	def save(self, outfile, fmt='png'):
		self.img.save(outfile, fmt)

	def show(self):
		self.img.show()

	def copy(self):
		return self.img.copy()

	def resize(self, size):
		src_img = self.img.copy()
		self.img = Image.new("RGB", size)
		xscale = float(size[0]) / src_img.width
		yscale = float(size[1]) / src_img.height
		for y in xrange(size[1]):
			for x in xrange(size[0]):
				xp = int(x / xscale)
				yp = int(y / yscale)
				pixel = src_img.getpixel((xp, yp))
				self.img.putpixel((x, y), pixel)
		self.width = size[0]
		self.height = size[1]

	def rgb2gray(self):
		"""color type change RGB->GRAY"""
		RedWeight   = 0.2989
		GreenWeight = 0.5870
		BlueWeight  = 0.1140

		for y in range(self.height):
			for x in range(self.width):
				c = self.img.getpixel((x, y))
				p = int(RedWeight * c[0] + GreenWeight * c[1] + BlueWeight * c[2])
				self.img.putpixel((x, y), (p, p, p))
            
	def threshold(self, thresh, HIGH=0xff, LOW=0x00):
		"""high or low as threshold"""
		for y in range(self.height):
			for x in range(self.width):
				c = self.img.getpixel((x, y))
				if c[0] > thresh:
					p = HIGH
				else:
					p = LOW
				self.img.putpixel((x, y), (p, p, p))
	
	def median(self):
		"""median filter"""
		src_img = self.img.copy()

		for y in range(1, self.height - 1):
			for x in range(1, self.width - 1):
				c = []
				c.append(src_img.getpixel((x - 1, y - 1))[0])
				c.append(src_img.getpixel((x - 1, y    ))[0])
				c.append(src_img.getpixel((x - 1, y + 1))[0])
				c.append(src_img.getpixel((x    , y - 1))[0])
				c.append(src_img.getpixel((x    , y    ))[0])
				c.append(src_img.getpixel((x    , y + 1))[0])
				c.append(src_img.getpixel((x + 1, y - 1))[0])
				c.append(src_img.getpixel((x + 1, y    ))[0])
				c.append(src_img.getpixel((x + 1, y + 1))[0])

				m = median_value(c)
				self.img.putpixel((x, y), (m, m, m))

		#def median_value(c):
		def median_value(self, c):
			for i in range(len(c) - 1):
				for j in range(len(c) - 1):
					if c[i + 1] > c[i]:
						tmp = c[i + 1]
						c[i + 1] = c[i]
						c[i] = tmp

			return c[int(len(c) / 2)]

	def image_and(self, img2, HIGH=0xff, LOW=0x00):
		"""and operation"""
		if self.img.size[0] != img2.size[0] or self.img.size[0] != self.img.size[0]:
			print 'image size unmatch'
			sys.exit(0)
		if self.img.size[1] != img2.size[1] or self.img.size[1] != self.img.size[1]:
			print 'image size unmatch'
			sys.exit(0)

		for y in range(height):
			for x in range(width):
				p1 = self.img.getpixel((x, y))[0]
				p2 = img2.getpixel((x, y))[0]
				if p1 == HIGH and p2 == HIGH:
					self.img.putpixel((x, y), (HIGH, HIGH, HIGH))
				else:
					self.img.putpixel((x, y), (LOW, LOW, LOW))

	def dilation(self):
		"""dilation"""
		src_img = self.img.copy()
		HIGH = 0xff

		for y in range(1, self.height - 1):
			for x in range(1, self.width - 1):
				if src_img.getpixel((x - 1, y - 1))[0] == HIGH \
				or src_img.getpixel((x - 1, y    ))[0] == HIGH \
				or src_img.getpixel((x - 1, y + 1))[0] == HIGH \
				or src_img.getpixel((x    , y - 1))[0] == HIGH \
				or src_img.getpixel((x    , y    ))[0] == HIGH \
				or src_img.getpixel((x    , y + 1))[0] == HIGH \
				or src_img.getpixel((x + 1, y - 1))[0] == HIGH \
				or src_img.getpixel((x + 1, y    ))[0] == HIGH \
				or src_img.getpixel((x + 1, y + 1))[0] == HIGH:
					self.img.putpixel((x, y), (HIGH, HIGH, HIGH))

	def erosion(self):
		"""erosion"""
		src_img = self.img.copy()
		LOW  = 0x00

		for y in range(1, self.height - 1):
			for x in range(1, self.width - 1):
				if src_img.getpixel((x - 1, y - 1))[0] == LOW \
				or src_img.getpixel((x - 1, y    ))[0] == LOW \
				or src_img.getpixel((x - 1, y + 1))[0] == LOW \
				or src_img.getpixel((x    , y - 1))[0] == LOW \
				or src_img.getpixel((x    , y    ))[0] == LOW \
				or src_img.getpixel((x    , y + 1))[0] == LOW \
				or src_img.getpixel((x + 1, y - 1))[0] == LOW \
				or src_img.getpixel((x + 1, y    ))[0] == LOW \
				or src_img.getpixel((x + 1, y + 1))[0] == LOW:
					self.img.putpixel((x, y), (LOW, LOW, LOW))

	def openning(self):
		"""openning"""
		erosion(self.img)
		dilation(self.img)
	
	def closing(self):
		"""closing"""
		dilation(self.img)
		erosion(self.img)

	def sobel(self, amp = 4):
		""" sobel operation """
		cx_sobel = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
		cy_sobel = [-1, -2, -1, 0, 0, 0, 1, 2, 1]

		gradient(self.img, amp, cx_sobel, cy_sobel)

	def gradient(self, amp, cx, cy):
		src_img = self.img.copy()
		LOW  = (0x00, 0x00, 0x00)

		for y in range(self.height):
			for x in range(self.width):
				self.img.putpixel((x, y), LOW)

		for y in range(1, self.height - 1):
			for x in range(1, self.width - 1):
				d = []
				d.append(src_img.getpixel((x - 1, y - 1))[0])
				d.append(src_img.getpixel((x    , y - 1))[0])
				d.append(src_img.getpixel((x + 1, y - 1))[0])
				d.append(src_img.getpixel((x - 1, y    ))[0])
				d.append(src_img.getpixel((x    , y    ))[0])
				d.append(src_img.getpixel((x + 1, y    ))[0])
				d.append(src_img.getpixel((x - 1, y + 1))[0])
				d.append(src_img.getpixel((x    , y + 1))[0])
				d.append(src_img.getpixel((x + 1, y + 1))[0])
				xx = (
					cx[0] * d[0] +
					cx[1] * d[1] +
					cx[2] * d[2] +
					cx[3] * d[3] +
					cx[4] * d[4] +
					cx[5] * d[5] +
					cx[6] * d[6] +
					cx[7] * d[7] +
					cx[8] * d[8])
				yy = (
					cy[0] * d[0] +
					cy[1] * d[1] +
					cy[2] * d[2] +
					cy[3] * d[3] +
					cy[4] * d[4] +
					cy[5] * d[5] +
					cy[6] * d[6] +
					cy[7] * d[7] +
					cy[8] * d[8])
				zz = amp * math.sqrt(xx * xx + yy * yy)
				dat = int(zz)
				if(dat > 255):
					dat = 255
				self.img.putpixel((x, y), (dat, dat, dat))

	def labeling(self):
		"""labeling"""
		label = 100
		HIGH, LOW = 0xff, 0x00

		for y in range(self.height):
			for x in range(self.width):
				if self.img.getpixel((x, y))[0] == HIGH:
					label_set(self.img, (x, y), label)
					label += 1

		def label_set(img, pixel, label):
			width, height = img.size
			img.putpixel(pixel, (label, label, label))
			color = (label, label, label)

			while True:
				count = 0
				#for y in range(height):
				for y in range(pixel[1], height):
					for x in range(width):
						c = img.getpixel((x, y))[0]
						if c == label:
							xm = x - 1
							xp = x + 1
							ym = y - 1
							yp = y + 1
							if xm < 0:
								xm = 0
							if xp >= width:
								xp = width - 1
							if ym < 0:
								ym = 0
							if yp >= height:
								yp = height - 1

							if img.getpixel((xm, ym))[0] == HIGH:
								img.putpixel((xm, ym), color)
								count += 1
							if img.getpixel((x , ym))[0] == HIGH:
								img.putpixel((x , ym), color)
								count += 1
							if img.getpixel((xp, ym))[0] == HIGH:
								img.putpixel((xp, ym), color)
								count += 1
							if img.getpixel((xm, y ))[0] == HIGH:
								img.putpixel((xm, y ), color)
								count += 1
							if img.getpixel((x , y ))[0] == HIGH:
								img.putpixel((x , y ), color)
								count += 1
							if img.getpixel((xp, y ))[0] == HIGH:
								img.putpixel((xp, y ), color)
								count += 1
							if img.getpixel((xm, yp))[0] == HIGH:
								img.putpixel((xm, yp), color)
								count += 1
							if img.getpixel((x , yp))[0] == HIGH:
								img.putpixel((x , yp), color)
								count += 1
							if img.getpixel((xp, yp))[0] == HIGH:
								img.putpixel((xp, yp), color)
								count += 1
				if count == 0:
					break

	def label_split_color(self):
		src = self.img.copy()

		color = ((150, 0, 0), (0, 150, 0), (0, 0, 150), (150, 150, 0), (150, 0, 150), (0, 150, 150), (150, 150, 150), (200, 0, 0), (0, 200, 0), (0, 0, 200), (200, 200, 0), (200, 0, 200), (0, 200, 200), (200, 200, 200), (250, 0, 0,), (0, 250, 0), (0, 0, 250), (250, 250, 0), (250, 0, 250), (0, 250, 250), (250, 250, 250), (175, 0, 0), (0, 175, 0), (0, 0, 175), (175, 175, 0), (175, 0, 175), (0, 175, 175), (175, 175, 175))
		yet = []
		i = 0
		for y in range(self.height):
			for x in range(self.width):
				c = src.getpixel((x, y))[0]
				if c != 0 and c not in yet:
					if i >= len(color):
						#break
						i = 0
					color_fill(self.img, c, color[i])
					i += 1
					yet.append(c)

		def color_fill(img, p, color):
			for y in range(self.height):
				for x in range(self.width):
					c = img.getpixel((x, y))[0]
					if c == p:
						img.putpixel((x, y), color)

	def show_histgram(self):
		"""histgram"""
		HIGH = (0xff, 0xff, 0xff)
		LOW  = (0x00, 0x00, 0x00)

		hist = [0] * (0xff + 1)

		for y in range(self.height):
			for x in range(self.width):
				hist[self.img.getpixel((x, y))[0]] += 1

		hist_max = max(hist)
		ratio = 0
		if hist_max > 500:
			ratio = int(math.ceil(hist_max / 500))
			hist_max = 500

		size = (hist_max, 0xff)
		hist_image = Image.new('RGB', size)

		for y in range(size[1]):
			for x in range(size[0]):
				hist_image.putpixel((x, y), LOW)

		for y in range(size[1]):
			for x in range(int(hist[y] / ratio)):
				if x >= size[0]:
					continue
				hist_image.putpixel((x, y), HIGH)

		hist_image.show()

	def histgram_plane(self):
		"""histgram smoothing"""
		HIGH = 0xff
		LOW  = 0x00
		hist_range = []

		for y in range(self.height):
			for x in range(self.width):
				c = self.img.getpixel((x, y))[0]
				if c not in hist_range:
					hist_range.append(c)
		
		hist_ratio = (min(hist_range), max(hist_range))

		# z' = ((b' - a') / (b - a)) * (z - a) + a'
		buf = float(HIGH - LOW) / (hist_ratio[1] - hist_ratio[0])

		for y in range(self.height):
			for x in range(self.width):
				c = self.img.getpixel((x, y))[0]
				p = int(buf * (c - hist_ratio[0]) + LOW)
				self.img.putpixel((x, y), (p, p, p))

	def thinning(self):
		"""thinning"""

		HIGH = 0xff
		LOW  = 0x00

		def ncon(p):
			q = []
			n = 0
			for i in range(len(p)):
				if p[i] == 1 or p[i] == -1:
					q.append(0)
				else:
					q.append(1)
			for i in range(1, len(p), 2):
				i1 = i + 1
				i2 = i + 2
				if i2 == 9:
					i2 = 1
				n = n + q[i] - (q[i] * q[i1] * q[i2])
			return n

		tmp = (128, 128, 128) # temp
		flg = 1
		while flg != 0:
			flg = 0
			for y in range(1, self.height - 1):
				for x in range(1, self.width - 1):
					p = []
					p.append(self.img.getpixel((x    , y    ))[0])
					p.append(self.img.getpixel((x + 1, y    ))[0])
					p.append(self.img.getpixel((x + 1, y - 1))[0])
					p.append(self.img.getpixel((x    , y - 1))[0])
					p.append(self.img.getpixel((x - 1, y - 1))[0])
					p.append(self.img.getpixel((x - 1, y    ))[0])
					p.append(self.img.getpixel((x - 1, y + 1))[0])
					p.append(self.img.getpixel((x    , y + 1))[0])
					p.append(self.img.getpixel((x + 1, y + 1))[0])
					for k in range(len(p)):
						if p[k] == HIGH:
							p[k] = 1
						elif p[k] == LOW:
							p[k] = 0
						else:
							p[k] = -1
					if p[0] != 1:
						continue
					if (p[1] * p[3] * p[5] * p[7]) != 0:
						continue
					n = 0
					for k in range(1, len(p)):
						if p[k] != 0:
							n += 1
					if n < 2:
						continue
					n = 0
					for k in range(1, len(p)):
						if p[k] == 1:
							n += 1
					if n < 1:
						continue
					if ncon(p) != 1:
						continue
					n = 0
					for k in range(1, len(p)):
						if p[k] != -1:
							n += 1
						elif p[k] == -1:
							p[k] = 0
							if ncon(p) == 1:
								n += 1
							p[k] = -1
					if n < 8:
						continue
					self.img.putpixel((x, y), tmp)
					flg += 1
			for y in range(1, self.height - 1):
				for x in range(1, self.width - 1):
					if self.img.getpixel((x, y)) == tmp:
						self.img.putpixel((x, y), (LOW, LOW, LOW))

