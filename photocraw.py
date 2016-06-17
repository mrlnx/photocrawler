#! /usr/bin/env python

import sys
import PIL
from PIL import Image
from PIL.ExifTags import TAGS
from os import walk
import os
import shutil

def main():

	try:
		input = sys.argv[1]
	
		if input and os.path.isdir(input):
			input_dir = input
		else:
			print "Insert the input argument!"
			exit()
	
	except IndexError:
		print "Insert the input argument!"
		exit()		

	try:
		output = sys.argv[2]
	
		if output and os.path.isdir(output):
			output_dir = output
		else:
			print "Insert the output argument"
			exit()

	except IndexError:
		print "Insert the output argument"
		exit()
	
	f = []
	for (dirpath, dirnames, filenames) in walk(input_dir):		

		for l in filenames:
			
			if not l.startswith('.'): 

				file = dirpath + "/" + l
	
				#print l

				if l.endswith('.jpeg') or l.endswith('.JPEG') or l.endswith('.jpg') or l.endswith('.JPG') or l.endswith('.png') or l.endswith('.PNG'):

					img = PIL.Image.open(file)
				
					if is_image_type(img, 'JPEG'):
						exif_data = img._getexif()
				
						try:
							created = get_field(exif_data, 'DateTime')
					
							date = splitter(created, " ", 0)
					
							if date:
								year = splitter(date, ":", 0)
								month = splitter(date, ":", 1)
								day = splitter(date, ":", 2)

								sorting(output_dir, file, day, month, year, 'JPEG')	
						except AttributeError:
							
							print "RORRIE = aanwezig; geen EXIF bij '" + l + "' en door!"						

					elif is_image_type(img, 'PNG'):
						sorting(output_dir, file, '',  '', '', 'PNG')
				
				elif l.endswith('.avi') or l.endswith('.AVI') or l.endswith('.mpeg') or l.endswith('.MPEG') or l.endswith('.mp4') or l.endswith('.MP4') or l.endswith('.mov') or l.endswith('.MOV'):
					#print 'file :: ' + l
					sorting(output_dir, file, '',  '', '', 'video')
				
				elif l.endswith('.pdf') or l.endswith('.PDF') or l.endswith('.doc') or l.endswith('.DOC'):
				
					#print 'file :: ' + l
					sorting(output_dir, file, '', '', '', 'documents')

def sorting(output, file, day, month, year, type):
	
	#print file + " :: " + day + "-" + month + "-" + year
	
	if os.path.exists(file):
	
		if type == 'JPEG':
			year_dir = output + "/" + year
			if os.path.isdir(year_dir):
	
				month_dir = year_dir + "/" + month
				if os.path.isdir(month_dir):
				
					shutil.copy(file, month_dir)
				else:
					# create month dir
					# call function gain

					os.makedirs(month_dir)

					print month_dir + " created!"

					sorting(output, file, day, month, year, type)
			else:
				# create year dir
				# call function again
			
				os.makedirs(year_dir)

				print year_dir + " created"
	
				sorting(output, file, day, month, year, type)			

		elif type == 'PNG':
			
			png_dir = output + '/png' 

			if os.path.isdir(png_dir):

				shutil.copy(file, png_dir)
			else:
				os.makedirs(png_dir)

				print png_dir + " created!"

				sorting(output, file, day, month, year, type)
		else:
			
			if type == 'video':
				
				video_dir = output + '/video'				

				if os.path.isdir(video_dir):
					shutil.copy(file, video_dir)
				else:
					os.makedirs(video_dir)
        
					print video_dir + " created!"
	
	                        	sorting(output, file, day, month, year, type)
		
			elif type == 'documents':

                                documents_dir = output + '/documents'
                                
                                if os.path.isdir(documents_dir):
                                        shutil.copy(file, documents_dir)
                                else:
                                        os.makedirs(documents_dir)

					print documents_dir + " created!"

                                        sorting(output, file, day, month, year, type)


def splitter(date, delimiter, num):
	
	if type(date) == str:
		split = date.split(delimiter)
		return split[num]


def get_field (exif,field):

	for (k,v) in exif.iteritems():
		if TAGS.get(k) == field:
        		return v


def is_image_type(img, type):
	try:
		return img.format == type
	except IOError:
		return False
		

if __name__ == '__main__':
	main()
	sys.exit()
