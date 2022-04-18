
import sys

from PyQt5.QtWidgets import QApplication,QDialog, QSizeGrip
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow,  QWidget

qtCreatorFile = "GUI.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

from AudioRecorderFunctions import *
import GlobalVars

def RescanInputsButtonPushed():
    
    import GlobalVars
    import pyaudio as pa
    
    inputdevices = 0
    
    pya = pa.PyAudio()
    info = pya.get_host_api_info_by_index(0)
    DeviceList = info.get('deviceCount')
    
    ui.InputSelectioncomboBox.clear();
    #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
    for i in range (0,DeviceList):
        #print(pya.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels'))
        if pya.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
             print(pya.get_device_info_by_host_api_device_index(0,i).get('name'))
            #if ((pya.get_device_info_by_host_api_device_index(0,i).get('name').find("Te"))!=-1):
             ui.InputSelectioncomboBox.insertItem(20,str(pya.get_device_info_by_host_api_device_index(0,i).get('name')))    
             inputdevices+=1

    
    from pygrabber.dshow_graph import FilterGraph
    ui.VideoSelectionComboBox.disconnect()
    graph = FilterGraph()
    cams=graph.get_input_devices();
    ui.VideoSelectionComboBox.clear();
    for i in cams:
         ui.VideoSelectionComboBox.insertItem(20,str(i))
    GlobalVars.VidSrc=0;

    video = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    video.set(cv2.CAP_PROP_FRAME_WIDTH,GlobalVars.Width)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT,GlobalVars.Height)
    GlobalVars.Width=video.get(cv2.CAP_PROP_FRAME_WIDTH);
    GlobalVars.Height= video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    ResolutionString=str(GlobalVars.Width) + 'x' + str(GlobalVars.Height)    
    video.release();
    ui.VideoSelectionComboBox.currentIndexChanged.connect(VidSelectChanged);
    
def InputSelectioncomboBoxChanged(newvalue):
    import GlobalVars
    import pyaudio
    import pdb
 
    
    GlobalVars.inputdeviceindex=int(newvalue)    

    p = pyaudio.PyAudio()            
    devinfo = p.get_device_info_by_index(int(newvalue))
    
    GlobalVars.CHANNELS=p.get_device_info_by_host_api_device_index(0,newvalue).get('maxInputChannels')
      
       
    samplerates = 32000, 44100, 48000, 96000, 128000
    ui.SampleRatecomboBox.disconnect()
    ui.SampleRatecomboBox.clear();
    
    for fs in samplerates:
        try:            
            p.is_format_supported(fs,  # Sample rate
                         input_device=devinfo['index'],
                         input_channels=devinfo['maxInputChannels'],
                         input_format=pyaudio.paInt16)
        except Exception as e:
            print(fs, e)
        else:            
            ui.SampleRatecomboBox.insertItem(20,str(fs))            
    
    
    ui.SampleRatecomboBox.setCurrentText(str(GlobalVars.SampleRate))    
    ui.SampleRatecomboBox.currentIndexChanged.connect(updateSampleRate);
    GlobalVars.SampleRate=int(ui.SampleRatecomboBox.currentText())
    GlobalVars.CHANNELS=devinfo['maxInputChannels']
    
    
    p.terminate

    
    
  
def StopPushButton():   
    import GlobalVars
    GlobalVars.isRunning=0
    
    ui.StartPushButton.setEnabled(True)
    ui.RescanInputsPushButton.setEnabled(True)
    ui.ThresholdLineEdit.setEnabled(True)
    ui.BirdNameLineEdit.setEnabled(True)   
    ui.InputSelectioncomboBox.setEnabled(True)
    ui.WorkingDirpushButton.setEnabled(True)
    ui.BufferTimeSpinBox.setEnabled(True)    
    ui.ListeningTextBox.setText('')

def loadConfig_ButtonPressed():
    import os
    import GlobalVars       
            
    loadfilename = (QtWidgets.QFileDialog.getOpenFileName(ui,'Open Config File', GlobalVars.path,'*.TAFcfg'))  
    GlobalVars.loadConfig(loadfilename[0],ui) 

def updateSampleRate():
    import GlobalVars
    GlobalVars.SampleRate=int(ui.SampleRatecomboBox.currentText())
      

def saveConfig_ButtonPressed():
    import GlobalVars
  
    savefilename = (QtWidgets.QFileDialog.getSaveFileName(ui,'Open Config File', GlobalVars.path,'*.TAFcfg','*.TAFcfg'))  
    GlobalVars.saveConfig(savefilename[0],ui)

def StartPushButton():

    import GlobalVars
    
    ui.StartPushButton.setEnabled(False)
    ui.RescanInputsPushButton.setEnabled(False)
    ui.ThresholdLineEdit.setEnabled(False)
    ui.BirdNameLineEdit.setEnabled(False)
    ui.InputSelectioncomboBox.setEnabled(False)
    ui.WorkingDirpushButton.setEnabled(False)
    ui.BufferTimeSpinBox.setEnabled(False)    
    GlobalVars.isRunning=1
    

    TriggeredRecordAudio(ui)
    
def inputDeviceComboBoxChanged(newvalue):
    import GlobalVars

    GlobalVars.VidSrc=ui.VideoSelectionComboBox.currentIndex();

def ThresholdLineEditChanged(newvalue):
    import GlobalVars
    GlobalVars.threshold=int(newvalue)
    
def BufferTimeSpinBoxChanged(newvalue):
    import GlobalVars
    GlobalVars.buffertime=int(newvalue)

def BirdNameLineEditChanged(newvalue):
    import GlobalVars
    GlobalVars.filename=str(newvalue)

    
def ResSelectChanged():
    import GlobalVars
    import pdb
    
    GlobalVars.VidSrc=ui.VideoSelectionComboBox.currentIndex();
    video = cv2.VideoCapture(GlobalVars.VidSrc)

    ResTxt=ui.ResolutionComboBox.currentText()
    ResTxt=ResTxt.split('x')
    
    GlobalVars.Width=int(ResTxt[0]);
    GlobalVars.Height=int(ResTxt[1]);

    video.set(cv2.CAP_PROP_FRAME_WIDTH,GlobalVars.Width)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT,GlobalVars.Height)
    
    GlobalVars.Width=int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    GlobalVars.Height=int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    ResTxt=str(GlobalVars.Width)+'x'+str(GlobalVars.Height);
    ui.ResolutionComboBox.setCurrentText(ResTxt)    

def VidSelectChanged():
    import GlobalVars
    import pdb
    
    GlobalVars.VidSrc=ui.VideoSelectionComboBox.currentIndex();
    video = cv2.VideoCapture(GlobalVars.VidSrc)


    
    
def WorkingDirpushButtonClicked():
    import os
    import GlobalVars
    
    dialog = QtWidgets.QFileDialog()
    dialog.setFileMode(QtWidgets.QFileDialog.Directory)
    dialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)    
    directory = QtWidgets.QFileDialog.getExistingDirectory(dialog, 'Select Drive')
    directory = str(directory)    
    GlobalVars.path=directory+'/'
    

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        from numpy import arange, array, zeros
        import GlobalVars;
        
        GlobalVars.buffertime=1
        GlobalVars.threshold=500
        GlobalVars.filename='birdname'
        GlobalVars.path='.';
        GlobalVars.inputdeviceindex=0
        GlobalVars.CHANNELS=1;
        GlobalVars.isRunning=False;
        GlobalVars.SampleRate=44100
        GlobalVars.Width=640;
        GlobalVars.Height=480;
        self.actionLoad.triggered.connect(loadConfig_ButtonPressed);
        self.actionSave.triggered.connect(saveConfig_ButtonPressed);                


        self.ThresholdLineEdit.setText(str(GlobalVars.threshold))
        self.RescanInputsPushButton.clicked.connect(RescanInputsButtonPushed)
        self.StopPushButton.clicked.connect(StopPushButton)
        self.StartPushButton.clicked.connect(StartPushButton)
        self.ThresholdLineEdit.textChanged.connect(ThresholdLineEditChanged)
        self.BirdNameLineEdit.textChanged.connect(BirdNameLineEditChanged)                                               
        self.BufferTimeSpinBox.valueChanged.connect(BufferTimeSpinBoxChanged) 
        self.InputSelectioncomboBox.currentIndexChanged.connect(InputSelectioncomboBoxChanged)        
        self.WorkingDirpushButton.clicked.connect(WorkingDirpushButtonClicked)
        self.ResolutionComboBox.currentIndexChanged.connect(ResSelectChanged);
        self.VideoSelectionComboBox.currentIndexChanged.connect(VidSelectChanged);

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    RescanInputsButtonPushed()
    sys.exit(app.exec_())
    
    window.show()
    sys.exit(app.exec_())


