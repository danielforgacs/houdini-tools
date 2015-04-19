#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python version 3.4

'''after grabbing thousands of frames for your showreel
whatever you're using puts the jpg or png, etc sequences
in a specific folder. all file in the same folder.
mark the braking points in the "frame_ranges" variable
and this script handles the rest. puts shots in a numbered
folder and deletes whats marked to be deleted. This way you
don't need to go frame by frame in a blue ray, it's enough
to check a smaller file size image sequence.
update folder and show name variables'''

__author__		= "Daniel Forgacs"
__version__		= "1.0"
__email__		= "forgacs.daniel@gmail.com"

# code:

import		shutil
import		os

# update frame range like this:
frame_ranges = '''818 - 901
902 - 1792 DELETE
1793 - 1979
1980 - 2007 DELETE
2008 - 2154
14762 - 14813
14814 - 15265 DELETE
15266 - 15404
15405 - 15527
15528 - 16348 DELETE
16349 - 16363
16364 - 16412
16413 - 16457 DELETE
16458 - 16482
16483 - 16526
16527 - 16757 DELETE
16758 - 16819
16820 - 25969 DELETE
25970 - 28255
28256 - 35430'''

base_path			= 'd:/<PUT FOLDER HERE>/'

# returns file name and move file name with padded frame number
def get_filename(frame_number, folder):
	padding			= 6
	filename		= '<PUT FILENAME HERE>'
	frame_number	= '{}{}'.format('000000', frame_number)[-padding:]
	extension		= 'jpg'

	return ('{}{}.{}.{}'.format(base_path, filename, frame_number, extension), '{}{}/{}.{}.{}'.format(base_path, folder, filename, frame_number, extension))


# deletes or organizes frame sequences
def main():
	# frame_ranges		= frame_ranges.split('\n')
	for k, frames in enumerate(frame_ranges.split('\n')):

		# loop in range
		for i in range(int(frames.split()[0]), int(frames.split()[2]) + 1):

			dir_name	= '<PUT COPY DIRECTORY NAME HERE>_{}'.format('{}{}'.format('0000', k+1)[-2:])
			filename	= get_filename(i, dir_name)

			print(filename)
		
		# check if delete or organize:
			if 'DELETE' in frames:
				# pass
				os.remove(filename[0])

			else:
				if not os.path.exists(base_path + dir_name):
					os.mkdir(base_path + dir_name)

				shutil.move(filename[0], filename[1])

if __name__ == '__main__':
	main()