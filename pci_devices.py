import os

f = os.popen('lspci -vmm')
lst = f.readlines()

for i in lst:
	if 'Vendor' in i and 'SVendor' not in i:
		print(i.rstrip())
	if 'Device' in i:
		print(i)