# python-encode

 Me trying to build a ffmpeg GUI based on SSA's (Small Sized Anime) code. I'm not experienced in Python coding and I'm doing it for fun.

 My goal is to make something that can automatically scan new files in a specified directory, then encode them.

 While SSA use MP4 as catainer and aac as audio codec, I'll go MKV and libopus since I only watch on PC and device compatibiliy (like Android TV or something) isn't an issue. Also I prefer subtitles that can be enabled or disabled. On MP4 subtitle is burned into video.

 It will start with system. I'll probablly use Task Scheduler on Windows or init.d on Linux (I have only used Ubuntu/Debian)

By the way, I'm using Python 3.10 and backward compatibility isn't my priority. It will probablly work on Python 3.9 with "from future import __annotation__" but not any version prior than that.
