from tkinter import *
from time import sleep
import os

white = '#FFFFFF'
lightgrey = '#999999'
darkgrey = '#444444'
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
c = Canvas(width = 1120, height = 560, bg = white)
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

x = 0
y = 0

#add whitespace
v_offset = 7 - height
c.create_rectangle(0,0,1120,80*v_offset,fill=white, outline = white)
h_offset_left = 4 - ((width + 1)//2)
h_offset_right = 3 - (width//2)
c.create_rectangle(0,0,80*h_offset_left,560,fill=white, outline = white)
c.create_rectangle(560,0,560+(80*h_offset_left),560,fill=white, outline = white)
c.create_rectangle(560,0,560-(80*h_offset_right),560,fill=white, outline = white)
c.create_rectangle(1120,0,1120-(80*h_offset_right),560,fill=white, outline = white)
window.update()

x += 8*h_offset_left
y += 8*v_offset

if firstbp == 1:
    x += 0
else:
    x += 56

#create 2d array, 112 x 56 - x and y are pointers to the array
grid = []
for i in range(112):
    column = []
    for j in range(56):
        column.append(0)
    grid.append(column)



def decodebitplane():
    global x, y, grid
    currentpacket = bin_to_int(get_next_bits(1))
    pixelsdrawn = 0
    while True:
        if pixelsdrawn >= (8*width)*(8*height):
            print('Decoded bitplane - raw data last')
            break

        if currentpacket == 0:
            firstnumber = ''
            while True:
                firstnumber += get_next_bits(1)
                if firstnumber[-1] == '0':
                    break

            secondnumber = bin_to_int(get_next_bits(len(firstnumber)))
            firstnumber = bin_to_int(firstnumber)
            zeropairs = firstnumber + secondnumber + 1

            for i in range(zeropairs):
                grid[x][y] = 0
                grid[x+1][y] = 0
                c.create_rectangle(x*10,y*10,(x*10)+20,(y*10)+10, fill = white, outline = white)
                y += 1
                if y >= 56:
                    y = 8*v_offset
                    x += 2
                window.update()
                pixelsdrawn += 2

            currentpacket = 1

        if pixelsdrawn >= (8*width)*(8*height):
            print('Decoded bitplane - RLE packet last')
            break

        if currentpacket == 1:
            while True:
                if pixelsdrawn >= (8*width)*(8*height):
                    break
                next2bits = get_next_bits(2)
                if next2bits == '00':
                    break

                else:
                    for i in range(2):
                        if next2bits[i] == '0':
                            c.create_rectangle(x*10,y*10,(x*10)+10,(y*10)+10, fill = white, outline = white)
                            grid[x][y] = 0
                        else:
                            c.create_rectangle(x*10,y*10,(x*10)+10,(y*10)+10, fill = black)
                            grid[x][y] = 1
                        pixelsdrawn += 1
                        x += 1

                    x -= 2
                    y += 1
                    if y >= 56:
                        y = 8*v_offset
                        x += 2
                    window.update()

            currentpacket = 0

decodebitplane()
sleep(1)

encodingmode = get_next_bits(1)
if encodingmode == '1':
    encodingmode += get_next_bits(1)
encodingmode = bin_to_int(encodingmode)
if encodingmode == 0:
    encodingmode = 1

if x >= 84:
    x = 8*h_offset_left
else:
    x = 8*h_offset_left + 56
y = 8*v_offset


decodebitplane()
sleep(1)

def deltadecode(bitplane):
    global grid, x, y
    if bitplane == 1:
        xstart = 0
    else:
        xstart = 56
    y = 0

    for i in range(56):
        x = xstart
        col = False

        for j in range(56):
            flipornot = grid[x][y]
            if flipornot == 1:
                col = not col
            
            if col:
                c.create_rectangle(x*10,y*10,(x*10)+10,(y*10)+10, fill = black)
                grid[x][y] = 1
            else:
                c.create_rectangle(x*10,y*10,(x*10)+10,(y*10)+10, fill = white, outline = white)
                grid[x][y] = 0
            
            x += 1
        y += 1
        window.update()
    print('Bitplane ' + str(bitplane) + ' delta decoded successfully.')
    
def xor(): #no bitplane is needed, only uses 2nd bitplane
    global x, y, grid
    if firstbp == 1:
        start = 56
        end = 112
    else:
        start = 0
        end = 56
    for y in range(56):
        for x in range(start,end):
            if grid[x][y] == grid[x-56][y]:
                c.create_rectangle(x*10,y*10,(x*10)+10,(y*10)+10, fill = white, outline = white)
                grid[x][y] = 0
            else:
                c.create_rectangle(x*10,y*10,(x*10)+10,(y*10)+10, fill = black)
                grid[x][y] = 1
        window.update()
    print('XOR performed successfully.')

if encodingmode == 1:
    deltadecode(0)
    sleep(1)
    deltadecode(1)
    sleep(1)

elif encodingmode == 2:
    deltadecode(firstbp)
    sleep(1)
    xor()
    sleep(1)

else:
    deltadecode(0)
    sleep(1)
    deltadecode(1)
    sleep(1)
    xor()
    sleep(1)

def combine_bitplanes():
    global x, y, grid
    for y in range(56):
        for x in range(56):
            colour = ''
            if grid[x][y] == 0 and grid[x+56][y] == 0:
                colour = white
            elif grid[x][y] == 0 and grid[x+56][y] == 1:
                colour = lightgrey
            elif grid[x][y] == 1 and grid[x+56][y] == 0:
                colour = darkgrey
            else:
                colour = black
            c.create_rectangle(x*10,y*10,(x*10)+10,(y*10)+10, fill = colour, outline = colour)
        window.update()
    print('Complete.')
    c.create_rectangle(560,0,1120,560,fill=white,outline=white)

combine_bitplanes()
window.mainloop()
