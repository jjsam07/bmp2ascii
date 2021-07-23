import sys, struct, random

def charset(num):
	#['GE', 'ND', 'ER', chr(random.randrange(0x21, 0x40))+chr(random.randrange(0x21,0x40)), 'EQ', 'UA', 'LI', 'TY', chr(random.randrange(0x21, 0x40))+chr(random.randrange(0x21,0x40)), 'AN', 'D'+chr(random.randrange(0x21,0x40)), chr(random.randrange(0x21, 0x40))+chr(random.randrange(0x21,0x40)), 'EQ', 'UA', 'L'+chr(random.randrange(0x21,0x40)), chr(random.randrange(0x21, 0x40))+chr(random.randrange(0x21,0x40)), 'AC', 'CE', 'SS', chr(random.randrange(0x21, 0x40))+chr(random.randrange(0x21,0x40)), 'TO', chr(random.randrange(0x21, 0x40))+chr(random.randrange(0x21,0x40)), 'JU', 'ST', 'IC', 'E'+chr(random.randrange(0x21,0x40)), chr(random.randrange(0x21, 0x40))+chr(random.randrange(0x21,0x40))]
	
	return ['GE', 'ND', 'ER', chr(random.randrange(0x21, 0x40))+chr(random.randrange(0x21,0x40)), 'EQ', 'UA', 'LI', 'TY', chr(random.randrange(0x21, 0x40))+chr(random.randrange(0x21,0x40)), 'AN', 'D'+chr(random.randrange(0x21,0x40)), chr(random.randrange(0x21, 0x40))+chr(random.randrange(0x21,0x40)), 'EQ', 'UA', 'L'+chr(random.randrange(0x21,0x40)), chr(random.randrange(0x21, 0x40))+chr(random.randrange(0x21,0x40)), 'AC', 'CE', 'SS', chr(random.randrange(0x21, 0x40))+chr(random.randrange(0x21,0x40)), 'TO', chr(random.randrange(0x21, 0x40))+chr(random.randrange(0x21,0x40)), 'JU', 'ST', 'IC', 'E'+chr(random.randrange(0x21,0x40)), chr(random.randrange(0x21, 0x40))+chr(random.randrange(0x21,0x40))][num % 27]

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
	#counter = 0
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
					#sys.stdout.write('  ')
				else:
					fout.write(chr(random.randrange(0x21, 0x7f))+chr(random.randrange(0x21, 0x7f)))
					#fout.write('##')
					#sys.stdout.write('##')
				#counter += 1
		fout.write('\n')
		bitrange = 32
		#counter = counter % 27
		#sys.stdout.write('\n') 
		
		# GE ND ER || EQ UA LI TY || AN D| || EQ UA L| || AC CE SS || TO || JU ST IC E| ||
	
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