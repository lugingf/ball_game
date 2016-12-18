import tkinter
import random

WIDTH = 600
HEIGHT = 450
BG_COLOR = 'white'
ZERO = 0
MAIN_BALL_RADIUS = 30
MAIN_BALL_COLOR = 'blue'
INIT_DX = 2
INIT_DY = 2
DELAY = 10
BAD_COLOR = 'red'
COLORS = [BAD_COLOR, 'black', 'yellow', 'grey', 'aqua', 'fuchsia', BAD_COLOR, 'pink', 'gold']

NUM_OF_BALLS = 10


class Balls():
	def __init__(self, x, y, r, color, dx=0, dy=0):
		self.x = x
		self.y = y
		self.color = color
		self.r = r
		self.dx = dx
		self.dy = dy
	
	def draw(self):
		canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=self.color, outline=self.color if self.color != BAD_COLOR else 'black')  # Х-радиус, X+радиус - координаты углов прямоугольника, в который вписан наш овал
	
	
	def hide(self):	
		canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=BG_COLOR, outline=BG_COLOR)
	
	
	def is_collision(self, ball):
		a = abs(self.x + self.dx - ball.x)
		b = abs(self.y + self.dy - ball.y)
		return (a*a + b*b)**0.5 <= self.r + ball.r
	
	def move(self):
		# colliding with walls
		if (self.x + self.r + self.dx >= WIDTH) or (self.x - self.r + self.dx <= ZERO):
			self.dx = -self.dx
		if (self.y + self.r + self.dy >= HEIGHT) or (self.y - self.r + self.dy <= ZERO):
			self.dy = -self.dy
		# colliding with balls
		for ball in balls:
			if self.is_collision(ball):
					if ball.color != BAD_COLOR:  #good ball
						ball.hide()
						balls.remove(ball)
						self.dx = -self.dx
						self.dy = -self.dy
					else:
						self.dx = self.dy = 0
		self.hide()  # прячем объект, чтобы перерисовать
		self.x += self.dx  # меняем координаты, чтобы нарисовать в новом месте
		self.y += self.dy
		self.draw()
	


#mouse events
def mouse_click(event):
	global main_ball
	if event.num == 1:
		if 'main_ball' not in globals():
			main_ball = Balls(event.x, event.y, MAIN_BALL_RADIUS, MAIN_BALL_COLOR, INIT_DX, INIT_DY)  #создание объекта в памяти
			main_ball.draw()  #вывод созданного объекта на экран - методом create_oval
		else:  #поворот налево
			if main_ball.dx * main_ball.dy > 0:
				main_ball.dy = -main_ball.dy
			else:
				main_ball.dx = -main_ball.dx
	elif event.num == 3:  #поворот направо
		if main_ball.dx * main_ball.dy > 0:
			main_ball.dx = -main_ball.dx
		else:
			main_ball.dy = -main_ball.dy
		main_ball.hide()


def create_list_of_balls(number):
	lst = []
	while len(lst) < number:
		next_ball = Balls(random.choice(range(0, WIDTH)),
							random.choice(range(0, HEIGHT)),
							random.choice(range(15, 35)),
							random.choice(COLORS))
		lst.append(next_ball)
		next_ball.draw()
	return lst

#count of bad balls
def count_bad_balls(list_of_balls):
	res = 0
	for ball in list_of_balls:
		if ball.color == BAD_COLOR:
			res += 1
	return res
	
# main game loop
def main():
	if 'main_ball' in globals():
		main_ball.move()
		if len(balls) - num_of_bad_balls == 0:
			canvas.create_text(WIDTH / 2, HEIGHT / 2, text = 'YOU WIN!', font="Arial 20", fill = MAIN_BALL_COLOR)
			main_ball.dx = main_ball.dy = 0
		elif main_ball.dx == main_ball.dy == 0:
			canvas.create_text(WIDTH / 2, HEIGHT / 2, text = 'YOU LOSE!', font="Arial 20", fill = BAD_COLOR)
	root.after(DELAY, main)

	
root = tkinter.Tk()
root.title('Colliding balls')

canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)  #основной объект где рисуем
canvas.pack()  #функция отображения холста
canvas.bind('<Button-1>', mouse_click)  #метод bind() - отслеживание событий <Button-1> - ЛКМ, mouse_click - название функции обработки события
canvas.bind('<Button-3>', mouse_click)

if __name__ == '__main__':
	if 'main_ball' in globals():
		del main_ball
	balls = create_list_of_balls(NUM_OF_BALLS)
	num_of_bad_balls = count_bad_balls(balls)
	main()
	root.mainloop()  #функция обязательна для конца mainloop() запускает цикл обработки событий; пока мы не вызовем эту функцию, наше окно не будет реагировать на внешние раздражители.


