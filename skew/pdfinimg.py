import fitz

def imInPdf(path):
    doc = fitz.open(path)
    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:       # this is GRAY or RGB
                pix.writePNG('/home/bhanu/net-centric/resources/skew/impdf/'+"p%s-%s.png" % (i, xref))
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.writePNG('/home/bhanu/net-centric/resources/skew/impdf/'+"p%s-%s.png" % (i, xref))
                pix1 = None
            pix = None

imInPdf('/home/bhanu/net-centric/resources/skew/check/file.pdf')