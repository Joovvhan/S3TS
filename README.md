# S3TS
Speech-to-Text-to-Speech

# File Format Information
* webm (44.1kHz/40kHz) [x]
* m4a (44.1kHz/32kHz)

## Related Repositories
* [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* [Whisper](https://github.com/openai/whisper)
* [UVR](https://github.com/Anjok07/ultimatevocalremovergui)
* [Spleeter](https://github.com/deezer/spleeter)

## Known Issues
* Whisper somtimes fails in cutting off silences

* Good example
![](https://github.com/Joovvhan/S3TS/blob/main/png/good.png)

* Bad example
![](https://github.com/Joovvhan/S3TS/blob/main/png/bad.png)

* 4 criteria limits (Jamos=X, Seconds=Y)
![](https://github.com/Joovvhan/S3TS/blob/main/png/quad_limits.png)



## TO-DO
* Split audio files into segments according to Whisper output convention [x]
* Filter out inappropriate samples with simple rules
* Store enough samples and visualize statistics 
  
* Search SOTA level TTS repositories
* Implement Korean token handling system
* Add training results with graphs and audio samples
* Test and pick the most appropriate source-seperation algorithm
* Test and pick the most appropriate vocoder algorithm