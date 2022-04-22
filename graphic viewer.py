from tkinter import *
import os

white = '#FFFFFF'
lightgrey = '#AAAAAA'
darkgrey = '#666666'
black = '#000000'

imagename = input('Enter the name of the image in Converted_Graphics: ')

os.system('certutil -encodehex Converted_Graphics/'+imagename+'.bin temp.txt')

file = open('temp.txt','r')
content = file.readlines()
file.close()
middleonly = []
for line in content:
    middleonly.append(line[4:-17])
rawhex = ''
for line in middleonly:
    for char in line:
        if char in ['a','b','c','d','e','f','0','1','2','3','4','5','6','7','8','9']:
            rawhex += char

os.remove('temp.txt')

hextobin = {
    '0' : '0000',
    '1' : '0001',
    '2' : '0010',
    '3' : '0011',
    '4' : '0100',
    '5' : '0101',
    '6' : '0110',
    '7' : '0111',
    '8' : '1000',
    '9' : '1001',
    'a' : '1010',
    'b' : '1011',
    'c' : '1100',
    'd' : '1101',
    'e' : '1110',
    'f' : '1111'
}

binary = ''
for char in rawhex:
    binary += hextobin[char]

window = Tk()
c = Canvas(width = 560, height = 560, bg = white)
c.pack()

lines = []
for i in range(57):
    if i % 8 == 0:
        lines.append(c.create_line(0,i*10,560,i*10, fill=black))
        lines.append(c.create_line(i*10,0,i*10,560, fill=black))
    else:
        lines.append(c.create_line(0,i*10,560,i*10, fill=lightgrey))
        lines.append(c.create_line(i*10,0,i*10,560, fill=lightgrey))

#window.mainloop()
