import os
import re
from glob import glob

from tqdm.auto import tqdm

def read_srt_file(file):

    with open(file, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    index = lines[0::4]
    times = lines[1::4]
    texts = lines[2::4]

    times = [time_str.split(' --> ') for time_str in times]

    return times

def get_youtube_vid(file_name):
	vid = re.search(r'\[.{11}\]', file_name)[0].strip('[]')
	return vid

if __name__ == "__main__":

    audio_dir = './raw_audio'
    # transcription_dir = './transcripts'
    transcription_dir = './filtered_transcripts'
    segment_dir = './audio_segments'
    srt_files = sorted(glob(f'{transcription_dir}/*.srt'))

    simul_output_num = 64

    raw_audio_files = sorted(glob(os.path.join(audio_dir, '*.webm')))

    for srt_file in srt_files:
        # audio_file = srt_file.replace(transcription_dir, audio_dir).rstrip('.srt')
        vid = get_youtube_vid(srt_file)
        for raw_audio_file in raw_audio_files:
            if vid in raw_audio_file:
                audio_file = raw_audio_file

        assert os.path.isfile(audio_file), f"{audio_file} does not exist"

        segment_path = os.path.join(segment_dir, os.path.basename(audio_file)).rstrip('.webm')
        
        assert not os.path.isdir(segment_path), f'{segment_path} already exists'

        os.makedirs(segment_path, exist_ok=True)

        times = read_srt_file(srt_file)

        print(f"Processing {audio_file}")
        for s, e in tqdm(times):
            # print(' '.join(['ffmpeg', f'-i "{audio_file}"', f'-ss {s}', f'-to {e}', '-acodec copy', '-vcodec copy', f'-o "{segment_path}/{s} --> {e}.webm"']))
            os.system(' '.join(['ffmpeg', f'-i "{audio_file}"', 
                                f"-ss {s.replace(',', '.')}", f"-to {e.replace(',', '.')}", 
                                '-acodec copy', '-vcodec copy', 
                                f'"{segment_path}/{s} --> {e}.webm"']))

        
        # for i in range(len(times) // simul_output_num + 1):
        #     command = ['ffmpeg', f'-i "{audio_file}"', '-acodec copy', '-vcodec copy']
        #     for s, e in tqdm(times[simul_output_num*i:min(simul_output_num*(i+1), len(times))]):
        #         command.extend([f"-ss {s.replace(',', '.')}", f"-to {e.replace(',', '.')}", f'"{segment_path}/{s} --> {e}.webm"'])
        #     command = ' '.join(command)
        #     os.system(command)


    # return