"""Tema 6: Realizați tabela operației de adunare respectiv de înmulțire
în inelul Zn, cu n > 1. Determinați toate elementele inversabile și
nilpotente ale inelului, precum și divizorii lui zero.
"""
import copy


def addition_Zn_table(n):
	"""
	Generează o matrice reprezentând adunarea claselor de resturi Zn
	 param n: număr natural
	 return: matricea tabelei adunării
	 rtype: list
	"""
	elements = list(range(n)) #listă cu numerele naturale de la 0 la n-1
	return [[(i + j) % n for i in elements] for j in elements]


def multiplication_Zn_table(n):
	"""
	Generează o matrice reprezentând înmulțirea claselor de resturi Zn
	 param n: număr natural
	 return: matricea tabelei înmulțirii
	 rtype: list
	"""
	elements = list(range(n))
	return [[(i * j) % n for i in elements] for j in elements]


def find_reversibles(matrix):
	"""
	Găsește elementele inversabile ale inelului (pentru care a*b = 1)
	 param matrix: tabla unei operații, sub formă de matrice
	 return: list
	 rtype: list
	"""
	return set(
	    sorted([
	        i for i in range(len(matrix)) for j in range(len(matrix[0]))
	        if matrix[i][j] == 1
	    ]))


def find_zeros_divisors(matrix):
	"""
	Găsește divizorii lui zero (pentru care a*b = 0)
	 param matrix: tabla unei operații, sub formă de matrice
	 return: list
	 rtype: list
	"""
	#adaugă if i != 0 if j != 0 pentru divizorii non-triviali ai lui 0
	return set(
	    sorted([
	        i for i in range(len(matrix)) for j in range(len(matrix[0]))
	        if matrix[i][j] == 0
	    ]))


def find_nilpotents(matrix):
	"""
	Găsește elementele nilpotente ale inelului (pentru care a^n = 0)
	 param matrix: tabla unei operații, sub formă de matrice
	 return: list
	 rtype: list
	"""
	return set(
	    sorted([
	        i for i in range(len(matrix)) for j in range(len(matrix[0])) if i == j
	        if matrix[i][j] == 0
	    ]))


def display_list(a_list):
	"""
	Afișează o listă ordonată crescător folosind acolade.
	 param a_list: lista sau setul de afișat
	 rtype: str
	"""
	return str(sorted(list(a_list))).replace('[', '{').replace(']', '}')


def display_table(grid, operator):
	"""
	Afișează tabela pentru matricea și operația dată
	 param grid: lista de afișat
	 param operator: operatorul care va fi afișat în colțul tabelei
	"""
	matrix = copy.deepcopy(grid)

	#găsește numărul cel mai mare dintr-un rând al matricei
	n = max(matrix[len(matrix) - 1])
	elements = list(range(len(matrix))) #cap de tabel
	h_space = 2 #spațiul orizontal dintre elemente în tabel
	width = len(str(n)) + h_space

	#include un rând pentru linia din tabel
	table_header = [[f'{operator:>{width}} |'] + [i for i in elements]] * 2
	for row in range(len(matrix)):
		matrix[row].insert(0, f'{elements[row]:>{width}} |')
	table = table_header + matrix

	result = '\n\t'
	empty = ''

	for i in range(len(table)):
		for j in range(len(table[i])):
			#separator între elemente și rânduri
			separator = '\n\t' if j == (len(table[i]) - 1) else ''
			if i == 0:
				element = f'{table[0][j]:>{width}}'
				result += (
				    element + separator + ('  ' if j == (len(table[i]) - 1) else ''))
			elif i == 1: #linia de separare
				result += f'{empty:->{width}}' + separator
			else: #conținutul tabelului
				result += f'{table[i][j]:>{width}}' + separator
	print(result)


def to_subscript(e):
	"""
	Convertește un indice numeric în subscript
	(în consolă, numai cu fonturi care suportă UTF-8,
	ex. Consolas, nu Lucida Console)
	 param e: string reprezentând un număr
	 return: string cu numărul subscript
	 rtype: string
	"""
	#transformă inputul numeric în string, apoi stringul
	# într-o listă conținând ca element fiecare caracter
	s = list(str(e))
	e = '' #rezultatul

	#iterează în listă și înlocuiește fiecare caracter numeric
	# cu forma lui de indice (subscript)
	for c in s:
		if c in [str(i) for i in range(10)]:
			e += chr(int(f'832{c}')) #folosește codepointul (v. HTML)

	return e


def positive_matcher(string):
	"""
	Verifică dacă stringul introdus este un număr natural mai mare decât 1
	 param string: input
	 return: int sau False
	 rtype: int sau False
	"""
	result = False
	try:
		number = int(string)
		result = number if number > 1 else result
	except:
		pass
	return result


def validate_input(string):
	"""
	Verifică dacă inputul este valid.
	 param string: input
	 return: numărul rezultat în urma validării
	 rtype: int
	"""
	while True:
		output = positive_matcher(string)
		if output:
			return output
		else:
			print("Trebuie să scrii un număr natural mai mare decât 1!")
			string = input("Mai încearcă: ")


def display_results():
	"""
	Afișează cerințele, inputul și rezultatul
	"""
	n = validate_input(input("Scrie numărul n > 1 (de la Zn): "))
	matrix = addition_Zn_table(n)
	print(f"\n\tAdunarea în Z{to_subscript(n)}")
	display_table(matrix, '+')

	matrix = multiplication_Zn_table(n)
	print(f"\n\tÎnmulțirea în Z{to_subscript(n)}")
	display_table(matrix, '*')

	print(
	    f"Elementele inversabile sunt: {display_list(find_reversibles(matrix))}")
	divisors = display_list(find_zeros_divisors(matrix))
	if divisors == set():
		divisors = '{}'
	print(f"Divizorii lui 0 sunt: {divisors}")
	nilpotents = display_list(find_nilpotents(matrix))
	if nilpotents == set():
		nilpotents = '{}'
	print(f"Elementele nilpotente sunt: {nilpotents}\n")


#aplicația
print(__doc__) #afișează enunțul temei
while True:
	display_results()