

import os

if __name__ == "__main__":

	with open('links.txt', 'r') as f:
		lines = [line.strip() for line in f.readlines()]

	# for line in lines:
	# 	os.system(' '.join(['yt-dlp', '-f', '140', '-P', '"./raw_audio"', f'{line}'])) # m4a
	for line in lines:
		os.system(' '.join(['yt-dlp', '-f', 'ba', '-P', '"./raw_audio"', f'{line}'])) # webm