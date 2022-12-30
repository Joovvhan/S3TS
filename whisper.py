from glob import glob
import os
import re

def get_youtube_vid(file_name):
	vid = re.search(r'\[.{11}\]', file_name)[0].strip('[]')
	return vid

if __name__ == "__main__":

	audio_dir = './raw_audio'
	transcription_dir = './transcripts'

	raw_audio_files = sorted(glob(f'{audio_dir}/*.webm'))
	
	processed_ids = set([get_youtube_vid(file) for file in glob(f'{transcription_dir}/*.srt')])

	unprocess_audio_files = [file for file in raw_audio_files if get_youtube_vid(file) not in processed_ids]

	for file in unprocess_audio_files:
		os.system(' '.join(['whisper', f'"{file}"', '--language Korean', '--model medium', '-o ./transcripts']))