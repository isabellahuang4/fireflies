import sys
import turtle as t

#given list of patterns, draws in turtle 
def draw_patterns(patterns):
    t.setup(1010,510,0,0)
    t.fillcolor('#ffff00')
    t.penup()
    y = 310
#    for p in patterns:
#        p += p
    for p in patterns:
        y -= 60 
        for i in range(len(p)):
            if p[i] == 1:
                t.goto(-500+(i*25),y)
                t.pendown()
                t.begin_fill()
                t.goto(-475+(i*25),y)
                t.goto(-475+(i*25),y-50)
                t.goto(-500+(i*25),y-50)
                t.goto(-500+(i*25),y)
                t.end_fill()
                t.penup()
    t.done()
