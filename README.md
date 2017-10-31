# GelDoc-Scanner
#Copyright 2017 Himanshu Patange
#This software is released under GNU public licence

The software is submitted in the iGEM-2017 compitition under the software tools category by the team IISER-Mohali-India. 
Scans gel doc slides and gives out band sizes as output.

Prerequisites:
	- Python 2.7
		link:- https://www.python.org/downloads/
	- OpenCV for python (cv2)
		link:- https://opencv.org/releases.html
	- Matplotlib
		https://matplotlib.org/downloads.html or install via pip
	- Numpy
		https://pypi.python.org/pypi/numpy or install via pip

Format:
	
	script_name.py img_name mode threshold saveorno
	
	script_name: name of the script
	img_name: Name of the image, with extension
	mode: man or auto
	threshold: Threshold value for detection
	saveorno: save or leave blank if settings aren't to be saved



This software takes a gel doc slide image as input and gives out band sizes for the detected bands in the lanes specified. There is a manual mode (man) in which you can choose which slides are to be analyzed, and whether or not to see the 2D graph for ease of detection. The auto mode can automate this task for all lanes.

In future we would like to introduce machine learning algorithms in it to give better detection and analysis performance.
