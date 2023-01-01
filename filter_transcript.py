import os
from glob import glob

import numpy as np

from datetime import datetime

from tqdm.auto import tqdm

import jamotools

def read_srt_file(file):

    with open(file, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    index = lines[0::4]
    times = lines[1::4]
    texts = lines[2::4]

    times = [time_str.split(' --> ') for time_str in times]

    return index, texts, times

def rewrite_srt_file(src_file, filtered_file, filtered):

    with open(src_file, 'r') as f:
        lines = [line for line in f.readlines()]

    with open(filtered_file, 'w') as f:
        i = 0
        for b in filtered:
            if b:
                for j in range(4):
                    f.write(lines[i]) 
                    i += 1
            else:
                i += 4
    
    assert i == len(lines), f'Rewriting srt file went wrong {filtered_file}'

    return

def time_string_to_datetime(time_string):

    return datetime.strptime(time_string, '%H:%M:%S,%f')

def get_delta_float(s, e):

    delta_time = time_string_to_datetime(e) - time_string_to_datetime(s)
    delta_float = delta_time.seconds + delta_time.microseconds / 10 ** 6
    delta_float = np.round(delta_float, 2)

    return delta_float

def length_filtered(dur, jamo):

    jamo_high = 138.7 
    dur_high = 11.8347000 
    r_high = 20.91667
    # r_low = 2.867143
    r_low = 7.085238

    dur_pass = dur < dur_high and dur > 0 
    jamo_pass = jamo < jamo_high and jamo > 0
    r = jamo / dur
    r_pass = r < r_high and r > r_low

    return  dur_pass and jamo_pass and r_pass

if __name__ == "__main__":

    audio_dir = './raw_audio'
    transcription_dir = './transcripts'
    filtered_transcription_dir = './filtered_transcripts'
    segment_dir = './audio_segments'
    srt_files = sorted(glob(f'{transcription_dir}/*.srt'))

    total_durations = list()
    total_jamos = list()

    for srt_file in tqdm(srt_files):

        filtered_srt_file = srt_file.replace(transcription_dir, filtered_transcription_dir)

        index, texts, times = read_srt_file(srt_file)
        
        durations = [get_delta_float(s, e) for s, e in times]
        jamos = [len(jamotools.split_syllables(text)) for text in texts]

        filterd_booleans = [length_filtered(dur, jamo) for (dur, jamo) in zip(durations, jamos)]

        rewrite_srt_file(srt_file, filtered_srt_file, filterd_booleans)
