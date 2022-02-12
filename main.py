# This is a sample Python script.
import re
import struct
from tkinter import *
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tkinter import filedialog
from tkinter.filedialog import *
import os


# outputFile = "C:/Users/Stasy/Desktop/output2FLASH.txt"

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Bye, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def selectImages():
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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    window = Tk()
    window.geometry('1100x100')
    window.title("flashFiller")

    lbl0 = Label(window, text="Выбор картинок")
    lbl0.grid(column=0, row=1)


    text0 = Text(width=7, height=1)
    text0.grid(column=2, row=1, sticky=(W))
    # text0.pack()

    btn0 = Button(window, text="Выбрать", command=selectImages)
    btn0.grid(column=1, row=1)

    window.mainloop()
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/