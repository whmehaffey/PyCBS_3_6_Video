# PyCBS - USB Camera version

Triggered Song Recording w/ video- buffered for pre/post song/video acquisiton. 

Tested w/ Pyton 3.6-10 (PyAudio Supports up to 3.10 for ALSA version). 

install requirements:

python -m pip install pyserial 
python -m pip install numpy 
python -m pip install pyqtgraph
python -m pip install scipy
python -m pip install pydub
python -m pip install acapture
python -m pip install pygrabber
python -m pip install pyqt5
python -m pip install opencv-python
python -m pip install acapture
python -m pip install pygrabber

sometimes numpy has to be downgraded to an earlier version. 

You will also need:

FFMPEG (https://ffmpeg.org/) installed

and:

https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
Only the above version of PyAudio will super high channel counts. 

get correct version (e.g. for Python 3.6 and for your system)
pip install filename.whl 

bitdepth is 16 (Make sure your hardware matches, some FocusRites default to 24), and
you can select the freqnency (but has to match what you set the hardware to, this doesn’t change the hardware to this sampling frequency). 
