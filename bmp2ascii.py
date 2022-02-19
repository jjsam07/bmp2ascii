#	Reference: Bits to Bitmaps: A simple walkthrough of BMP Image Format
#	From: medium.com
#
#	Block 1: File Type Data
#	This block is a BMP Header labeled as BITMAPFILEHEADER (the name comes from
#	c++ struct in Windows OS). This is the starting point of the BMP file and has
#	14 bytes width. This header contains a total of 5 fields of variable byte width.
#	These are mentioned in the below table.
#
#	Address 0x0
#
#	FileType (0x0)				2 bytes		A 2 character string value in ASCII to specify a DIB file type.
#											It must be 'BM' or '0x42 0x4D' in hexadecimals for modern
#											compatibility reasons.
#
#	FileSize (0x2)				4 bytes		An integer (unsigned) representing entire file size in bytes.
#											This value is basically the number of bytes in a BMP image file.
#
#	Reserved (0x6)				2 bytes		These 2 bytes are reserved to be utilized by an image processing
#											application to add additional meaningful information. It should be
#											initialized to '0' integer (unsigned) value.
#
#	Reserved (0x8)				2 bytes		Same as the above.
#
#	PixelDataOffset (0xA)		4 bytes		An integer (unsigned) representing the offset of actual pixel data
#											in bytes. In nutshell:- it is the number of bytes between start of
#											the file (0) and the first byte of the pixel data.
#	----						----		----
#	Total						14 bytes	Size of the BITMAPFILEHEADER in bytes.
#
#	One thing to remember is that BMP uses the little-endian system to store a
#	number (integer or float) when a number is larger than 1-byte.
#	
#	For example, 312 decimal value in 2-bytes binary is 00000001 00111000 and its
#	hex byte representation is 0x01 0x38. Similarly, in 4-bytes, it is 00000000
#	00000000 00000001 00111000 or 0x00 0x00 0x01 0x38.
#	
#	But in the little-endian system (in modern computers), the least-significant byte
#	(LSB) is stored first. Therefore, 312 decimal value in hex byte representation
#	will be 0x38 0x01 0x00 0x00 and BMP will construct binary value like
#	RHS: 0x38 <- 0x01 <- 0x00 <- 0x00 :LHS.
#
import sys, struct, random

def isprint(c):
	if (c > 0x20) and (c < 0x7E):
		return c
	else:
		return random.randrange(0x20, 0x7E)
             
def pxAvg(f, addr):
	f.seek(addr)
	px1 = struct.unpack('B', f.read(1))[0]
	px2 = struct.unpack('B', f.read(1))[0]
	px3 = struct.unpack('B', f.read(1))[0]
	avg = (px1 + px2 + px3)/3
	
	if (avg >= 0) and (avg <= 7):
		return "  "
	elif (avg >= 8) and (avg <= 15):
		return " `"
	elif (avg >= 16) and (avg <= 23):
		return "``"
	elif (avg >= 24) and (avg <= 31):
		return " ."
	elif (avg >= 32) and (avg <= 39):
		return " ~"
	elif (avg >= 40) and (avg <= 47):
		return " -"
	elif (avg >= 48) and (avg <= 55):
		return ".."
	elif (avg >= 56) and (avg <= 63):
		return " ,"
	elif (avg >= 64) and (avg <= 71):
		return "-."
	elif (avg >= 72) and (avg <= 79):
		return ".~"
	elif (avg >= 80) and (avg <= 87):
		return " *"
	elif (avg >= 88) and (avg <= 95):
		return ".:"
	elif (avg >= 96) and (avg <= 104):
		return "--"
	elif (avg >= 104) and (avg <= 111):
		return "=~"
	elif (avg >= 112) and (avg <= 119):
		return "=="
	elif (avg >= 120) and (avg <= 127):
		return "!!"
	elif (avg >= 128) and (avg <= 135):
		return "ii"
	elif (avg >= 136) and (avg <= 143):
		return "i?"
	elif (avg >= 144) and (avg <= 151):
		return "**"
	elif (avg >= 152) and (avg <= 159):
		return "il"
	elif (avg >= 160) and (avg <= 167):
		return "//"
	elif (avg >= 168) and (avg <= 175):
		return "[]"
	elif (avg >= 176) and (avg <= 183):
		return "[["
	elif (avg >= 184) and (avg <= 191):
		return ".$"
	elif (avg >= 192) and (avg <= 199):
		return ".#"
	elif (avg >= 200) and (avg <= 207):
		return ".%"
	elif (avg >= 208) and (avg <= 215):
		return ".@"
	elif (avg >= 216) and (avg <= 223):
		return "oo"
	elif (avg >= 224) and (avg <= 231):
		return "$$"
	elif (avg >= 232) and (avg <= 239):
		return "##"
	elif (avg >= 240) and (avg <= 247):
		return "%%"
	elif (avg >= 248) and (avg <= 255):
		return "@@"
	
def getData(f, addr):
	f.seek(addr)
	return struct.unpack('>I', f.read(4))[0]

def pxArrStart(f):
	f.seek(0xA)
	return struct.unpack('<I', f.read(4))[0]

def imgWidth(f):
	f.seek(0x12)
	return struct.unpack('<I', f.read(4))[0]
	
def imgHeight(f):
	f.seek(0x16)
	return struct.unpack('<I', f.read(4))[0]
	
def colorDepth(f):
	f.seek(0x1C)
	return struct.unpack('<H', f.read(2))[0]

def bmp2ascii_monochrome(fin, fout):
	if (imgWidth(fin) % 32) > 0:
		width = (imgWidth(fin) + (32 - (imgWidth(fin) % 32)))/8
	else:
		width = imgWidth(fin)/8
	
	iwidth = imgWidth(fin)
	arrStart = pxArrStart(fin)
	height = imgHeight(fin)	
	pixelData = 0
	boundary = range(0, width, 4)[-1:][0]
	bitrange = 32
	
	print("Array start = {}\nByteWidth = {}\nWidth = {}\nHeight = {}\nBoundary = {} \n".format(arrStart, width, imgWidth(fin), height, boundary))
	
	for i in range(height-1, -1, -1):
		for j in range(0, width, 4):
			if j == boundary:
				bitrange = imgWidth(fin) % 32
			pixelData = getData(fin, arrStart+j+(width*i))
			for k in range(0, bitrange):
				if (pixelData & (0x80000000 >> k)) != 0:
					fout.write('  ')
				else:
					fout.write('##')
		fout.write('\n')
		bitrange = 32
	
def bmp2ascii_greyscale(fin, fout):
	arrStart = pxArrStart(fin)
	iwidth = imgWidth(fin)
	width = (colorDepth(fin)*iwidth)/8
	height = imgHeight(fin)
	px = 0
	
	print("Pixel array start = {}\nWidth (bytes) = {}\nWidth (px) = {}\nHeight (px) = {}\nColor depth = {} bit\n".format(arrStart, width, imgWidth(fin), height, colorDepth(fin)))
	
	for i in range(height-1, -1, -1):
		for j in range(0, width, 3):
			#px = isprint(pxAvg(fin, arrStart+j+(width*i)))
			px = pxAvg(fin, arrStart+j+(width*i))
			#fout.write("{:c}{:c}".format(px, px))
			fout.write(px)
		fout.write('\n')

def main():
	count = 1
	mode = 0
	for i in sys.argv:
		if i == '-o':
			fout = open(sys.argv[count], 'wb')
			count += 1
			continue
		if i == '-i':
			fin = open(sys.argv[count], 'rb')
			count += 1
			continue
		if (i == '-m') and (mode == 0):
			mode = 'm'
			count += 1
			continue
		if (i == '-g') and (mode == 0):
			mode = 'g'
			count += 1
			continue
		count += 1
		
	if (mode == 'm'):
		bmp2ascii_monochrome(fin, fout)
	elif (mode == 'g'):
		bmp2ascii_greyscale(fin, fout)
	else:
		print("Specify a mode bro! (-m | -g)\n")
	
	fin.close()
	fout.close()
		
def printable():
	for i in range(0, 0xFF, 1):
		print("{:X}: {:c}\n".format(i,i))

if __name__ == '__main__':
	main()