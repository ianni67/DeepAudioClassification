# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np

#Returns numpy image at size imageSize*imageSize
def getProcessedData(img,imageSize, sliceHeight):
    img = img.resize((imageSize,sliceHeight), resample=Image.ANTIALIAS)
    imgData = np.asarray(img, dtype=np.uint8).reshape(imageSize, sliceHeight,1)
    imgData = imgData/255.
    return imgData

#Returns numpy image at size imageSize*imageSize
def getImageData(filename,imageSize, sliceHeight):
    img = Image.open(filename)
    imgData = getProcessedData(img, imageSize, sliceHeight)
    return imgData
