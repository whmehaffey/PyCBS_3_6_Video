
global isRunning
global numdevices
global devicenumber
global inputdeviceindex
global filename
global pathname
global threshold
global buffertime
global path
global CHANNELS
global VidSrc
global Resolution
global Height
global Width

def loadConfig(loadfilename,ui):
    from configparser import SafeConfigParser
    import os
    import GlobalVars
    import serial    
    import pdb
   
    parser = SafeConfigParser()
    loadfilename=loadfilename.replace('/','\\')
   
    if not parser.read(str(loadfilename)): #.replace('/','\\')):
        raise(IOError, 'cannot load')
    
  
    GlobalVars.buffertime=int(parser.get('main','GlobalVars.buffertime'))
    GlobalVars.InputSelection=parser.get('main','GlobalVars.InputSelectionText');        
    GlobalVars.path=(parser.get('main','GlobalVars.Ch1DirPath'))    
    GlobalVars.filename=(parser.get('main','GlobalVars.Ch1fileName'))
    GlobalVars.Height=int(parser.get('main','GlobalVars.Height'))
    GlobalVars.Width=int(parser.get('main','GlobalVars.Width'))

    GlobalVars.VidSrc=int(parser.get('main','GlobalVars.VidSrc'))
    GlobalVars.threshold=int(parser.get('main','GlobalVars.threshold'))
    GlobalVars.SampleRate=int(parser.get('main','GlobalVars.SampleRate'))
    
    ui.BirdNameLineEdit.setText(GlobalVars.filename);    
    ui.BufferTimeSpinBox.setValue(GlobalVars.buffertime)
    ui.ThresholdLineEdit.setText(str(GlobalVars.threshold))

    ui.SampleRatecomboBox.setCurrentText(str(GlobalVars.SampleRate)) 
    ui.InputSelectioncomboBox.setCurrentText(GlobalVars.InputSelection)
    ui.VideoSelectionComboBox.setCurrentIndex(GlobalVars.VidSrc)    

    
    ui.SampleRatecomboBox.setCurrentText(str(GlobalVars.SampleRate))
    ResTxt=str(GlobalVars.Width)+'x'+str(GlobalVars.Height);
    ui.ResolutionComboBox.setCurrentText(ResTxt)
    

def saveConfig(savefilename,ui):
    from configparser import SafeConfigParser
    import os
    import GlobalVars
    from numpy import array    

    
    SaveFile= open((savefilename),'w')
    
    parser = SafeConfigParser()
    
    parser.add_section('main')

    
    parser.set('main','GlobalVars.buffertime',str(GlobalVars.buffertime))
    parser.set('main','GlobalVars.Ch1DirPath',str(GlobalVars.path))
    parser.set('main','GlobalVars.Height',str(GlobalVars.Height))
    parser.set('main','GlobalVars.Width',str(GlobalVars.Width))
    parser.set('main','GlobalVars.VidSrc',str(GlobalVars.VidSrc))
    parser.set('main','GlobalVars.SampleRate',str(GlobalVars.SampleRate))
    parser.set('main','GlobalVars.Ch1fileName',str(GlobalVars.filename))
    parser.set('main','GlobalVars.VidSrc',str(GlobalVars.VidSrc))
    
    parser.set('main','GlobalVars.threshold',str(GlobalVars.threshold))
    parser.set('main','GlobalVars.InputSelectionText',ui.InputSelectioncomboBox.currentText()); 
        
    parser.write(SaveFile)    
    SaveFile.close()
