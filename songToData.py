# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE, STDOUT
import os
from PIL import Image
import eyed3
import re

import SpectroImageTools as SIT

from sliceSpectrogram import createSlicesFromSpectrograms
from audioFilesTools import isMono, getGenre
from config import rawDataPath
from config import spectrogramsPath
from config import pixelPerSecond

#Tweakable parameters
desiredSize = 128
desiredHeight = 1024
withPhase = False

#Define
currentPath = os.path.dirname(os.path.realpath(__file__)) 

#Remove logs
eyed3.log.setLevel("ERROR")

#Create spectrogram from mp3 files
def createSpectrogram(filename,newFilename):
	#Create temporary mono track if needed
	if isMono(rawDataPath+filename):
		command = "cp '{}' '/tmp/{}.mp3'".format(rawDataPath+filename,newFilename)
	else:
		command = "sox '{}' '/tmp/{}.mp3' remix 1,2".format(rawDataPath+filename,newFilename)
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
	output, errors = p.communicate()
	if errors:
		print errors
	
	#Create spectrogram
	filename.replace(".mp3","")
	if withPhase == True :
		SIT.SoundToSpectroImage('/tmp/{}.mp3'.format(newFilename), '{}.png'.format( spectrogramsPath+newFilename ))
        else:
		command = "sox '/tmp/{}.mp3' -n spectrogram -Y {} -X {} -m -r -o '{}.png'".format(newFilename, desiredHeight+4, pixelPerSecond, spectrogramsPath+newFilename)
        	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
        	output, errors = p.communicate()
        	if errors:
            		print errors
	
	#Remove tmp mono track
	os.remove("/tmp/{}.mp3".format(newFilename))

#Creates .png whole spectrograms from mp3 files
def createSpectrogramsFromAudio():
	genresID = dict()
	files = os.listdir(rawDataPath)
	files = [file for file in files if file.endswith(".mp3")]
	nbFiles = len(files)

	#Create path if not existing
	if not os.path.exists(os.path.dirname(spectrogramsPath)):
		try:
			os.makedirs(os.path.dirname(spectrogramsPath))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	#Rename files according to genre
	for index,filename in enumerate(files):
		print "Creating spectrogram for file {}/{}...{}".format(index+1,nbFiles,rawDataPath+filename)
		#fileGenre = getGenre(rawDataPath+filename)
		fignr = getGenre(rawDataPath+filename)
		t = re.split('\W+',fignr)
		fileGenre = t[0]
		genresID[fileGenre] = genresID[fileGenre] + 1 if fileGenre in genresID else 1
		fileID = genresID[fileGenre]
		newFilename = fileGenre+"_"+str(fileID).zfill(5)
		#print "Creating spectrogram for file {}/{}...{}".format(index+1,nbFiles,newFilename)
		createSpectrogram(filename,newFilename)

#Whole pipeline .mp3 -> .png slices
def createSlicesFromAudio():
	print "Creating spectrograms..."
	createSpectrogramsFromAudio()
	print "Spectrograms created!"

	print "Creating slices..."
	createSlicesFromSpectrograms(desiredSize,desiredHeight)
	print "Slices created!"
