from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

score = 0
jump = False
desc = False
angle = 1
square_x1 = 100
square_x2 = 150
square_y1 = 105
square_y2 = 155
line_x1 = 12000
bubbles = []
height_increase = 150
pause = False
Shoot = False
game_over = False
warning = False
shooter_sens = 15
bullet_speed = 0.8
bubble_speed = 0.1
misfire_count = 0
bubble_miss_count = 0
warning_frame = 0
jump_height = 0
rotation_angle = 0


def draw_square(x1, y1, x2, y2):
    # Initialize lists to store coordinates of the square
    coords = []

    # Draw the lines of the square using the midpoint line algorithm
    draw_square_pixels(x1, y1, x2, y1, coords)
    draw_square_pixels(x2, y1, x2, y2, coords)
    draw_square_pixels(x2, y2, x1, y2, coords)
    draw_square_pixels(x1, y2, x1, y1, coords)

    draw_pixels(coords)


def draw_square_pixels(x1, y1, x2, y2, coords):
    # Calculate dx and dy
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    # Determine the sign of slope
    if x1 < x2:
        sx = 1
    else:
        sx = -1
    if y1 < y2:
        sy = 1
    else:
        sy = -1

    # Initialize decision parameters
    if dx > dy:
        P = 2 * dy - dx
        while x1 != x2:
            coords.append([x1,y1])

            if P > 0:
                y1 += sy
                P -= 2 * dx
            x1 += sx
            P += 2 * dy
    else:
        P = 2 * dx - dy
        while y1 != y2:
            coords.append([x1, y1])
            if P > 0:
                x1 += sx
                P -= 2 * dy
            y1 += sy
            P += 2 * dx
    coords.append([x1, y1])


def draw_circle(center_x, center_y, r):
    x = 0
    y = r
    d = 5-4*r
    while y >= x:
        draw_circle_pixels(x, y, center_x, center_y)
        if d <= 0:
            d += 4*(2*x + 3)
            x += 1
        else:
            d += 4*(2*x - 2*y + 5)
            x += 1
            y -= 1


def draw_circle_pixels(x, y, center_x, center_y):
    glBegin(GL_POINTS)
    glVertex2f(x + center_x, y + center_y)
    glVertex2f(-x + center_x, y + center_y)
    glVertex2f(x + center_x, -y + center_y)
    glVertex2f(-x + center_x, -y + center_y)
    glVertex2f(y + center_x, x + center_y)
    glVertex2f(-y + center_x, x + center_y)
    glVertex2f(y + center_x, -x + center_y)
    glVertex2f(-y + center_x, -x + center_y)
    glEnd()


def draw_line(x0, y0, x1, y1):
    zone = find_zone(x0, y0, x1, y1)
    if zone == 0:
        midPointLine(x0, y0, x1, y1, zone)
    if zone == 1:
        midPointLine(y0, x0, y1, x1, zone)
    if zone == 2:
        midPointLine(y0, -x0, y1, -x1, zone)
    if zone == 3:
        midPointLine(-x0, y0, -x1, y1, zone)
    if zone == 4:
        midPointLine(-x0, -y0, -x1, -y1, zone)
    if zone == 5:
        midPointLine(-y0, -x0, -y1, -x1, zone)
    if zone == 6:
        midPointLine(-y0, x0, -y1, x1, zone)
    if zone == 7:
        midPointLine(x0, -y0, x1, -y1, zone)


def midPointLine(x0, y0, x1, y1, zone):
    dx = x1 - x0
    dy = y1 - y0
    delE = 2 * dy
    delNE = 2 * (dy - dx)
    d = 2 * dy - dx
    x = x0
    y = y0
    points = []
    while x < x1:
        original_zone(x, y, zone, points)
        if d < 0:
            d += delE
            x += 1
        else:
            d += delNE
            x += 1
            y += 1

    draw_pixels(points)


def original_zone(x, y, zone, points):
    if zone == 0:
        points.append((x, y))
    if zone == 1:
        points.append((y, x))
    if zone == 2:
        points.append((-y, x))
    if zone == 3:
        points.append((-x, y))
    if zone == 4:
        points.append((-x, -y))
    if zone == 5:
        points.append((-y, -x))
    if zone == 6:
        points.append((y, -x))
    if zone == 7:
        points.append((x, -y))


def find_zone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) >= abs(dy):
        if dx >= 0:
            if dy >= 0:
                zone = 0
            else:
                zone = 7
        else:
            if dy >= 0:
                zone = 3
            else:
                zone = 4
    else:
        if dx >= 0:
            if dy >= 0:
                zone = 1
            else:
                zone = 6
        else:
            if dy >= 0:
                zone = 2
            else:
                zone = 5
    return zone


def draw_pixels(coords):
    glBegin(GL_POINTS)
    for x, y in coords:
        glVertex2f(x, y)
    glEnd()


def close_button():
    global score
    print(f'GGWP!  Score: {score}')
    glutLeaveMainLoop()


def stop_button():
    global pause
    if pause:
        print('Lock In !')
    else:
        print('Paused!')
    pause = not pause


def restart_button():
    global score, pause, game_over, bubbles, bubble_miss_count, misfire_count, warning_frame
    game_over = False
    score = 0
    bubble_miss_count = 0
    misfire_count = 0
    warning_frame = 0
    pause = False
    bubbles.clear()
    print('Starting Over!')




def main_box():
    glClear(GL_COLOR_BUFFER_BIT)
    global jump_height, rotation_angle, square_x1, square_x2, square_y1, square_y2, angle
    glTranslatef(0, jump_height, 0)  # Translate to the center of the square
    glRotatef(rotation_angle, 0, 0, angle)
    draw_square(square_x1, square_y1, square_x2, square_y2)


def obstacles():

    global line_x1
    draw_square(line_x1-10760, 100, line_x1-10700, 200)



def display():
    global pause, Shoot, bubbles, jump_height, rotation_angle, jump, line_x1
    glClear(GL_COLOR_BUFFER_BIT)
    glPushMatrix()
    main_box()
    glPopMatrix()
    obstacles()
    draw_line(0, 100, line_x1, 100)
    glFlush()
    glutSwapBuffers()


def animate():
    global jump_height, rotation_angle, jump, square_x1, square_x2, height_increase, square_y1, square_y2, desc, angle, line_x1

    if jump:
        jump_height += height_increase
        rotation_angle -= 20  # Decrease jump height to simulate falling
    if desc:
        jump_height -= height_increase
        rotation_angle -= 20
    if jump_height >= 400 and jump:
        desc = True
        jump = False
        angle = 1

    if (jump_height <= 0 or rotation_angle <= -100) and desc:
        desc = False
        rotation_angle = 0
        jump_height = 0
        angle = 1

    line_x1 -= 15

    glutPostRedisplay()


def timer(value):
    global pause, game_over, bubble_speed
    glutPostRedisplay()
    glutTimerFunc(1600, timer, 0)



def mouse_callback(button, state, x, y):
    # global pause, game_over, Shoot, bullet_x, bullet_y
    # print(f"Mouse Clicked at ({x}, {y})")
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            if 440 <= x <= 500 and 10 <= y <= 60:
                close_button()

            elif 242 <= x <= 275 and 10 <= y <= 60:
                stop_button()

            elif 10 <= x <= 50 and 10 <= y <= 60:
                restart_button()

            # elif not pause and not game_over:
            #     Shoot = True
            #     bullet_x = shooter_x
            #     bullet_y = 60


def keyboard_listener(key, x, y):
    global jump, desc
    if key == b' ' and not jump and not desc:
        jump = True




def reshape(width, height):
    glViewport(0, 0, GLsizei(width), GLsizei(height))
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, float(width), 0.0, float(height))
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1000, 500)
    glutCreateWindow(b"Dash")

    glClearColor(0.0, 0.0, 0.0, 0.0)  # Set clear color to black
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glutKeyboardFunc(keyboard_listener)
    glutMouseFunc(mouse_callback)
    glutTimerFunc(0, timer, 0)
    glutIdleFunc(animate)
    glutMainLoop()


if __name__ == "__main__":
    main()