import os
from glob import glob

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

from datetime import datetime

import jamotools

def read_srt_file(file):

    with open(file, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    index = lines[0::4]
    times = lines[1::4]
    texts = lines[2::4]

    times = [time_str.split(' --> ') for time_str in times]

    return index, texts, times

def time_string_to_datetime(time_string):
    return datetime.strptime(time_string, '%H:%M:%S,%f')

def get_delta_float(s, e):
    delta_time = time_string_to_datetime(e) - time_string_to_datetime(s)
    delta_float = delta_time.seconds + delta_time.microseconds / 10 ** 6
    delta_float = np.round(delta_float, 2)
    return delta_float

if __name__ == "__main__":

    audio_dir = './raw_audio'
    transcription_dir = './transcripts'
    segment_dir = './audio_segments'
    srt_files = sorted(glob(f'{transcription_dir}/*.srt'))

    for srt_file in srt_files:
        index, texts, times = read_srt_file(srt_file)
        
        durations = [get_delta_float(s, e) for s, e in times]
        jamos = [len(jamotools.split_syllables(text)) for text in texts]

        # plt.figure()
        # plt.hist(durations, bins=range(0, int(max(durations))), width=0.8)
        # plt.show()
        
        # plt.figure()
        # plt.scatter(jamos, durations, alpha=0.2)
        # plt.show()

        fig = plt.figure(figsize=(6, 6))
        gs = fig.add_gridspec(2, 2,  width_ratios=(4, 1), height_ratios=(1, 4),
                            left=0.15, right=0.90, bottom=0.10, top=0.90,
                            wspace=0.05, hspace=0.05)

        ax = fig.add_subplot(gs[1, 0])
        ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
        ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)

        ax_histx.tick_params(axis="x", labelbottom=False)
        ax_histy.tick_params(axis="y", labelleft=False)

        # the scatter plot:
        ax.scatter(jamos, durations, alpha=0.3)
        ax.plot([np.median(jamos)], [np.median(durations)], color='r', marker='*')

        deg = np.rad2deg(np.arctan2(np.median(durations), np.median(jamos)))
        print(np.median(jamos), np.median(durations), deg)

        ells = Ellipse((np.median(jamos), np.median(durations)), 60, 10, deg * 0.75, color='r', alpha=0.2)
        ax.add_artist(ells)
        # ax.set_xlim((0, max(jamos)))
        # ax.set_ylim((0, max(jamos)))

        ax_histx.hist(jamos, bins=30, rwidth=0.9)
        ax_histy.hist(durations, bins=30, rwidth=0.9, orientation='horizontal')

        plt.show()
        

    # return