import sys, struct, random

def getData(f, addr):
	f.seek(addr)
	return struct.unpack('>I', f.read(4))[0]

def imgWidth(f):
	f.seek(0x12)
	return struct.unpack('<I', f.read(4))[0]
	
def imgHeight(f):
	f.seek(0x16)
	return struct.unpack('<I', f.read(4))[0]
	
def pxArrStart(f):
	f.seek(0xA)
	return struct.unpack('<I', f.read(4))[0]
	
def bmp2ascii(fin, fout):
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
	
def main():
	count = 1
	for i in sys.argv:
		if i == '-o':
			fout = open(sys.argv[count], 'wb')
			count += 1
			continue
		if i == '-i':
			fin = open(sys.argv[count], 'rb')
			count += 1
			continue
		count += 1
		
	bmp2ascii(fin, fout)
	fin.close()
	fout.close()
		
	

if __name__ == '__main__':
	main()