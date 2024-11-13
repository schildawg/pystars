
from astropy.coordinates import SkyCoord
import astropy.units as u

import turtle, time, csv

scale = 1
angle = 0
offset = 0

# Converts from text to coordinates
#
def convert(ra, dec):
   coord = SkyCoord(ra, dec, unit=(u.hourangle, u.deg))
   
   return coord.ra.deg, coord.dec.deg

# Draws a star!
#
def draw(ra, dec, mag, color, name = "x"):
    pen.up()
    pen.goto(0, offset)

    coord = convert(ra, dec)
    if coord[1] < 0:
        return
    
    pen.setheading(270 - coord[0] + angle)
    pen.forward(360*scale - 4*scale*coord[1])

    pen.down()
    pen.begin_fill() 

    scolor = "#d4deff"
    if color < -0.40:
        scolor = "#d4deff" # Blue
    elif -0.40 <= color < -0.30:
        scolor = "#d4deff" # Blue
    elif -0.30 <= color < -0.10:
        scolor = "lightblue"  # Blue-White
    elif -0.10 <= color < +0.10:
        scolor = "white"  # White
    elif +0.10 <= color < +0.30:
        scolor = "#eaecff"  # Yellow-White
    elif +0.30 <= color < +0.60:
        scolor = "#f9f5ff"  # Yellow
    elif +0.60 <= color < +1.00:
        scolor = "#fff4ea"  # Orange
    elif +1.00 <= color < +1.50:
       scolor = "#fed7a2"  # Red
    elif +1.50 <= color < +2.00:
        "#ffd8a5"  # Deep Red
    else:  # +2.00 and above
        scolor = "orange"  # Very Red

    pen.dot(abs(7 - mag), scolor) 
    pen.end_fill() 

# Draws a line connecting two stars!
#
def line(star1, star2):
    pen.up()
    pen.goto(0, offset)
    
    coord1 = convert(star1[4], star1[5])

    pen.setheading(270 - coord1[0] + angle)
    pen.forward(360*scale - 4*scale*coord1[1])
    start_pos = pen.pos()

    pen.up()
    pen.goto(0, offset)
    coord2 = convert(star2[4], star2[5])
    pen.setheading(270 - coord2[0] + angle)
    pen.forward(360*scale - 4*scale*coord2[1])

    pen.down()
    pen.goto(start_pos)      


def draw_lines(stars, lines):
    pen.color("#9ea8be")

    for l in lines:
        constellation = l[0]
        designator = l[1]

        first = find(stars, constellation, designator)

        constellation2 = l[2]
        designator2 = l[3]

        second = find(stars, constellation2, designator2)
        if first != -1 and second != -1:
            line(stars[first], stars[second])

def find(stars, constellation, name):
    i = 0
    for star in stars:
        print(star[1] + " " + star[3])
        if star[1] == constellation and star[3] == name:
           return i
        i = i + 1
    
    return -1

# Draws all stars!
#
def draw_stars(stars):
    for i in range(0, len(stars)):
        ra = stars[i][4]
        dec = stars[i][5]
        
        mag = 0.0
        mag_str = stars[i][8]
        if mag_str == "":
            mag = 4
        else:
            mag = float(mag_str)
        
        color = stars[i][9]
        bv = 0
        if color != "":
           bv = float(color)

        designator = stars[i][2]

        draw(ra, dec, mag, bv, designator)

stars = []
with open('stars.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  
    stars.append(header)  

    for row in csv_reader:
        stars.append(row)

lines = []
with open('lines.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  
    lines.append(header)  

    for row in csv_reader:
        lines.append(row)

screen = turtle.Screen() 
screen.bgcolor("darkblue") 
  
pen = turtle.Turtle() 
pen.speed(0) 
pen.fillcolor("blue") 

while True:
   angle = angle + 1
   
   pen.up()
   screen.tracer(0) 
   screen.bgcolor("#0a081f") 
   pen.fillcolor("#0a081f")  

   pen.begin_fill()
   pen.goto(-800, 800)  # Top-left corner
   pen.goto(800, 800)   # Top-right corner
   pen.goto(800, -800)  # Bottom-right corner
   pen.goto(-800, -800) # Bottom-left corner
   pen.goto(-800, 800)  # Back to top-left corner
   pen.end_fill()
   pen.up()

   draw_lines(stars, lines)
   draw_stars(stars)

   time.sleep(.1)
