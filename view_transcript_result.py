import os
from glob import glob

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.patches import Polygon

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

    total_durations = list()
    total_jamos = list()

    for srt_file in tqdm(srt_files):
        index, texts, times = read_srt_file(srt_file)
        
        durations = [get_delta_float(s, e) for s, e in times]
        jamos = [len(jamotools.split_syllables(text)) for text in texts]

        filtered = [(dur, jamo) for (dur, jamo) in zip(durations, jamos) if dur < 80000 and dur > 0]
        durations = [dur for (dur, jamo) in filtered]
        jamos = [jamo for (dur, jamo) in filtered]

        total_durations.extend(durations)
        total_jamos.extend(jamos)

    print(f'Total valid files: {len(total_durations)}')
    print(f'Total valid seconds: {sum(total_durations)}')
    print(f'Total valid jamos: {sum(total_jamos)}')

    # Total valid files: 77369
    # Total valid seconds: 456998.5200000008
    # Total valid jamos: 2933095

    total_r = [jamo / dur for (jamo, dur) in zip(total_jamos, total_durations)]

    # fig, axes = plt.subplots(2, 1, sharex=True, figsize=(12, 6))
    # axes[0].hist(total_r, bins=100, rwidth=0.9)
    # axes[1].hist(total_r, bins=100, rwidth=0.9)
    # axes[1].set_yscale("log")
    # plt.show()

    upper_percentage = 0.99
    lower_percentage = 0.15

    total_r = [r for r in total_r if r < 30]
    fig, axes = plt.subplots(2, 1, sharex=True, figsize=(12, 6))
    axes[0].hist(total_r, bins=300, rwidth=0.9)
    n, bins, patches = axes[1].hist(total_r, bins=300, rwidth=0.9, cumulative=True, density=True)
    axes[1].axhline(upper_percentage, color='r')
    axes[1].axhline(lower_percentage, color='r')
    
    for i in range(len(n) - 1):
        if n[i+1] >= lower_percentage and n[i] < lower_percentage:
            # print(n[i+1], bins[i+1], n[i], bins[i])
            r_low = np.mean([bins[i+1], bins[i]])
        if n[i+1] >= upper_percentage and n[i] < upper_percentage:
            # print(n[i+1], bins[i+1], n[i], bins[i])
            r_high = np.mean([bins[i+1], bins[i]])
    
    plt.show()

    fig = plt.figure(figsize=(9, 9))
    gs = fig.add_gridspec(2, 2,  width_ratios=(4, 1), height_ratios=(1, 4),
                        left=0.15, right=0.90, bottom=0.10, top=0.90,
                        wspace=0.05, hspace=0.05)

    ax = fig.add_subplot(gs[1, 0])
    ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
    ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)

    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    # the scatter plot:
    ax.scatter(total_jamos, total_durations, alpha=0.05, s=4)
    x_max, y_max = max(total_jamos), max(total_durations)
    ax.plot([0, x_max], [0, x_max / r_high], color='r')
    ax.plot([0, y_max * r_low], [0, y_max], color='r')
    ax.plot([np.median(total_jamos)], [np.median(total_durations)], color='r', marker='*')

    # deg = np.rad2deg(np.arctan2(np.median(total_durations), np.median(total_jamos)))
    # print(np.median(total_jamos), np.median(total_durations), deg)

    # ells = Ellipse((np.median(total_jamos), np.median(total_durations)), 60, 10, deg * 0.75, color='r', alpha=0.2)
    # ax.add_artist(ells)
    # ax.set_xlim((0, max(jamos)))
    # ax.set_ylim((0, max(jamos)))

    upper_percentage = 0.99

    # ax_histx.hist(total_jamos, bins=100, rwidth=0.8)
    n, bins, patches = ax_histx.hist(total_jamos, bins=100, rwidth=0.8, cumulative=True, density=True)
    ax_histx.axhline(upper_percentage, color='r')
    
    for i in range(len(n) - 1):
        if n[i+1] >= upper_percentage and n[i] < upper_percentage:
            # print(n[i+1], bins[i+1], n[i], bins[i])
            jamo_high = np.mean([bins[i+1], bins[i]])
    
    ax.axvline(jamo_high, color='r')

    upper_percentage = 0.90

    # ax_histy.hist(total_durations, bins=100, rwidth=0.8, orientation='horizontal')
    n, bins, patches = ax_histy.hist(total_durations, bins=100, rwidth=0.8, orientation='horizontal', cumulative=True, density=True)
    ax_histy.axvline(upper_percentage, color='r')

    for i in range(len(n) - 1):
        if n[i+1] >= upper_percentage and n[i] < upper_percentage:
            # print(n[i+1], bins[i+1], n[i], bins[i])
            dur_high = np.mean([bins[i+1], bins[i]])
    
    ax.axhline(dur_high, color='r')    

    ax.set_xlim([0, max(total_jamos)])
    ax.set_ylim([0, max(total_durations)])

    p = Polygon([[0,0], [jamo_high, jamo_high/r_high], [jamo_high, dur_high], [dur_high*r_low, dur_high]], facecolor='r', alpha=0.2)
    ax.add_patch(p)

    plt.show()
        

    print(f'{jamo_high} / {dur_high} / {r_high} / {r_low}')
    # 138.7000000000000 / 11.8347000 / 20.91667 / 2.867143

    total_durations = list()
    total_jamos = list()

    def length_filtered(dur, jamo):

        dur_pass = dur < dur_high and dur > 0 
        jamo_pass = jamo < jamo_high and jamo > 0
        r = jamo / dur
        r_pass = r < r_high and r > r_low

        return  dur_pass and jamo_pass and r_pass

    for srt_file in tqdm(srt_files):
        index, texts, times = read_srt_file(srt_file)
        
        durations = [get_delta_float(s, e) for s, e in times]
        jamos = [len(jamotools.split_syllables(text)) for text in texts]

        filtered = [(dur, jamo) for (dur, jamo) in zip(durations, jamos) if length_filtered(dur, jamo)]
        durations = [dur for (dur, jamo) in filtered]
        jamos = [jamo for (dur, jamo) in filtered]

        total_durations.extend(durations)
        total_jamos.extend(jamos)

    print(f'Total filtered files: {len(total_durations)}')
    print(f'Total filtered seconds: {sum(total_durations)}')
    print(f'Total filtered jamos: {sum(total_jamos)}')

    # Total filtered files: 60726
    # Total filtered seconds: 263847.75999999954
    # Total filtered jamos: 2285993