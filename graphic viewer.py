from tkinter import *
from time import sleep
import os
import random

imagename = ""
while imagename.strip('!') + ".bin" not in os.listdir("Converted_Graphics"):
    imagename = input('''Enter the name of the image in Converted_Graphics:
(You can use \"!\" to corrupt the pokemon, for example: \"!mew\")
>>> Converted_Graphics/''')

rng = False
if imagename.startswith('!'):
    imagename = imagename.strip('!')
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
    elif colsystem == 1: colours = {"white": "#e0f8d0", "lightgrey": "#88c070", "darkgrey": "#346856", "black": "#081820"}
    elif colsystem == 2: colours = {"white": "#ffffff", "lightgrey": "#a9a9a9", "darkgrey": "#545454", "black": "#000000"}
    elif colsystem == 3: colours = {"white": "#f8e8f8", "lightgrey": "#a0d080", "darkgrey": "#48a058", "black": "#181010"}
    elif colsystem == 4: colours = {"white": "#f8e8f8", "lightgrey": "#f8a050", "darkgrey": "#d05030", "black": "#181010"}
    elif colsystem == 5: colours = {"white": "#f8e8f8", "lightgrey": "#a8c8e8", "darkgrey": "#7098c8", "black": "#181010"}
    elif colsystem == 6: colours = {"white": "#f8e8f8", "lightgrey": "#f8e070", "darkgrey": "#e0a000", "black": "#181010"}
    elif colsystem == 7: colours = {"white": "#f8e8f8", "lightgrey": "#e0a078", "darkgrey": "#a87048", "black": "#181010"}
    elif colsystem == 8: colours = {"white": "#f8e8f8", "lightgrey": "#d0a8b0", "darkgrey": "#787890", "black": "#181010"}
    elif colsystem == 9: colours = {"white": "#f8e8f8", "lightgrey": "#d8b0c0", "darkgrey": "#a878b8", "black": "#181010"}
    elif colsystem == 10:colours = {"white": "#f8e8f8", "lightgrey": "#90a0d8", "darkgrey": "#5878b8", "black": "#181010"}
    elif colsystem == 11:colours = {"white": "#f8e8f8", "lightgrey": "#f0b0c0", "darkgrey": "#e078a8", "black": "#181010"}
    elif colsystem == 12:colours = {"white": "#f8e8f8", "lightgrey": "#f0b088", "darkgrey": "#807098", "black": "#181010"}
    elif colsystem == 13:colours = {"white": "#f8e8f8", "lightgrey": "#383838", "darkgrey": "#101818", "black": "#181010"}
    elif colsystem == 14:colours = {"white": "#ef0000", "lightgrey": "#a40000", "darkgrey": "#550000", "black": "#000000"}
    elif colsystem == 15:colours = {"white": "#000000", "lightgrey": "#550000", "darkgrey": "#a40000", "black": "#ef0000"}
    elif colsystem == 16:colours = {"white": input('Enter the hex code for the white: '), "lightgrey": input('Enter the hex code for the lightgrey: '), "darkgrey": input('Enter the hex code for the darkgrey: '), "black": input('Enter the hex code for the black: ')}
    break

#colours
while True:
    smooth = int(input('''Choose a smoothing mode:
1 - None
2 - Basic smooth
3 - Basic smooth v2
4 - Minimalist
5 - AMOGUS MODE
6 - Corruptor JR.
7 - Hazy vision
8 - 2-Tone
>>> '''))
    if smooth <= 0 or smooth > 8:
        print('Enter a valid smoothing mode.')
        continue
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
    c = Canvas(width = 112 * pixsize, height = 56 * pixsize, bg = colours['white'])
else:
    c = Canvas(width = 56 * pixsize, height = 56 * pixsize, bg = colours['white'])
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
c.create_rectangle(0,0,112*pixsize,8*v_offset*pixsize,fill=colours['white'], outline = colours['white'])
h_offset_left = 4 - ((width + 1)//2)
h_offset_right = 3 - (width//2)
c.create_rectangle(0,0,8*h_offset_left*pixsize,56*pixsize,fill=colours['white'], outline = colours['white'])
c.create_rectangle(56*pixsize,0,(56*pixsize)+(8*pixsize*h_offset_left),56*pixsize,fill=colours['white'], outline = colours['white'])
c.create_rectangle(56*pixsize,0,(56*pixsize)-(8*pixsize*h_offset_right),56*pixsize,fill=colours['white'], outline = colours['white'])
c.create_rectangle(112*pixsize,0,(112*pixsize)-(80*h_offset_right*pixsize),56*pixsize,fill=colours['white'], outline = colours['white'])
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
                        c.create_rectangle(x*pixsize,y*pixsize,(x*pixsize)+(2*pixsize),(y*pixsize)+pixsize, fill = colours['white'], outline = colours['white'])
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
                                c.create_rectangle(x*pixsize,y*pixsize,(x*pixsize)+pixsize,(y*pixsize)+pixsize, fill = colours['white'], outline = colours['white'])
                            grid[x][y] = 0
                        else:
                            if showprocess == 'y':
                                c.create_rectangle(x*pixsize,y*pixsize,(x*pixsize)+pixsize,(y*pixsize)+pixsize, fill = colours['black'], outline = colours['black'])
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

        for j in range(56-8*h_offset_right):
            flipornot = grid[x][y]
            if flipornot == 1:
                col = not col
            
            if col:
                if showprocess == 'y':
                    c.create_rectangle(x*pixsize,y*pixsize,(x*pixsize)+pixsize,(y*pixsize)+pixsize, fill = colours['black'], outline = colours['black'])
                grid[x][y] = 1
            else:
                if showprocess == 'y':
                    c.create_rectangle(x*pixsize,y*pixsize,(x*pixsize)+pixsize,(y*pixsize)+pixsize, fill = colours['white'], outline = colours['white'])
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
                    c.create_rectangle(x*pixsize,y*pixsize,(x*pixsize)+pixsize,(y*pixsize)+pixsize, fill = colours['white'], outline = colours['white'])
                grid[x][y] = 0
            else:
                if showprocess == 'y':
                    c.create_rectangle(x*pixsize,y*pixsize,(x*pixsize)+pixsize,(y*pixsize)+pixsize, fill = colours['black'], outline = colours['black'])
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


# Below this is a load of smoother shit, LOOK AT YOUR OWN RISK!
def x3load():
    global x, y, grid, smooth

    sub = pixsize/3

    try:
        for y in range(56):
            for x in range(56):
                if smooth == 1:
                    if grid[x][y] == 0 and grid[x+56][y] == 0:   pixColour = colours['white']
                    elif grid[x][y] == 0 and grid[x+56][y] == 1: pixColour = colours['lightgrey']
                    elif grid[x][y] == 1 and grid[x+56][y] == 0: pixColour = colours['darkgrey']
                    else:                                        pixColour = colours['black']
                    c.create_rectangle(x*pixsize,y*pixsize,(x*pixsize)+pixsize,(y*pixsize)+pixsize, fill = pixColour, outline = pixColour)
                    continue
                i = 0
                for subY in range(3):
                    for subX in range(3):
                        s = []
                        for yy in range(3):
                            for xx in range(3):
                                try:
                                    if   grid[x+xx-1][y+yy-1] == 0 and grid[x+xx+55][y+yy-1] == 0: stemp = "4"
                                    elif grid[x+xx-1][y+yy-1] == 0 and grid[x+xx+55][y+yy-1] == 1: stemp = "3"
                                    elif grid[x+xx-1][y+yy-1] == 1 and grid[x+xx+55][y+yy-1] == 0: stemp = "2"
                                    else:                                                          stemp = "1"
                                except: stemp = "4"
                                s.append(stemp)
                        if smooth == 2:   data = smoothing(s)
                        elif smooth == 3: data = smoothingv2(s)
                        elif smooth == 4: data = minimalist_smooth(s)
                        elif smooth == 5: data = amogus_smooth(s)
                        elif smooth == 6: data = corruptor_jr(s)
                        elif smooth == 7: data = hazy_smooth(s)
                        elif smooth == 8: data = cum_mode(s)
                        if   data[i] == "4": pixColour = colours['white']
                        elif data[i] == "3": pixColour = colours['lightgrey']
                        elif data[i] == "2": pixColour = colours['darkgrey']
                        else:                pixColour = colours['black']
                        c.create_rectangle((x*pixsize)+sub*(subX),(y*pixsize)+sub*(subY),(x*pixsize)+sub*(subX+1),(y*pixsize)+sub*(subY+1), fill = pixColour, outline = pixColour)
                        i += 1
            window.update()
        print('Rendered.')
        c.create_rectangle(56*pixsize,0,112*pixsize,56*pixsize,fill=colours['white'],outline=colours['white'])
    except: print('Fatal error rendering.')

def smoothing(s):
    newtile = []
    for x in range(9): newtile.append(s[4])
    pixcolour = s[4]

    if s[0] == s[1] == s[3]:
        if s[0] != pixcolour:
            newtile[0] = s[0]
    if s[2] == s[1] == s[5]:
        if s[2] != pixcolour:
            newtile[2] = s[2]
    if s[6] == s[7] == s[3]:
        if s[6] != pixcolour:
            newtile[6] = s[6]
    if s[8] == s[7] == s[5]:
        if s[8] != pixcolour:
            newtile[8] = s[8]

    data = ""
    for x in range(9): data += newtile[x]

    return data

def minimalist_smooth(s):
    newtile = []
    for x in range(9): newtile.append(s[4])
    pixcolour = s[4]

    for x in range(4):
        t = str(x+1)
        if s[1] == t:
            if int(t) > int(pixcolour):
                newtile[0] = t
                newtile[1] = t
                newtile[2] = t
        if s[3] == t:
            if int(t) > int(pixcolour):
                newtile[0] = t
                newtile[3] = t
                newtile[6] = t
        if s[7] == t:
            if int(t) > int(pixcolour):
                newtile[6] = t
                newtile[7] = t
                newtile[8] = t
        if s[5] == t:
            if int(t) > int(pixcolour):
                newtile[2] = t
                newtile[5] = t
                newtile[8] = t

    data = ""
    for x in range(9): data += newtile[x]

    return data

def amogus_smooth(s):
    newtile = []
    for x in range(9): newtile.append(s[4])
    pixcolour = s[4]

    for x in range(4):
        t = str(x+1)
        if s[1] == t:
            if int(t) > int(pixcolour):
                newtile[0] = t
                newtile[1] = t
                newtile[2] = t
        if s[3] == t:
            if int(t) < int(pixcolour):
                newtile[0] = t
                newtile[3] = t
                newtile[6] = t
        if s[7] == t:
            if int(t) < int(pixcolour):
                newtile[6] = t
                newtile[7] = t
                newtile[8] = t
        if s[5] == t:
            if int(t) < int(pixcolour):
                newtile[2] = t
                newtile[5] = t
                newtile[8] = t

    data = ""
    for x in range(9): data += newtile[x]

    return data

def corruptor_jr(s):
    mode = random.randint(1, 4)
    if mode == 1:   return smoothing(s)
    elif mode == 2: return minimalist_smooth(s)
    elif mode == 3: return amogus_smooth(s)
    elif mode == 4: return hazy_smooth(s)

def hazy_smooth(s):
    data = ""
    for x in range(9): data += s[x]

    return data

def cum_mode(s):
    newtile = []
    for x in range(9): newtile.append(s[4])

    for x in range(len(newtile)):
        if newtile[x] != "4":
            newtile[x] = "3"
            
    data = ""
    for x in range(9): data += newtile[x]

    return data

def smoothingv2(s):
    newtile = []
    for x in range(9): newtile.append(s[4])
    pixcolour = s[4]

    if s[0] == s[1] == s[3] and s[0] > pixcolour: newtile[0] = s[0]
    if s[2] == s[1] == s[5] and s[2] > pixcolour: newtile[2] = s[2]
    if s[6] == s[7] == s[3] and s[6] > pixcolour: newtile[6] = s[6]
    if s[8] == s[7] == s[5] and s[8] > pixcolour: newtile[8] = s[8]

    if s[1] == s[3] < pixcolour and int(newtile[0]) != int(s[1]): newtile[0] = s[1]
    if s[1] == s[5] < pixcolour and int(newtile[2]) != int(s[1]): newtile[2] = s[1]
    if s[7] == s[3] < pixcolour and int(newtile[6]) != int(s[7]): newtile[6] = s[7]
    if s[7] == s[5] < pixcolour and int(newtile[8]) != int(s[7]): newtile[8] = s[7]

    data = ""
    for x in range(9): data += newtile[x]

    return data

x3load()
window.mainloop()