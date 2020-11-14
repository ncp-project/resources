import numpy as np
from skimage import io
from skimage.transform import rotate
from skimage.color import rgb2gray
from deskew import determine_skew
import os

from pdf2image import convert_from_path

from pdf2image.exceptions import (
 PDFInfoNotInstalledError,
 PDFPageCountError,
 PDFSyntaxError
)

path = '/home/abhishekbvs/repo/Pratilipi/resources/skew'
i = 0
images = convert_from_path('/home/abhishekbvs/repo/Pratilipi/resources/skew/skew11.pdf')
# convert the pdf into a series of images and save them
for i, image in enumerate(images):
	print('1')
	fname = 'image'+str(i)+'.png'
	image.save(fname, "PNG")

#search for images in the given path and deskew and save them
for filename in os.listdir(path):
	if filename.endswith(".png") or filename.endswith(".jpg"):
		i += 1
		print(os.path.join(path, filename))
		x = os.path.join(path, filename)
		image = io.imread(x)
		grayscale = rgb2gray(image)
		angle = determine_skew(grayscale)
		rotated = rotate(image, angle, resize=True) * 255
		io.imsave('output' + str(i) + '.png', rotated.astype(np.uint8))