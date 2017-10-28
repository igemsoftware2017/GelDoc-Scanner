import cv2
from matplotlib import pyplot as plt
import os
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from numpy import sign
from sys import argv

global lowest

try:
	script, img, mode, lowest, saveorno = argv
except ValueError:
	script, img, mode,lowest = argv
	saveorno = 'no'

class Start(object):
	
	def imgread(self,img_path):
		img = cv2.imread(img_path)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)		
		return img

class View(object):

	def __init__(self,command):
		if command == 1:
			self.threshold = int(lowest)
		if command ==2:
			self.threshold = 0
	
	def TwoD(self, img,lanes,lane,command,y):
		i = lanes[lane]
		val = []
		for j in y:
			if int(img[j][i[0]])>self.threshold:
				val.append(int(img[j][i[0]]))
			else:
				val.append(0)
		
		der = [0]
		for k in range(1,len(val)):
			der.append(val[k]-val[k-1])
		
		if command != "Don't view":
			plt.plot(y,val)
			plt.plot(y,der)
			plt.show()

		else:
			return val, der
	
	def ThreeD(self, img, h, w):
		x = []; y = []; z = []
		img = cv2.flip(img,0)

		for i in range(w):
			for j in range(1,h):
				#diff = img[j,i]-img[j-1,i]		#might work when image isn't shitty
				val = img[j,i]
				#if diff > 50:
				if val >190:
					x.append(i)
					y.append(j)
					#z.append(val)
		
		plt.scatter(x,y)
		plt.show()

		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		ax.scatter(x,y,z,c='r',marker=',')
		
		ax.zaxis.set_major_locator(LinearLocator(10))
		ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
		ax.set_xlabel('X Label')
		ax.set_ylabel('Y Label')
		ax.set_zlabel('Z Label')

		plt.show()

class Prelim(object):
	
	def xy(self,event,x,y,flags,param):
		global mouseX, mouseY
		if event == cv2.EVENT_RBUTTONDOWN:
			cv2.circle(img_temp,(x,y),2,(255,0,0),-1)
			mouseX = x
			mouseY = y
	
	def Select_ROI(self,img):
		
		print "\n\nRight click on two diagonally opposite corners of the\nregion encompassing all the lanes."
		print "\nPress Esc to quit, and r to retry.\n"
		
		global img_temp
		img_temp = np.array(img)
		cv2.namedWindow('Slide')
		cv2.setMouseCallback('Slide',self.xy)
		
		corners = []
		global mouseX, mouseY

		while len(corners) != 2:
			mouseX, mouseY = 'x','y'
			cv2.imshow('Slide',img_temp)			
			k = cv2.waitKey(1) & 0xFF


			if k == ord('r'):
				corners = []
				img_temp = np.array(img)

			elif k == 27:
				break
			
			
			if mouseX != 'x':
				corners.append((mouseX,mouseY))
			else:
				continue
		cv2.destroyAllWindows()
		
		return img,corners
	
	def Select_Lanes(self,img):
		
		print "\n\nSelect the lanes you want analyzed by Right Clicking"
		print "on their midpoints(approximate).\n"
		print "Please select the standard lane first."
		print "\nPress d when done."
		print "Press r to reset.\n"

		cv2.namedWindow('Slide')
		cv2.setMouseCallback('Slide',self.xy)
		global img_temp
		img_temp = np.array(img)
		lanes = []
		while(1):
			global mouseX, mouseY
			mouseX = 'x'; mouseY = 'y'
			
			cv2.imshow('Slide',img_temp)
			k = cv2.waitKey(1) & 0xFF

			if k == ord('r'):
				lanes = []
				img_temp = np.array(img)
			elif k == ord('d'):
				if len(lanes) == 1:
					print "Please select at least two lanes."
					print "press esc to quit."
					img_temp = np.array(img)
					lanes = []
					continue
				break
			elif k == 27:
				break

			if mouseX != 'x':
				lanes.append((mouseX,mouseY))
			else:
				continue
		
		cv2.destroyAllWindows()
		return lanes

class Analysis(object):
	
	def analyze(self, img, lanes, corners,y):
		global pos
		pos = {}
		std_lane = []
		command = 1
		get = View(command)

		for i in lanes:
			if lanes.index(i) != 0:
				pos['Lane '+str(lanes.index(i))] = []

			val, der = get.TwoD(img,lanes,lanes.index(i),"Don't view",y)
			loc = []
			for l in range(1,len(der)):
				if (sign(der[l-1]) == 0 or sign(der[l-1]) == 1) and sign(der[l]) == -1:
					if lanes.index(i) == 0:
						std_lane.append(l)
					else:
						loc.append(l)
			
			if lanes.index(i) != 0:
				std_lane = np.array(std_lane)
				loc = np.array(loc)
				
				for m in loc:
					position = 0
					position1 = 0
					position2 = 0
					temp = std_lane-m
					abstemp = abs(temp)
					location = min(abstemp)
					abstemp = list(abstemp)
					location1 = abstemp.index(location)
					location1 = temp[location1]
					position1 = standard_lane[list(temp).index(location1)]
					
					if location1 == 0:
						location = location1
						location2 = location1
						diff = 0
					else:
						location = 's'
						if location1 > 0:
							if list(temp).index(location1) != 0:
								location2 = temp[list(temp).index(location1)-1]
								position2 = standard_lane[list(temp).index(location2)]
								step = -(abs(location1)+abs(location2))/10.0
							else:
								location2 = location1
								location = location1
						else:
							if list(temp).index(location1) != len(temp)-1:
								location2 = temp[list(temp).index(location1)+1]
								position2 = standard_lane[list(temp).index(location2)]
								step = (abs(location1)+abs(location2))/10.0
							else:
								location2 = location1
								location = location1
						diff = (position2-position1)/10.0
					
					if location1 != location:
						scale = np.arange(location1,location2,step)
						abstemp = abs(scale)
						location = min(abstemp)
						abstemp = list(abstemp)
						location = abstemp.index(location)
						position = position1+diff*location
						location = location1+step*location
					else:
						position = position1
						position2 = position1
					
					pos['Lane '+str(lanes.index(i))].append(position)

		for i in pos.keys():
			if len(pos[i]) != 0:
				print i,': ',
				for j in range(len(pos[i])):
					if j != len(pos[i])-1:
						print pos[i][j],
					else:
						print pos[i][j]
			else:
				pass

class Engine(object):

	def __init__(self, mode,img):
		Open = Start()
		self.img = Open.imgread(img)

	def Prepare(self,img,mode,saveorno):
		
		global standard_lane
		if mode == 'man':
			img,corners = Prelim().Select_ROI(img)
			try:
				W = abs(corners[1][0]-corners[0][0])
			except IndexError:
				exit(0)
			H = abs(corners[1][1]-corners[0][1])
			
			img = cv2.resize(img, None, fx = 500/float(W), fy = 250/float(H), interpolation = cv2.INTER_CUBIC)
			corner1 = (corners[0][0]*500/float(W),corners[0][1]*250/float(H))
			corner2 = (corners[1][0]*500/float(W),corners[1][1]*250/float(H))
			corners = [corner1,corner2]
			
			lanes = Prelim().Select_Lanes(img)
			
			standard_lane = []
			if saveorno == 'save':
				inp = None
				print "Please provide the standard lane band sizes."
				print "At the prompt, type in the values of the band sizes"
				print "of the standard ladder bands that you are using one"
				print "by one and press enter."
				print "When done, press d and hit enter."
				while inp != 'd':
					inp = raw_input()
					try:
						inp = float(inp)
						standard_lane.append(inp)
					except ValueError:
						if inp != 'd':
							print "Please provide valid numbers."
							continue					
				
				os.system('mkdir settings')
				fil = open('settings/settings.py','w')
				fil.write('corners = '+str(corners)+'\nlanes = '+str(lanes)+'\nshape  = '+str(img.shape)+'\npos = '+str(standard_lane))
				fil.close()

			else:
				try:
					sys.path.append('settings')
				except:
					print 'No settings were found. You might want to create settings through the manual mode first.'
					exit(0)
				try:
					from settings import pos
					standard_lane = pos[:]
				except:
					print 'Standard Ladder readings weren\'t found.\nTo use manual mode, please create the standard ladder readings first'
					exit(0)
		
		elif mode == 'auto':
			try:
				sys.path.append('settings')
			except:
				print 'No settings were found. You might want to create settings through the\nmanual mode first.'
				exit(0)
			try:
				from settings import corners,lanes,shape,pos
				standard_lane = pos[:]
				img = cv2.resize(img,(shape[1],shape[0]),interpolation=cv2.INTER_CUBIC)
				
			except:
				print 'No settings were found.\nYou might want to create settings through the manual mode first.'
				exit(0)
		
		return img,corners,lanes
	
	def take_commands(self,img,lanes,corners,y):
		
		self.commands = {1:'Do the complete analysis of the lanes specified.',
							2: 'View the 2D graph of the lanes specified.'}
		
		if mode == 'man':
			print '\nSelect command by pressing the command number.'
			for i in self.commands:
				print i,':',self.commands[i]
			self.command = int(raw_input())
		
		elif mode == 'auto':
			self.command = 1
		
		if self.command == 2:
			print "\nThe lanes range from 1 to ", len(lanes)-1
			lane = 'kl'
			while lane.isdigit() != True:
				lane = raw_input("Which lane do you want to see?")
				if lane.isdigit() != True:
					print 'Please type a number.'
				else:
					lane = int(lane)
					if lane > len(lanes)-1:
						print lane, len(lanes)-1
						print "Please type a valid lane number."
						lane = 'kl'
					lane = str(lane)			
			View(self.command).TwoD(img,lanes,int(lane),"View",y)
		
		elif self.command == 1:
			self.complete(img,lanes,corners,y,mode)
	
	def complete(self,img,lanes,corners,y,mode):
		inp = 0
		command = 1
		Analysis().analyze(img,lanes,corners,y)
		if mode == 'auto':
			exit(0)

def Run(img_path,mode,saveorno):
	a = 0
	while a == 0:
		start = Engine(mode,img_path)
		img,corners,lanes= start.Prepare(start.img,mode,saveorno)
		y = range(int(corners[0][1]), int(corners[1][1]))
		
		while(1):
			start.take_commands(img,lanes,corners,y)
			cv2.destroyAllWindows()
			if mode == 'man':
				break

Run(img,mode,saveorno)