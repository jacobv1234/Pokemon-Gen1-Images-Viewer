from tkinter import *
from time import sleep
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

binarydata = ''
for char in rawhex:
    binarydata += hextobin[char]

window = Tk()
c = Canvas(width = 560, height = 560, bg = white)
c.pack()


def bin_to_int(binary):
    total = 0
    worth = 1
    for i in range(len(binary),0,-1):
        total += worth * int(binary[i-1])
        worth *= 2
    return total

datapointer = 0 #this shows the index of the next bit

def get_next_bits(amount_returned):
    global datapointer, binarydata
    returned_bits = ''
    for i in range(amount_returned):
        returned_bits += binarydata[datapointer]
        datapointer += 1
    return returned_bits


width = bin_to_int(get_next_bits(4))
height = bin_to_int(get_next_bits(4))
firstbp = int(get_next_bits(1))
currentpacket = int(get_next_bits(1))

x = 0
y = 0

#add whitespace
v_offset = 7 - height
c.create_rectangle(0,0,1120,80*v_offset,fill=white)
h_offset_left = 4 - ((width + 1)//2)
h_offset_right = 3 - (width//2)
c.create_rectangle(0,0,80*h_offset_left,560,fill='white')
c.create_rectangle(560,0,560+(80*h_offset_left),560,fill='white')
c.create_rectangle(560,0,560-(80*h_offset_right),560,fill='white')
c.create_rectangle(1120,0,1120-(80*h_offset_right),560,fill='white')

x += 8*h_offset_left
y += 8*v_offset

if firstbp == 1:
    x += 0
else:
    x += 56


while True:
    if currentpacket == 0:
        firstnumber = ''
        while True:
            firstnumber += get_next_bits(1)
            if firstnumber[-1] == '0':
                break
        secondnumber = bin_to_int(get_next_bits(len(firstnumber)))
        firstnumber = bin_to_int(firstnumber)
        zeropairs = firstnumber + secondnumber + 1

