import numpy as np
from skimage import io
from skimage.transform import rotate
from skimage.color import rgb2gray
from deskew import determine_skew
import os
import fitz
from pdf2image import convert_from_path

from pdf2image.exceptions import (
 PDFInfoNotInstalledError,
 PDFPageCountError,
 PDFSyntaxError
)
i = 0

def imInPdf(path):
    doc = fitz.open(path)
    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:       # this is GRAY or RGB
                print("Saving images in the pdf")
                pix.writePNG('/home/bhanu/net-centric/resources/skew/impdf/'+"p%s-%s.png" % (i, xref))
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                print("Saving images in the pdf")
                pix1.writePNG('/home/bhanu/net-centric/resources/skew/impdf/'+"p%s-%s.png" % (i, xref))
                pix1 = None
            pix = None


path = '/home/bhanu/net-centric/resources/skew/check/'
path1 = '/home/bhanu/net-centric/resources/skew/impdf/'
path2 = '/home/bhanu/net-centric/resources/skew/pdf2img/'

for filename in os.listdir(path):
    if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
        i += 1
        print("Detecting and deskewing the given images")
        print(os.path.join(path, filename))
        x = os.path.join(path, filename)
        image = io.imread(x)
        grayscale = rgb2gray(image)
        angle = determine_skew(grayscale)
        rotated = rotate(image, angle, resize=True) * 255
        print("Saving the deskewed images")
        io.imsave("/home/bhanu/net-centric/resources/skew/deskew/" + 'deskew' + str(i) + '.png', rotated.astype(np.uint8))

    elif filename.endswith('.pdf'):
        imInPdf(path + filename)
        for files in os.listdir(path1):
            if files.endswith(".png"):
                print("Detecting and deskewing images inside pdf")
                print(os.path.join(path1, files))
                x = os.path.join(path1, files)
                image = io.imread(x)
                grayscale = rgb2gray(image)
                angle = determine_skew(grayscale)
                rotated = rotate(image, angle, resize=True) * 255
                print("Saving the deskewed images")
                io.imsave("/home/bhanu/net-centric/resources/skew//deskew" + 'deskew' + str(i) + '.png', rotated.astype(np.uint8))
        images = convert_from_path('/home/bhanu/net-centric/resources/skew/check/'+ filename)
        
        for j, image in enumerate(images):
            fname = 'image'+str(j)+'.png'
            image.save('/home/bhanu/net-centric/resources/skew/pdf2img/' + fname, "PNG")
        
        for filex in os.listdir(path2):
            if filex.endswith(".png"):
                print("Detecting and deskewing pdf file")
                print(os.path.join(path2, filex))
                x = os.path.join(path2, filex)
                image = io.imread(x)
                grayscale = rgb2gray(image)
                angle = determine_skew(grayscale)
                rotated = rotate(image, angle, resize=True) * 255
                print("Saving the deskewed images")
                io.imsave("/home/bhanu/net-centric/resources/skew/dspdf/" + 'deskew' + str(i) + '.png', rotated.astype(np.uint8))



