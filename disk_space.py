import os

def get_space_remaining(path = '.'):
	'''
	Returns the number of bytes the user has access to
	
	Parameters:
	path: path enclosed by the device to be measured (default is this path)
	'''
	filesystem_info = os.statvfs(path)
	#return the block size times the number of blocks the user can use
	return filesystem_info.f_frsize * filesystem_info.f_bavail

def have_more_space_than(threshold, path = '.'):
	'''
	Checks if there is more space on the device than the threshold 
	
	Parameters:
	threshold: the minimum number of bytes the device should hold to return True
	path: path enclosed by the device to be measured (default is this path)
	'''
	if get_space_remaining() < threshold:
		return False
	else:
		return True
	
if __name__ == '__main__':
	print(get_space_remaining())
	minimum = 100000000 #100 MB
	print(have_more_space_than(minimum))