import math
import sys

#TODO: There can't be a goal in the table

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __str__(self):
		return "(" + str(self.x) + "," + str(self.y) + ")"

# https://martin-thoma.com/how-to-check-if-two-line-segments-intersect/
#https://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html

linear_margin = 0.4
angle_margin = 30
table = [Point(1.7,1.325),Point(1.73,2.125),Point(4.34,1.2),Point(4.38,2)]
#table = [Point(1.25,1.15),Point(1.3,2.3),Point(4.72,0.88),Point(4.72,2.1)]

def clamp(n, smallest, largest): return max(smallest, min(n, largest)) # https://stackoverflow.com/questions/4092528/how-to-clamp-an-integer-to-some-range

def getNearestPointInPerimeter(obst,p): #https://stackoverflow.com/questions/20453545/how-to-find-the-nearest-point-in-the-perimeter-of-a-rectangle-to-a-given-point


	l = min([obst[0].x, obst[1].x, obst[2].x, obst[3].x])
	t = max([obst[0].y, obst[1].y, obst[2].y, obst[3].y])
	w = max([obst[0].x, obst[1].x, obst[2].x, obst[3].x])
	h = min([obst[0].y, obst[1].y, obst[2].y, obst[3].y])
	

	r = l + w
	b = t + h

	x = clamp(p.x,l,r)
	y = clamp(p.y,t,b)

	dl = abs(x-l)
	dr = abs(x-r)
	dt = abs(y-t)
	db = abs(y-b)
	m = min(dl,dr,dt,db)

	'''
	print("x ", x, file=sys.stderr)
	print("y ", y, file=sys.stderr)
	print("r ", r, file=sys.stderr)
	print("l ", l, file=sys.stderr)
	print("w ", w, file=sys.stderr)
	print("h ", h, file=sys.stderr)
	print("t ", t, file=sys.stderr)
	print("m ", m, file=sys.stderr)
	'''
	
	if(m == dt):
		return Point(x,t)
	elif(m == db):
		return Point(x,b)
	elif(m == dl):
		return Point(l,y)
	return Point(r,y)

def area(p1, p2, p3): 
      
    return abs((p1.x * (p2.y - p3.y) + 
                p2.x * (p3.y - p1.y) + 
                p3.x * (p1.y - p2.y)) / 2.0) 

def isPointInsideArea(p, obst): #https://www.geeksforgeeks.org/check-whether-given-point-lies-inside-rectangle-not/

	A = area(obst[0], obst[1], obst[2]) + area(obst[1], obst[3], obst[2])
	A1 = area(p,obst[0],obst[1])
	A2 = area(p,obst[1],obst[3])
	A3 = area(p,obst[2],obst[3])
	A4 = area(p,obst[0],obst[2])

	#print("A = " + str(A) + " A1 " + str(A1) + " A2 " + str(A2) + " A3 " + str(A3) + " A4 " + str(A4) + " sum " + str(A1 + A2 + A3 + A4))

	return (A == A1 + A2 + A3 + A4)


def deg_to_rotate(position, path, start_p, yaw, i):

	path_deg = math.atan2(position[path[i]].y - start_p.y, position[path[i]].x - start_p.x)*180/math.pi
#	print("path_deg1: ", path_deg, file=sys.stderr)
	if(path_deg < 0):
		path_deg += 360

	#if(path_deg <= 180):
	#	path_deg = 180 - path_deg
	#elif(path_deg < 360):
	#	path_deg = 360 - (path_deg - 180)

	path_deg = 360 - path_deg
	'''
	if(path_deg <= 90):
		#path_deg = 90 - path_deg;
	#elif(path_deg < 180):
		#path_deg = 360 - (path_deg % 90)
		
	elif(path_deg < 270):
		path_deg = 270 - (path_deg % 90)
	elif(path_deg < 360):
		path_deg = 180 - (path_deg % 90)
	'''
	deg_diff = path_deg - yaw
	if(deg_diff > 180):
		deg_diff -= 360
	elif(deg_diff < -180):
		deg_diff += 360
	
	print("path_deg2: ", str(path_deg),file=sys.stderr)
	print("deg_diff: ", str(deg_diff), file=sys.stderr)
#	print("yaw: ", str(yaw), file=sys.stderr)
	return deg_diff

def heuristic(objective, node):

	return abs(objective.x - node.x) + abs(objective.y - node.y)

def distance_calc(node1, node2):
	return math.sqrt(math.pow(node1.x - node2.x, 2) + math.pow(node1.y - node2.y, 2))

def doBoundingBoxesIntersect(a, b):
	return a[0].x < b[1].x and a[1].x > b[0].x and a[0].y < b[1].y and a[1].y > b[0].y


def isPointOnLine(a, b):
	vertice_new = []
	vertice_new.append(Point(0,0))
	vertice_new.append(Point(a[1].x - a[0].x, a[1].y - a[0].y))
	point_new = Point(b.x - a[0].x, b.y - a[0].y)
	res = vertice_new[1].x * point_new.y - point_new.x * vertice_new[1].y
	return abs(res) < 0.000001

def isPointRightOfLine(a, b):
	vertice_new = []
	vertice_new.append(Point(0,0))
	vertice_new.append(Point(a[1].x - a[0].x, a[1].y - a[0].y))

	point_new = Point(b.x - a[0].x, b.y - a[0].y)
	res = vertice_new[1].x * point_new.y - point_new.x * vertice_new[1].y
	return res < 0

def lineSegmentTouchesOrCrossesLine(a, b):
	#print(str(isPointOnLine(a, Point(b[0].x, b[0].y)) or isPointOnLine(a, Point(b[1].x, b[1].y))))
	return isPointOnLine(a, Point(b[0].x, b[0].y)) or isPointOnLine(a, Point(b[1].x, b[1].y)) or (isPointRightOfLine(a, b[0]) != isPointRightOfLine(a, b[1]))

def getBoundingBox(a):
	points = []
	points.append(Point(min(a[0].x, a[1].x), min(a[0].y, a[1].y)))
	points.append(Point(max(a[0].x, a[1].x), max(a[0].y, a[1].y)))
	return points

def doLinesIntersect(a, b):
	box1 = getBoundingBox(a)
	box2 = getBoundingBox(b)
	"""
	print(a[0])
	print(a[1])
	print(b[0])
	print(b[1])
	print(box1[0])
	print(box1[1])
	print(box2[0])
	print(box2[1])
	print(str(doBoundingBoxesIntersect(box1, box2)))
	print(str(lineSegmentTouchesOrCrossesLine(a, b)))
	print(str(lineSegmentTouchesOrCrossesLine(a, b)))
	print("")
	"""
	
	return doBoundingBoxesIntersect(box1, box2) and lineSegmentTouchesOrCrossesLine(a, b) and lineSegmentTouchesOrCrossesLine(b, a)

def nodes_visibles(position, vertices, nodes, beginning, end):

	intersect = 0
	add_vertices = ""

	vertices = [[table[0],table[1]],[table[0],table[2]],[table[1],table[3]],[table[2],table[3]]]

	for v in nodes:
		if(v != beginning):
			for ver in vertices:
				#print(v + " " + str(doLinesIntersect([position[beginning],position[v]], [position[ver[0]], position[ver[1]]])))
				#print(v)
				#print(ver)
				#print("")
				#if(not (intersect & 1) and doLinesIntersect([position[beginning],position[v]], [position[ver[0]], position[ver[1]]])): #[ver[0],ver[1]
				if(not (intersect & 1) and doLinesIntersect([position[beginning],position[v]], [ver[0], ver[1]])):
					intersect |= 1
				#if(v == end or (not (intersect & 2) and doLinesIntersect([position[end], position[v]], [position[ver[0]], position[ver[1]]]))):
				if(v == end or (not (intersect & 2) and doLinesIntersect([position[end], position[v]], [ver[0], ver[1]]))):
					intersect |= 2
				if(intersect == 3):
					break
			#print("intersect: " + v + " " + str(intersect))
			if(intersect != 3):
				if(not (intersect & 1)):
					add_vertices += " " + beginning + "|" + v + "|" + str(distance_calc(position[beginning], position[v]))
				if(not (intersect & 2)):
					add_vertices += " " + end + "|" + v + "|" + str(distance_calc(position[end], position[v]))
			intersect = 0
			
	return add_vertices



def a_star(nodes, vertices, beginning, objective, position):
	"""Algoritmo A* -> recibe la lista de nodes, los vértices con el peso asociado,
	el node de beginning, el node objective y el valor de la función de heurística para
	cada node. Devuelve el path solución"""

	g = {}
	p = {}
	f = {}

	#1.- Se inicializan los conjuntos, se asigna un predecessor nulo a los nodes y una distancia tentativa inicial
	open_set = []
	closed_set = []
	open_set.append(beginning)

	for i in nodes:
		if(i == beginning):
			g[i] = 0
			p[i] = -1
			f[i] = 0
		else:
			g[i] = math.inf

	node_actual = beginning
#	print("node | Distancia | predecessor")

	#2.- Se hacen los calculos correspondientes para obtener el path solución
	while(open_set):
#		print (node_actual, "|",  f[node_actual], "|", p[node_actual])

		if(node_actual == objective):
			return reconstruir_path(p,node_actual)
		
		open_set.remove(node_actual)

		closed_set.append(node_actual)
		print(vertices, file=sys.stderr)
		for i in vertices[node_actual]:
			if(not (i in closed_set)):
				
				g_tent = g[node_actual] + vertices[node_actual][i]
				if( not (i in open_set)):
					open_set.append(i)
				if(g_tent < g[i]):
					p[i] = node_actual
					g[i] = g_tent
					f[i] = g[i] + heuristic(position[objective], position[i])

		minimo = open_set[0]
		for i in open_set:
			if(f[i] < f[minimo]):
				minimo = i
		node_actual = minimo

		
	#3.- Se regresa error	
	print("error")
	
def reconstruir_path(predecessor, actual):
	"""Función de reconstrucción del path -> recibe el node actual y la lista de predecessores de cada node.
	Devuelve el path construido a partir de los predecessores."""

	path = []
	path.append(actual)
	while(predecessor[actual] != -1):
		actual = predecessor[actual]
		path.append(actual)
	return path[::-1]

def format_vertices(vertices):
	"""Función que da format a los vértices que se pide al usuario -> recibe los vértices en el format
	pedido al usuario y los devuelve en un format apto para los algoritmos."""

	l_vertices = vertices.split()
	vertices_dict = {}

	for i in l_vertices:
		elem = i.split('|')
		for x in range(0,2):
			if(x == 0):
				otro = 1
			else:
				otro = 0

			if(elem[x] not in vertices_dict):
				tmp_dict = {elem[x]: {elem[otro] : float(elem[2])}}
				vertices_dict.update(tmp_dict)
			else:
				tmp_dict = {elem[otro]: float(elem[2])}
				vertices_dict[elem[x]].update(tmp_dict)
	return vertices_dict

def extract_vertices(vertices):
	l_vertices = vertices.split()
	vertices_sim = []

	for i in l_vertices:
		elem = i.split('|')
		vertices_sim.append([elem[0], elem[1]])
	return vertices_sim


def loc_instructions(start_p, yaw, goal_p):
	"""Función de menú de entrada para especificar el algoritmo a usar"""

	print("start_p: " +  str(start_p) + " goal_p: " + str(goal_p), file=sys.stderr)
#	print("goal_p:", goal_p)
#	print("yaw:", yaw)
	nodes = {"start", "0", "1", "2", "3", "goal"}
	position = {}
	position.update({"0": Point(1.25,1.15)})
	position.update({"1": Point(4.72,0.88)})
	#position.update({"2": Point(1.3,2.3)})
	position.update({"2": Point(1.2,2.4)})
	position.update({"3": Point(4.72,2.1)})
	beginning = "start"
	end = "goal"
	vertices_raw = "0|1|3.9 0|2|2.4 1|3|2.4 2|3|3.9"
	vertices_sim = extract_vertices(vertices_raw)

	if(isPointInsideArea(goal_p, table)):
		goal_p = getNearestPointInPerimeter(table, goal_p)

	if(isPointInsideArea(start_p, table)):
		start_p = getNearestPointInPerimeter(table, start_p)

	
	body = 0.25
	if(yaw < 90):
		start_p.y += body
	elif(yaw < 180):
		start_p.x += body
	elif(yaw < 270):
		start_p.y -= body
	elif(yaw <= 360):
		start_p.x -= body
	

	position.update({"start": start_p})
	position.update({"goal": goal_p})
	print("Now start_p: " + str(start_p) + " goal_p: " + str(goal_p), file=sys.stderr)

	vertices_extra = nodes_visibles(position, vertices_sim, nodes, beginning, end)
#	print("vertices_extra: ", vertices_extra)
	#print(vertices_raw + vertices_extra)
	vertices = format_vertices(vertices_raw + vertices_extra)
	print(vertices, file=sys.stderr)
	path = a_star(nodes, vertices, beginning, end, position)
	print("path: ", path, file=sys.stderr)
	linear_done = False
	
	voice_data = ""

	
	linear_less_than_margin = vertices[path[0]][path[1]] <= linear_margin
	if(linear_less_than_margin):
		i = 1
	else:
		i = 0
	if(not linear_less_than_margin or len(path) > 2):
		print_data = '"linear":"Walk for ' + str(round(float(vertices[path[i]][path[i+1]]),1)) + ' meters"'
		voice_data = print_data
#		print(print_data)
	else:
		linear_done = True
		
	
	if(linear_less_than_margin and len(path) == 2):
		i -= 1
		
	deg_diff = deg_to_rotate(position, path, start_p, yaw, i+1)
	
	if(abs(deg_diff) > angle_margin and not linear_done):
		print_data = '"angular":"Rotate for ' + str(int(abs(deg_diff))) + ' degrees '
		if(deg_diff > 0):
			print_data += 'clockwise"'
		else:
			print_data += 'anticlockwise"'
		if(voice_data):
			voice_data += ', '
		voice_data = print_data
#		print(print_data)

	elif(linear_done):
		print_data = '"end":"You already arrived to your destination"'
		voice_data = print_data
#		print(print_data)
		
	voice_data = '{' + voice_data + '}'
	return voice_data
		
#loc_instructions(Point(0,0), 193, Point(9,5))

