import os
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


if __name__ == "__main__":

    audio_dir = './raw_audio'
    transcription_dir = './transcripts'
    segment_dir = './audio_segments'
    srt_files = sorted(glob(f'{transcription_dir}/*.srt'))

    for srt_file in srt_files:
        audio_file = srt_file.replace(transcription_dir, audio_dir).rstrip('.srt')

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

    # return