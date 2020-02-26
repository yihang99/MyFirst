#exercise

import turtle
turtle.speed(10)
turtle.setup(500,500,100,100)
turtle.penup()
turtle.right(90)
turtle.fd(30)
turtle.pendown()
turtle.pensize(5)
turtle.pencolor(0.93,0.2,0.54)

for i in range(25, 150):
    turtle.circle(2*i, 20)

turtle.done()
