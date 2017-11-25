import os

param = ['Model Number', 'Serial Number', 'Firmware Revision', 'PIO', 'DMA',
	'Supported', 'device size with M = 1024*1024']

f = os.popen('sudo hdparm -I /dev/sda')
lst = f.readlines()
for i in lst:
	for parm in param:
		if parm in i:
			print(i)
			break

f = os.popen('df -m')
lst = f.readlines()

size = 0
used = 0
for i in list(lst)[1:]:
	size += int(i.split('\t')[0].split()[1])
	used += int(i.split('\t')[0].split()[2])
print("\tSize memory: ", size)
print("\n\tFree memory: ", size - used)
print("\n\tUsed memory: ", used)
