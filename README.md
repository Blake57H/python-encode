# python-encode

 Me trying to build a ffmpeg GUI based on SSA's (Small Sized Animations) code. I'm not experienced in Python coding (very likely to make a lot of stupid mistakes) and I'm doing it for fun.

 My goal is to make something that can automatically scan new files in a specified directory, then encode them.

 While SSA use MP4 as catainer and aac as audio codec, I'll go MKV and libopus since I only watch on PC and device compatibiliy (like Android TV or something) isn't my concern. Also I prefer subtitles that can be enabled or disabled (softsubs, is that the word?). On MP4 subtitle is burned into video.

 It will start with system. I'll probablly use Task Scheduler on Windows.

 Should I made the GUI based on SSA's profile or more general purpose?

 Currently I'm making it using python 3.10 on Windows 10. When this is finished I may port it to Python 3.8, because:

- It supports Windows 7
- Ubuntu 20.04 comes with Python 3.8 (though I have Zorin installed on my home desktop and Ubuntu 21.10 on Raspbery Pi 4)

In short, it's more popular and widerly used (I guess?)
