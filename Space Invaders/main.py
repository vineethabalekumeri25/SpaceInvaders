import turtle
import random
import time

# Screen setup
screen = turtle.Screen()
screen.title("Space Invaders")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

# Title text
title_text = turtle.Turtle()
title_text.hideturtle()
title_text.color("green")
title_text.penup()
title_text.goto(0, 260)
title_text.write("SPACE INVADERS", align="center", font=("Courier", 24, "bold"))

# Score display
score = 0
score_display = turtle.Turtle()
score_display.hideturtle()
score_display.color("white")
score_display.penup()
score_display.goto(-350, 260)
score_display.write(f"Score: {score}", align="left", font=("Courier", 18, "normal"))

# Spaceship
spaceship = turtle.Turtle()
spaceship.shape("square")
spaceship.color("cyan")
spaceship.shapesize(stretch_wid=1, stretch_len=2)
spaceship.penup()
spaceship.goto(0, -250)

# Alien setup
aliens = []
alien_colors = ["red", "orange", "purple", "yellow"]
for i in range(7):
    for j in range(4):
        alien = turtle.Turtle()
        alien.shape("square")
        alien.color(random.choice(alien_colors))
        alien.penup()
        alien.shapesize(stretch_wid=1, stretch_len=2)
        alien.goto(-300 + i * 100, 200 - j * 50)
        aliens.append(alien)

# Barriers setup (rectangular barriers in white color)
barriers = []

def create_barrier(x, y):
    barrier = []
    for i in range(4):  # 4 blocks per row
        block = turtle.Turtle()
        block.shape("square")
        block.color("white")  # Barrier is white
        block.penup()
        block.shapesize(stretch_wid=1, stretch_len=2)
        block.goto(x + i * 20, y)
        barrier.append(block)
    return barrier

# Create barriers
barriers.append(create_barrier(-200, -100))
barriers.append(create_barrier(0, -100))
barriers.append(create_barrier(200, -100))

# Bullet setup for spaceship
bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("yellow")
bullet.penup()
bullet.speed(0)
bullet.hideturtle()
bullet.setheading(90)
bullet.shapesize(stretch_wid=0.3, stretch_len=1)
bullet_state = "ready"

# Alien bullet setup
alien_bullets = []

def create_alien_bullet(x, y):
    alien_bullet = turtle.Turtle()
    alien_bullet.shape("square")
    alien_bullet.color("red")
    alien_bullet.penup()
    alien_bullet.speed(0)
    alien_bullet.setheading(270)  # Alien bullets move downwards
    alien_bullet.shapesize(stretch_wid=0.3, stretch_len=1)
    alien_bullet.goto(x, y)
    alien_bullets.append(alien_bullet)

# Movement functions for spaceship
def move_left():
    x = spaceship.xcor() - 20
    if x > -370:
        spaceship.setx(x)

def move_right():
    x = spaceship.xcor() + 20
    if x < 370:
        spaceship.setx(x)

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.goto(spaceship.xcor(), spaceship.ycor() + 10)
        bullet.showturtle()

# Collision check function
def is_collision(t1, t2):
    return t1.distance(t2) < 25

# Barrier hit check function
def check_barrier_collision(bullet, barrier):
    for block in barrier:
        if is_collision(bullet, block):
            block.hideturtle()
            return True
    return False

# Key bindings
screen.listen()
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")
screen.onkey(fire_bullet, "space")

# Game loop
game_over = False
alien_direction = 10
alien_speed = 0.05  # Decreased speed
alien_descent = 10

while not game_over:
    screen.update()

    # Move aliens left and right and slowly descend
    for alien in aliens:
        alien.setx(alien.xcor() + alien_direction)

    # Check if aliens hit the screen edge
    for alien in aliens:
        if alien.xcor() > 370 or alien.xcor() < -370:
            alien_direction *= -1
            for a in aliens:
                a.sety(a.ycor() - alien_descent)
            break

    # Move bullet from spaceship
    if bullet_state == "fire":
        bullet.sety(bullet.ycor() + 20)
        if bullet.ycor() > 300:
            bullet.hideturtle()
            bullet_state = "ready"

    # Check bullet collision with aliens
    for alien in aliens:
        if is_collision(bullet, alien):
            alien.hideturtle()
            aliens.remove(alien)
            bullet.hideturtle()
            bullet_state = "ready"
            score += 10
            score_display.clear()
            score_display.write(f"Score: {score}", align="left", font=("Courier", 18, "normal"))

    # Check if bullet hits barriers
    for barrier in barriers:
        if check_barrier_collision(bullet, barrier):
            bullet.hideturtle()
            bullet_state = "ready"

    # Create alien bullets (aliens shoot)
    if random.randint(1, 100) < 2:  # Random chance for aliens to shoot
        shooting_alien = random.choice(aliens)
        create_alien_bullet(shooting_alien.xcor(), shooting_alien.ycor())

    # Move alien bullets
    for alien_bullet in alien_bullets:
        alien_bullet.sety(alien_bullet.ycor() - 15)
        if alien_bullet.ycor() < -300:
            alien_bullet.hideturtle()
            alien_bullets.remove(alien_bullet)

        # Check collision between alien bullet and spaceship
        if is_collision(spaceship, alien_bullet):
            game_over = True
            alien_bullet.hideturtle()
            break

    # Check if aliens reach spaceship
    for alien in aliens:
        if alien.ycor() < -230:
            game_over = True

    # Check if all aliens are destroyed
    if not aliens:
        print("You win!")
        game_over = True

    time.sleep(alien_speed)

# Display Game Over
game_over_text = turtle.Turtle()
game_over_text.hideturtle()
game_over_text.color("red")
game_over_text.penup()
game_over_text.goto(0, 0)
game_over_text.write("GAME OVER", align="center", font=("Courier", 36, "bold"))

screen.mainloop()
