
from PyQt5 import QtGui, QtCore

import pyaudio 
import wave
import audioop
from collections import deque
import os
import time
import math
import GlobalVars
import copy

import pdb;

import acapture
import cv2
import pyqtgraph as pg

global graph_win
from numpy import arange, true_divide



CHUNK = 1024 # CHUNKS of bytes to read each time from mic
FORMAT = pyaudio.paInt16 #this is the standard wav data format (16bit little endian)s
RATE = 44100# sampling frequency
MAX_DUR=60 #max dur in seconds


def RescanInputs():
    import GlobalVars

   
    inputdevices = 0
    
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    
    
    #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
    for i in range (0,numdevices):
        if p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
            print("DevID ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name'))
            inputdevices+=1

    GlobalVars.numdevices=inputdevices
    p.terminate()


def TriggeredRecordAudio(ui):

 import GlobalVars
 global graph_win
 import array
 import pydub;
 import audioop;
 
 MIN_DUR=GlobalVars.buffertime+0.1;#
 threshold=GlobalVars.threshold;
 SILENCE_LIMIT = GlobalVars.buffertime;
 PREV_AUDIO = GlobalVars.buffertime;

 p = pyaudio.PyAudio()
 video = cv2.VideoCapture(GlobalVars.VidSrc) 
 video.set(cv2.CAP_PROP_FPS,60)
 fps=video.get(cv2.CAP_PROP_FPS)
 video.set(cv2.CAP_PROP_FRAME_WIDTH,GlobalVars.Width)
 video.set(cv2.CAP_PROP_FRAME_HEIGHT,GlobalVars.Height)
 
 video.release();

 video = acapture.open(0) 
 GlobalVars.CHANNELS=1;    
 
 stream=p.open(format=FORMAT,input_device_index=GlobalVars.inputdeviceindex,channels=GlobalVars.CHANNELS,rate=RATE,
               input=True,
               frames_per_buffer=CHUNK)
    
 ui.ListeningTextBox.setText('<span style="color:green">quiet</span>')
 audio2send = []
 
 CHANNELS=GlobalVars.CHANNELS;
 last_val_high = [0] * CHANNELS
 last_val_low = [0] * CHANNELS
 last_data = [0] * CHANNELS
 
 rel = int(RATE/CHUNK)
 slid_win = deque(maxlen=SILENCE_LIMIT * rel) #amplitude threshold running buffer
 prev_audio = deque(maxlen=PREV_AUDIO * rel) #prepend audio running buffer
 perm_win = deque(maxlen=PREV_AUDIO*rel)

 imagestartbuffer=deque(maxlen=int(fps*PREV_AUDIO)); 
 imagesaving=deque(maxlen=int(fps*SILENCE_LIMIT));
 permwinimage=deque(maxlen=int(fps*PREV_AUDIO));

 startbuffertimes=deque(maxlen=int(fps*PREV_AUDIO));
 activewintimes=deque(maxlen=int(fps*SILENCE_LIMIT));
 permwintimes=deque(maxlen=int(fps*PREV_AUDIO));


 started = False
 
  

 def updateGraph():
       t=arange(plotarray.buffer_info()[1])
       t=true_divide(t, RATE)
       ui.GraphWidget.plot(t,plotarray, width=1, clear=True)

 timer = pg.QtCore.QTimer()
 timer.timeout.connect(updateGraph)
 timer.start(250)
 
 count=1;

 start = time.time()
 newtime = time.time()
 oldret=0;           
 
 newframe=False;
 time.sleep(0.01); 
 
 while (GlobalVars.isRunning==1):

  ret, frame = video.read()
  time.sleep(0.001); 
  if (ret != oldret):
        lasttime=newtime; 
        newtime = time.time()   
        cv2.imshow("Input", frame)
        newframe=True;
        interval=float(newtime-lasttime);
        currFPS=1/float(interval);        
        ui.FPSLabel.setText('Current FPS:' + str(currFPS));

  oldret=ret;
  
        

  newtime = time.time()
  #alltimes.append(newtime-start);
  
  cur_data = stream.read(CHUNK)
  cv2.namedWindow("Input")
  
  count=count+1
  if (count>20):
      count=0
      QtGui.qApp.processEvents()


  perm_win.append(cur_data)
  data = b''.join(list(perm_win))
  
  if (pyaudio.get_sample_size(FORMAT)==2):
      plotarray = array.array("h",data);  # force 16 bit, since that's the correct #
  else:
      plotarray=  array.array("i",data);  # not 16 bit, so....       
  
  if (newframe):
      permwinimage.append(frame);
      permwintimes.append(newtime-start);
      
  currmax=audioop.max(data,2);
    
  if (currmax > GlobalVars.threshold) and (len(audio2send)<MAX_DUR*rel):      
   if(not started):
    ui.ListeningTextBox.setText('<span style="color:red">singing</span>')
    started = True
   audio2send.append(cur_data)
   if (newframe):
       imagesaving.append(frame);
       activewintimes.append(newtime-start)
  elif (started is True and len(audio2send)>MIN_DUR*rel):
   print("Finished")
  # pdb.set_trace();
   alltimes=list(startbuffertimes)+list(activewintimes);
   filename = save_audio(list(prev_audio) + audio2send,imagestartbuffer,imagesaving,fps,alltimes,GlobalVars.path,GlobalVars.filename)
   started = False
   slid_win = deque(maxlen=SILENCE_LIMIT * rel)   
   prev_audio = copy.copy(perm_win)
   for i in range(0,len(permwintimes)):
       permwintimes[i]=str(float(permwintimes[i])-GlobalVars.buffertime);
   imagestartbuffer=copy.copy(permwinimage)
   startbuffertimes=copy.copy(permwintimes);
   imagesaving=[]
   activewintimes=[]
   start = time.time()
   ui.ListeningTextBox.setText('<span style="color:green">quiet</span>')
   audio2send=[]
  elif (started is True):
   ui.ListeningTextBox.setText('too short')
   started = False
   slid_win = deque(maxlen=SILENCE_LIMIT * rel)
   prev_audio = copy.copy(perm_win)
   imagestartbuffer=copy.copy(permwinimage)   
   startbuffertimes=copy.copy(permwintimes);
   imagesaving=[]
   activewintimes=[]
   start = time.time()
   audio2send=[]
   ui.ListeningTextBox.setText('<span style="color:green">quiet</span>')
  else:
   prev_audio.append(cur_data)
   if (newframe):
       imagestartbuffer.append(frame);
       startbuffertimes.append(newtime-start)
   
 print("done recording")
 stream.close()
 p.terminate()

def save_audio(data, imagebuffer,imagedata,fps, timestamps,rootdir, filename):
 import GlobalVars
 import cv2
 import pdb;
 import pyaudio;
 
 """ Saves mic data to  WAV file. Returns filename of saved
 file """
# filename = GlobalVars.path+'_'+str(int(time.time()))
 # writes data to WAV file
 T=time.localtime()
 outtime=str("%02d"%T[0])+str("%02d"%T[1])+str("%02d"%T[2])+str("%02d"%T[3])+str("%02d"%T[4])+str("%02d"%T[5])
 DatePath='/'+str("%02d"%T[0])+'_'+str("%02d"%T[1])+'_'+str("%02d"%T[2])+'/' 
 filename = rootdir+DatePath+filename+'_'+outtime
 
 if not os.path.exists(os.path.dirname(rootdir+DatePath)):
    try:
        os.makedirs(os.path.dirname(rootdir+DatePath))
    except:
        print('File error- bad directory?')

 data = b''.join(data)
 wf = wave.open(filename + '.wav', 'wb')
 wf.setnchannels(GlobalVars.CHANNELS);
 wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
 wf.setframerate(RATE) 
 wf.writeframes(data)
 wf.close()
 #pdb.set_trace();
 print('saving image');
 print(str(GlobalVars.Frame_Width) + 'x');
 print(GlobalVars.Frame_Height);
 out = cv2.VideoWriter(filename + '.avi',cv2.VideoWriter_fourcc(*'DIVX'), fps,(int(GlobalVars.Width),int(GlobalVars.Height)))
 for i in range (len(imagebuffer)):
     out.write(imagebuffer[i]);
 for i in range (len(imagedata)):
     out.write(imagedata[i]);
 out.release
 
 f = open(filename + 'timestamps.txt','a')
 for i in timestamps:
     reltime=float(i)-float(timestamps[0])
     f.write(str(reltime)+'\n');
 f.close(); 
 return filename + '.wav'
 

##
##if(__name__ == '__main__'):
## audio_int()
## record_song()

