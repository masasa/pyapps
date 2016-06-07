#!/usr/bin/python
import os
import argparse

# this function copy files unless it got arument move as True, then
# instead of copying the file it moving the file
def file_copy(src_file, dst_file, move = False):

	# incase source file does not exist
	if not os.path.exists(src_file):
		print '{} does not exit in system'.format(src_file)
		raise SystemExit(2)

	if move:
		# moving source file to desstenation file
		os.rename(src_file, dst_file)
		print '{} was moved successfully to {}'.format(src_file, dst_file)
	else:
		# copying source file to desstenation file
		file(dst_file, 'wb').write(file(src_file, 'rb').read())
		print '{} was copied successfully to {}'.format(src_file, dst_file)

def main():

	# parsing user arguments input
	parser = argparse.ArgumentParser()
	parser.add_argument('src_file', help='Path to source file')
	parser.add_argument('dst_file', help='Path to destenation file')
	
	# parse optional arguments for copying or moving respectively
	parser.add_argument('-c', '--copy', help='Copy source file onto destination path',
						default=False, action='store_true')
	parser.add_argument('-m', '--move', help='Move source file to destenation path',
						default=False, action='store_true')
	
	# won't do anything and here to show example of getting argument with value like -n 5
	# will create 5 copies
	parser.add_argument('-n', '--copies', help='Number of copies to create (not working on purpose)')
	args = parser.parse_args()

	if(args.move):
		# move the file
		file_copy(args.src_file, args.dst_file, move=True)
	else:
		# copy the file
		file_copy(args.src_file, args.dst_file)


if __name__ == '__main__':
	main()
