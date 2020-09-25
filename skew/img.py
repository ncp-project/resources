import os

path = '/home/bhanu/net-centric/resources/skew'

for filename in os.listdir(path):
	if filename.endswith(".png") or filename.endswith(".jpg"):
		print(os.path.join(filename))
