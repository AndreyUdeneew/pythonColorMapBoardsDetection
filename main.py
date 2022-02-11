# This is a sample Python script.
import re
import struct
from tkinter import *
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tkinter import filedialog
from tkinter.filedialog import *
import os
# import scipy
# import wave
# from scipy.io import wavfile
import numpy as np
# import soundfile as sf
# from scipy.io.wavfile import read

# outputFile = "C:/Users/Stasy/Desktop/output2FLASH.txt"
fullscreen_width = 128
fullscreen_height = 128
fullscreen_length = fullscreen_width*fullscreen_height/2
MAX_N_of_Fullscreens = 256
MAX_N_of_SmallImages = 256
print('fullscreenlength = '+str(fullscreen_length))

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Bye, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def selectOutputDir():
    OutputDir = filedialog.askdirectory(parent=window)
    outputFile = OutputDir+'/output2FLASH.bin'
    text3.insert(INSERT, outputFile)


def selectFullScreens():
    outputFile = format(text3.get("1.0", 'end-1c'))
    fileNames = askopenfilenames(parent=window)
    fileNames = sorted(fileNames)
    fOut = open(outputFile, 'wb')
    for fileName in fileNames:
        with open(fileName, mode='rb') as f:
            header = [header_byte for header_byte in f.read(118)]
            f.seek(118)
            data_bytes = [255-byte for byte in f.read()]
            fOut.write(bytes(data_bytes))
        print(fileName)

    add = '0xff'
    add = int(add, base=16)
    for i in range((MAX_N_of_Fullscreens-len(fileNames))*int(fullscreen_length)):
        fOut.write(int.to_bytes(add, 1, byteorder='big'))
    fOut.close()
    text0.insert(INSERT, 'Готово')


def selectSmallImages():
    outputFile = format(text3.get("1.0", 'end-1c'))
    fileNamesSmall = askopenfilenames(parent=window)
    fileNamesSmall = sorted(fileNamesSmall)
    print(len(fileNamesSmall))
    for fileNameSmall in fileNamesSmall:
        print(fileNameSmall)
        print('small image')
        with open(fileNameSmall, mode='rb') as f:
            header = [header_byte for header_byte in f.read(118)]
            f.seek(118)
            data_bytes = [255-byte for byte in f.read()]
            print('len of rastr = '+str(len(data_bytes)))
            width = header[18]
            print('width = ' + str(width))
            height = header[22]
            if (height % 2) != 0:
                height += 1
            print('height = ' + str(height))
        print(height * width / 2)
        length = height * width / 2
        # print(length)
        length += 2

#################################################################################
        f = open(fileNameSmall)          #   width and height became known
        fOut = open(outputFile, 'ab')
        fOut.write(int.to_bytes(height, 1, byteorder='big'))
        fOut.write(int.to_bytes(width, 1, byteorder='big'))
        fOut.write(bytes(data_bytes))
        nAdds = 0
        if len(data_bytes) < (int(fullscreen_length)):
            complement = '0xff'
            complement = int(complement, base=16)
            nOfComplements = int(fullscreen_length - 2 - len(data_bytes))
            print('nOfComplements = ' + str(nOfComplements))
            for i in range(nOfComplements):
                fOut.write(int.to_bytes(complement, 1, byteorder='big'))
                nAdds = i
            adds = '0xff'
            adds = int(adds, base=16)
            print('number of complements = ' + str(nAdds))
            print('len of image rastr = ' + str(len(data_bytes)))
            print('len of image with a complement = '+str(nOfComplements+len(data_bytes)+2))
            ######################################    Adds to 256*8192 ################################
    for i in range((MAX_N_of_SmallImages-len(fileNamesSmall))*int(fullscreen_length)):
        fOut.write(int.to_bytes(adds, 1, byteorder='big'))
    fOut.close()
    text1.insert(INSERT,'Готово')

def selectSounds():
    outputFile = format(text3.get("1.0", 'end-1c'))
    types = {
        1: np.int8,
        2: np.int16,
        4: np.int32
    }
    fileNames = askopenfilenames(parent=window)
    fileNames = sorted(fileNames)
    fOut = open(outputFile, 'a')
#################Adding adds after images before sounds##########################################
    adds = '0xff'
    adds = int(adds, base=16)
    for n in range(262144*64):
        fOut.write(int.to_bytes(adds, 1, byteorder='big'))
    # for n in range(1, 262144 + 1, 1):
    #     adds = ('ff,' * 64) + '\n'
    #     adds = re.sub(r'\]', '', adds)
    #     adds = re.sub(r'\[', '', adds)
    #     # adds = re.sub(r'0x', '', adds)
    #     adds = re.sub(r'\'', '', adds)
    #     adds = re.sub(r'\ ', '', adds)
    #     # print(adds)
    #     fOut.writelines(adds)

    soundNum = -1
    prevAddr = 0x01400900
    prevAddr = 20973824

    for fileName in fileNames:
        frames=''
        wav = wave.open(fileName, mode="r")
        (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
        print(fileName)
###############################################  soundNum obtaining ###############################
        soundNum = soundNum + 1
        soundNumHex = hex(soundNum)
        print('soundNum='+str(soundNumHex))
        soundNumHex = int(soundNumHex, base=16)
        soundNumHex = format(int(soundNumHex), 'x')
        print('soundNum='+str(soundNumHex))
################################################ length of sounв obtaining ########################
        nframes_3 = hex((nframes >> 24) & 0xFF)
        nframes_2 = hex((nframes >> 16) & 0xFF)
        nframes_1 = hex((nframes >> 8) & 0xFF)
        nframes_0 = hex((nframes >> 0) & 0xFF)
        nframes_3 = int(nframes_3, base=16)
        nframes_2 = int(nframes_2, base=16)
        nframes_1 = int(nframes_1, base=16)
        nframes_0 = int(nframes_0, base=16)
        nframes_3 = format(nframes_3, "x")
        nframes_2 = format(nframes_2, "x")
        nframes_1 = format(nframes_1, "x")
        nframes_0 = format(nframes_0, "x")
        print('nframes_3=' + str(nframes_3))
        print('nframes_2=' + str(nframes_2))
        print('nframes_1=' + str(nframes_1))
        print('nframes_0=' + str(nframes_0))
        print('nframes=' + str(nframes))
        # print('compname=' + str(compname))
        # print('comptype=' + str(comptype))
        # print('N channels=' + str(nchannels))
        # print('sample width='+str(sampwidth))
        # print('framerate='+str(framerate))
##################################################### current address obtaining #####################
        currAddr = prevAddr                         # bubble
        currAddr_3 = hex((currAddr >> 24) & 0xFF)
        currAddr_2 = hex((currAddr >> 16) & 0xFF)
        currAddr_1 = hex((currAddr >> 8) & 0xFF)
        currAddr_0 = hex((currAddr >> 0) & 0xFF)
        currAddr_3 = int(currAddr_3, base=16)
        currAddr_2 = int(currAddr_2, base=16)
        currAddr_1 = int(currAddr_1, base=16)
        currAddr_0 = int(currAddr_0, base=16)
        currAddr_3 = format(currAddr_3, "x")
        currAddr_2 = format(currAddr_2, "x")
        currAddr_1 = format(currAddr_1, "x")
        currAddr_0 = format(currAddr_0, "x")
        print('currAddr_3=' + str(currAddr_3))
        print('currAddr_2=' + str(currAddr_2))
        print('currAddr_1=' + str(currAddr_1))
        print('currAddr_0=' + str(currAddr_0))
        print('currAddr=' + str(currAddr))
        prevAddr = currAddr + nframes               # bubble
##################################################### write info to infoPage ########################
        fOut.writelines(str(soundNumHex)+','+str(currAddr_3)+','+str(currAddr_2)+','+str(currAddr_1)+','
                        +str(currAddr_0)+','+str(nframes_3)+','+str(nframes_2)+','+str(nframes_1)+','
                        +str(nframes_0)+',')
        fOut.writelines('\n')
##################################################### write adds after soundInfo to output file #####
    if len(fileNames)<256:
        nSoundComplements = (256 - len(fileNames)) * 9
        soundComplement = ('ff,' + '\n' )
        for i in range(1, nSoundComplements+1, 1):
            fOut.writelines(soundComplement)
##################################################### write content to output file ##################
    for fileName_ in fileNames:
        print(fileName_)
        frames = ''
        wav = wave.open(fileName_, mode="r")
        (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
        content = wav.readframes(nframes)
        content = str(content)
        content = re.findall(r'[x]\w+', str(content))
        content = str(content)
        content = re.sub(r'\]', '', content)
        content = re.sub(r'\[', '', content)
        content = re.sub(r'x', '', content)
        content = re.sub(r'\'', '', content)
        content = re.sub(r'\ ', '', content)
        # print(content)
        fOut.writelines(content + ',')
        fOut.writelines('\n')
        wav.close()
    fOut.close()
    text2.insert(INSERT, 'Готово')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    window = Tk()
    window.geometry('1100x100')
    window.title("flashFiller")

    lbl0 = Label(window, text="Выбор полноэкранных картинок")
    lbl0.grid(column=0, row=1)
    lbl1 = Label(window, text="Выбор маленьких картинок")
    lbl1.grid(column=0, row=2)
    lbl2 = Label(window, text="Выбор звуков")
    lbl2.grid(column=0, row=3)
    lbl3 = Label(window, text="Выбор директории выходного файла")
    lbl3.grid(column=0, row=0)

    text0 = Text(width=7, height=1)
    text0.grid(column=2, row=1, sticky=(W))
    # text0.pack()
    text1 = Text(width=7, height=1)
    text1.grid(column=2, row=2, sticky=(W))
    # text1.pack()
    text2 = Text(width=7, height=1)
    text2.grid(column=2, row=3, sticky=(W))
    # text2.pack()
    text3 = Text(width=100, height=1)
    text3.grid(column=2, row=0)

    btn0 = Button(window, text="Выбрать", command=selectFullScreens)
    btn0.grid(column=1, row=1)
    btn1 = Button(window, text="Выбрать", command=selectSmallImages)
    btn1.grid(column=1, row=2)
    btn2 = Button(window, text="Выбрать", command=selectSounds)
    btn2.grid(column=1, row=3)
    btn3 = Button(window, text="Выбрать", command=selectOutputDir)
    btn3.grid(column=1, row=0)

    window.mainloop()
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/