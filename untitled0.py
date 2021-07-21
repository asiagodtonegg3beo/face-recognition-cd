from flask import Flask,render_template,url_for,redirect,request,session
import json,os,time,cv2,shutil
import numpy as np
import os

def fill_photo(img,out_path):

	width=150
	h,w=img.shape[0],img.shape[1]
	side=max(h,w)
	new = np.zeros((side,side,3), np.uint8)
	new.fill(255)
	if w>h:
		center=((side-h)/2.0)
		for i in range(img.shape[0]):
			for j in range(img.shape[1]):			
				new[int(i+center),j]=img[i,j]
	else:
		center=((side-w)/2.0)
		for i in range(img.shape[0]):
			for j in range(img.shape[1]):			
				new[i,int(j+center)]=img[i,j]

	ratio= width * 1.0 / side
	new=cv2.resize(new, None, fx=ratio, fy=ratio)
	cv2.imwrite(out_path, new)


path = 'C:/Users/FuckYouBitch/Desktop/3B10_python/static/uploads/B0642003/test/album/photo/B0642003_32.jpg'
ou_path='C:/Users/FuckYouBitch/Desktop/3B10_python/static/uploads/B0642003/test/album/'

#for i in os.listdir(path):
image=cv2.imread(path)
fill_photo(image,ou_path)
