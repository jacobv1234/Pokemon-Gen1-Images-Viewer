from tkinter import *
from time import sleep
import os
import random

imagename = input('''Enter the name of the image in Converted_Graphics:
>>> ''')

rng = False
if imagename.startswith('rng-'):
    imagename = imagename.strip('rng-')
    rng = True

#colours
while True:
    colsystem = int(input('''Enter a colour scheme:
1 - Game Boy Grellow
2 - Game Boy Pocket Greyscale
3 - GBC Green
4 - GBC Red
5 - GBC Cyan
6 - GBC Yellow
7 - GBC Brown
8 - GBC Grey
9 - GBC Purple
10 - GBC Blue
11 - GBC Pink
12 - GBC Mew
13 - GBC Evolution
14 - Virtual Boy Red
15 - Virtual Boy Red - Inverted
16 - Custom
>>> '''))
    if colsystem <= 0 or colsystem > 16:
        print('Enter a valid colour palette.')
        continue
    elif colsystem == 1:
        white = '#e0f8d0'
        lightgrey = '#88c070'
        darkgrey = '#346856'
        black = '#081820'
    elif colsystem == 2:
        white = '#ffffff'
        lightgrey = '#a9a9a9'
        darkgrey = '#545454'
        black = '#000000'
    elif colsystem == 3:
        white = '#f8e8f8'
        lightgrey = '#a0d080'
        darkgrey = '#48a058'
        black = '#181010'
    elif colsystem == 4:
        white = '#f8e8f8'
        lightgrey = '#f8a050'
        darkgrey = '#d05030'
        black = '#181010'
    elif colsystem == 5:
        white = '#f8e8f8'
        lightgrey = '#a8c8e8'
        darkgrey = '#7098c8'
        black = '#181010'
    elif colsystem == 6:
        white = '#f8e8f8'
        lightgrey = '#f8e070'
        darkgrey = '#e0a000'
        black = '#181010'
    elif colsystem == 7:
        white = '#f8e8f8'
        lightgrey = '#e0a078'
        darkgrey = '#a87048'
        black = '#181010'
    elif colsystem == 8:
        white = '#f8e8f8'
        lightgrey = '#d0a8b0'
        darkgrey = '#787890'
        black = '#181010'
    elif colsystem == 9:
        white = '#f8e8f8'
        lightgrey = '#d8b0c0'
        darkgrey = '#a878b8'
        black = '#181010'
    elif colsystem == 10:
        white = '#f8e8f8'
        lightgrey = '#90a0d8'
        darkgrey = '#5878b8'
        black = '#181010'
    elif colsystem == 11:
        white = '#f8e8f8'
        lightgrey = '#f0b0c0'
        darkgrey = '#e078a8'
        black = '#181010'
    elif colsystem == 12:
        white = '#f8e8f8'
        lightgrey = '#f0b088'
        darkgrey = '#807098'
        black = '#181010'
    elif colsystem == 13:
        white = '#f8e8f8'
        lightgrey = '#383838'
        darkgrey = '#101818'
        black = '#181010'
    elif colsystem == 14:
        white = '#ef0000'
        lightgrey = '#a40000'
        darkgrey = '#550000'
        black = '#000000'
    elif colsystem == 15:
        black = '#ef0000'
        darkgrey = '#a40000'
        lightgrey = '#550000'
        white = '#000000'
    elif colsystem == 16:
        white = input('Enter the hex code for the white: ')
        lightgrey = input('Enter the hex code for the lightgrey: ')
        darkgrey = input('Enter the hex code for the darkgrey: ')
        black = input('Enter the hex code for the black: ')
    break

pixsize = int(input('''Enter the width of each pixel:
>>> '''))
        
showprocess = input('''Show the decompression process? (y/n)
>>> ''')


path = 'Converted_Graphics/' + imagename + '.bin'
print(path)
os.system(f'certutil -encodehex {path} temp.txt')

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
if rng:
    binarydata2 = binarydata[8:]
    binarydata2 = [i for i in binarydata2]
    random.shuffle(binarydata2)
    binarydata2 = "".join(binarydata2)
    binarydata = binarydata[:8] + binarydata2
    print('''
WARNING
The CORRUPTOR has been activated.
Results may not be as expected.
Do not complain, you caused this.
''')

window = Tk()
if showprocess == 'y':
    c = Canvas(width = 112 * pixsize, height = 56 * pixsize, bg = white)
else:
    c = Canvas(width = 56 * pixsize, height = 56 * pixsize, bg = white)
c.pack()

window.attributes('-topmost', True)

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
        try:
            returned_bits += binarydata[datapointer]
            datapointer += 1
        except IndexError:
            returned_bits += '0'
    return returned_bits


width = bin_to_int(get_next_bits(4))
height = bin_to_int(get_next_bits(4))
firstbp = int(get_next_bits(1))

x = 0
y = 0

#add whitespace
v_offset = 7 - height
c.create_rectangle(0,0,112*pixsize,8*v_offset*pixsize,fill=white, outline = white)
h_offset_left = 4 - ((width + 1)//2)
h_offset_right = 3 - (width//2)
c.create_rectangle(0,0,8*h_offset_left*pixsize,56*pixsize,fill=white, outline = white)
c.create_rectangle(56*pixsize,0,(56*pixsize)+(8*pixsize*h_offset_left),56*pixsize,fill=white, outline = white)
c.create_rectangle(56*pixsize,0,(56*pixsize)-(8*pixsize*h_offset_right),56*pixsize,fill=white, outline = white)
c.create_rectangle(112*pixsize,0,(112*pixsize)-(80*h_offset_right*pixsize),56*pixsize,fill=white, outline = white)
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
                try:
                    grid[x][y] = 0
                    grid[x+1][y] = 0
                    if showprocess == 'y':
                        c.create_rectangle(x*pixsize,y*pixsize,(x*pixsize)+(2*pixsize),(y*pixsize)+pixsize, fill = white, outline = white)
                    y += 1
                    if y >= 56:
                        y = 8*v_offset
                        x += 2
                    window.update()
                    pixelsdrawn += 2
                except IndexError:
                    pass

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
                            if showprocess == 'y':
                                c.create_rectangle(x*pixsize,y*pixsize,(x*pixsize)+pixsize,(y*pixsize)+pixsize, fill = white, outline = white)
                            grid[x][y] = 0
                        else:
                            if showprocess == 'y':
                                c.create_rectangle(x*pixsize,y*pixsize,(x*pixsize)+pixsize,(y*pixsize)+pixsize, fill = black, outline = black)
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
if showprocess == 'y':
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
if showprocess == 'y':
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
                if showprocess == 'y':
                    c.create_rectangle(x*pixsize,y*pixsize,(x*pixsize)+pixsize,(y*pixsize)+pixsize, fill = black, outline = black)
                grid[x][y] = 1
            else:
                if showprocess == 'y':
                    c.create_rectangle(x*pixsize,y*pixsize,(x*pixsize)+pixsize,(y*pixsize)+pixsize, fill = white, outline = white)
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
                if showprocess == 'y':
                    c.create_rectangle(x*pixsize,y*pixsize,(x*pixsize)+pixsize,(y*pixsize)+pixsize, fill = white, outline = white)
                grid[x][y] = 0
            else:
                if showprocess == 'y':
                    c.create_rectangle(x*pixsize,y*pixsize,(x*pixsize)+pixsize,(y*pixsize)+pixsize, fill = black, outline = black)
                grid[x][y] = 1
        window.update()
    print('XOR performed successfully.')

if encodingmode == 1:
    deltadecode(0)
    if showprocess == 'y':
        sleep(1)
    deltadecode(1)
    if showprocess == 'y':
        sleep(1)

elif encodingmode == 2:
    deltadecode(firstbp)
    if showprocess == 'y':
        sleep(1)
    xor()
    if showprocess == 'y':
        sleep(1)

else:
    deltadecode(0)
    if showprocess == 'y':
        sleep(1)
    deltadecode(1)
    if showprocess == 'y':
        sleep(1)
    xor()
    if showprocess == 'y':
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
            c.create_rectangle(x*pixsize,y*pixsize,(x*pixsize)+pixsize,(y*pixsize)+pixsize, fill = colour, outline = colour)
        window.update()
    print('Complete.')
    c.create_rectangle(56*pixsize,0,112*pixsize,56*pixsize,fill=white,outline=white)

combine_bitplanes()
window.mainloop()
