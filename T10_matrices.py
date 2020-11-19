"""Tema 10: Să se realizeze un program care:
a) să calculeze suma și produsul a două matrice pătratice de ordin n;
b) să calculeze urma unei matrice pătratice;
c) să verifice dacă o matrice este simetrică sau antisimetrică
(calculând transpusa acesteia).

Notă: pentru afișare corectă schimbă fontul consolei în Consolas!
"""
"""specificație:
- intern, matricea este reprezentată printr-o listă de liste
- fiecare element din lista principală reprezintă un rând
- fiecare element din listele secundare (elemente în lista principală)
	reprezintă o coloană
ex.
	matrice linie: (1 2 3) => [[1, 2, 3]]
	matrice coloană:
	(1
	 2		=> [[1], [2], [3]]
	 3)
	matrice rectangulară:
	(1 3 4
	 1 0 1) => [[1, 3, 4], [1, 0 ,1]]

* față de versiunea anterioară, nu mai există ambiguitatea de reprezentare din cazul matricei linie
(înainte: [1, 2, 3], acum: [[1, 2, 3]])
"""


def add_matrices(a, b):
	"""
	Adună două matrice reprezentate ca liste
	 param a: prima matrice
	 param b: a doua matrice
	 return: matricea sumă
	 rtype: list
	"""
	#algoritm: creează prin list comprehension o listă în care fiecare
	# element este suma elementelor corespunzătoare din matricile din input
	#verifică dacă matricele sunt de același ordin
	if (len(a) != len(b)) or (len(a[0]) != len(b[0])):
		return

	return [[a[row][column] + b[row][column]
	         for column in range(len(a[0]))]
	        for row in range(len(a))]


def multiply_matrices(a, b):
	"""
	Înmulțește două matrice compatibile (cu ordine de tipul A(n x m) și B(m x p))
	 param a: prima matrice
	 param b: a doua matrice
	 return: matricea produs
	 rtype: list
	"""
	#procedeul general se poate aplica și cazurilor particulare (ex. matrice pătratice)
	#algoritm: v. https://en.wikipedia.org/wiki/Matrix_multiplication_algorithm
	# - pentru a fi posibilă operația trebuie ca numărul de coloane din
	#  prima matrice să fie egal cu numărul de rânduri din a doua matrice
	#  -> A(n x m), B(m x p), rezultatul va fi M(n x p)
	# - generează o matrice nulă de ordin n x p, în care se va stoca rezultatul
	# - fiecare element al rezultatului se obține ca sumă a produselor de tip
	# 	a[i][j] * b[j][i]

	#calculează ordinul fiecărei matrice din input
	a_rows = len(a)
	a_columns = len(a[0])
	b_rows = len(a)
	b_columns = len(b[0])

	#verifică dacă matricele sunt compatibile
	if a_columns != b_rows:
		return

	#generează o matrice care stochează rezultatul
	product = null_matrix_rc(a_rows, b_columns)

	for i in range(a_rows):
		for j in range(b_columns):
			sum = 0
			for k in range(a_columns):
				sum += a[i][k] * b[k][j]
			product[i][j] = sum

	return product


def trace_matrix(a):
	"""
	Calculează suma elementelor din diagonala principală a unei matrice
	 param a: matricea
	 return: suma elementelor de tip a[i][i]
	 rtype: float
	"""
	#algoritm: adună toate elementele de forma a[i][i]
	trace = 0
	for i in range(len(a)):
		trace += a[i][i]

	return trace


def transpose_matrix(a):
	"""
	Calculează transpusa unei matrice
	 param a: matricea
	 return: transpusa matricei a
	 rtype: list
	"""
	#algoritm: pentru fiecare element din matrice inversează-i coordonatele
	# ex. a01 devine a10
	# v. https://en.wikipedia.org/wiki/Transpose

	return [
	    [a[column][row] for column in range(len(a))] for row in range(len(a[0]))
	]


def is_symmetric(a):
	"""
	Verifică dacă o matrice este simetrică
	 param a: matricea
	 return: este a simetrică?
	 rtype: bool
	"""
	#algoritm: (folosind transpusa) o matrice A este simetrică
	# dacă transpusa AT = A
	# v. https://en.wikipedia.org/wiki/Symmetric_matrix

	return (transpose_matrix(a) == a)


def is_antisymmetric(a):
	"""
	Verifică dacă o matrice este antisimetrică
	 param a: matricea
	 return: este a antisimetrică?
	 rtype: bool
	"""
	#algoritm: (folosind transpusa) o matrice A este antisimetrică
	# dacă transpusa AT = -A
	# v. https://en.wikipedia.org/wiki/Skew-symmetric_matrix

	return (transpose_matrix(a) == scalar_multiply_matrix(-1, a))


#utilitare
def scalar_multiply_matrix(number, a):
	"""
	Înmulțește un scalar cu o matrice; utilizată pentru a calcula
	opusul lui A prin înmulțire cu -1
	 param number: scalarul
	 param a: matricea
	 return: matricea produs cu scalar
	 rtype: list
	"""
	#algoritm: rezultatul este o matrice de același ordin cu cea din input,
	# iar fiecare element al acesteia e obținut prin înmulțirea scalarului
	# cu elementul corespunzător din matricea input

	return [[number * column for column in row] for row in a]


def null_matrix_rc(rows, columns):
	"""
	Generează o matrice nulă de ordin rows x columns
	 param rows: număr de rânduri
	 param columns: număr de coloane
	 return: matrice nulă
	 rtype: list
	"""

	return [[0 for i in range(columns)] for i in range(rows)]


def null_matrix_m(a):
	"""
	Generează o matrice nulă de ordinul celei din input
	 param a: matricea
	 return: matrice nulă
	 rtype: list
	"""
	#algoritm: iterează în input și creează o matrice de
	# același ordin, dar cu toate elementele 0

	return [[0 for i in a[0]] for i in a]


def max_elem_width(a):
	"""
	Calculează cea mai mare lungime de element dintr-o matrice; folosit
	 pentru afișare
	 param a: matricea
	 return: cea mai mare lungime de element
	 rtype: int
	"""
	max_width = 1

	for row in a:
		for element in row:
			if len(str(element)) > max_width:
				max_width = len(str(element))

	return max_width


def matrix_to_text(a):
	"""
	Transformă o listă ce reprezintă o matrice, într-un text
	ce corespunde formei convenționale a matricei
	 param a: matricea
	 return: text reprezentând matricea
	 rtype: string
	"""
	result = '\n\t'
	width = max_elem_width(a)

	for row in a:
		for i in range(len(row)):
			separator = '\t' #separator între elemente
			if i == (len(row) - 1):
				separator = '\n\t' #separator între rânduri
			#formatează lizibil: > aliniere la dreapta sau ^ centrat
			result += f'{row[i]:>{width}g}' + separator

	return result


def square_matrix_matcher(s):
	"""
	Verifică dacă un text corespunde formei acceptate pentru matrice pătratice
	 param s: text primit din input, reprezentând matricea
	 return: matricea ca listă sau False
	 rtype: list or bool
	"""
	#elimină spațiile și convertește caracterele la minuscule
	matrix_rows = s.replace(' ', '').lower().split(';')
	matrix = []
	for row in range(len(matrix_rows)):
		f_row = matrix_rows[row].split(',')
		for e in range(len(f_row)):
			try:
				f_row[e] = float(f_row[e])
			except:
				return False
		matrix.insert(row, f_row)

	for i in range(len(matrix)):
		if len(matrix[i]) != len(matrix):
			return False

	return matrix


def validate_input(s):
	"""
	Verifică dacă inputul corespunde formatului acceptat:
	matrice pătratică - ex. a, b, c; d, e, f; g, h, i:
	virgula separă elementele într-un rând (linie)
	punctul și virgula separă rândurile.
	 param s: text primit din input, reprezentând matricea
	 return: matricea ca listă în formatul [[a, b, c], [d, e ,f], [g, h, i]]
	 rtype: list
	"""

	while True:
		matrix = square_matrix_matcher(s)
		if matrix:
			return matrix
		else:
			print("Trebuie să scrii matricea în forma acceptată!")
			s = input("Mai încearcă: ")


def display_results():
	"""
	Afișează cerințele, inputul și rezultatul
	"""

	#cerința a)
	print(
	    "\na) să se calculeze suma și produsul a două matrice pătratice de ordin n\n"
	)
	print("Scrie două matrice pătratice de același ordin:")
	while True:
		a = validate_input(input("\nA = "))
		b = validate_input(input("B = "))
		#matricele pătratice pot fi adunate sau înmulțite doar dacă au același rang
		if len(a) == len(b):
			print("\nA = " + matrix_to_text(a))
			print("B = " + matrix_to_text(b) + "\n-------------")
			print("A + B = " + matrix_to_text(add_matrices(a, b)))
			print("A * B = " + matrix_to_text(multiply_matrices(a, b)))
			break
		else:
			print("Matricele introduse nu sunt de același ordin! Mai încearcă: ")
			continue

	#cerința b)
	print("\nb) să se calculeze urma unei matrice pătratice\n")
	print("Scrie o matrice pătratică:")
	a = validate_input(input("\nA = "))
	print("\nA = " + matrix_to_text(a) + "\n-------------")
	trace = trace_matrix(a)
	print(f'urma(A) = {trace:g}')

	#cerința c)
	print("\nc) să se verifice dacă o matrice este simetrică sau antisimetrică")
	print("Scrie o matrice pătratică:")
	a = validate_input(input("\nA = "))
	print("\nA = " + matrix_to_text(a) + "\n-------------")
	symmetry = "A\u1d40 \u2260 A, deci A nu este simetrică"
	antisymmetry = "A\u1d40 \u2260 -A, deci A nu este antisimetrică"
	if is_symmetric(a):
		symmetry = "A\u1d40 = A, deci A este simetrică"
	if is_antisymmetric(a):
		antisymmetry = "A\u1d40 = -A, deci A este antisimetrică"
	#\u1d40 (indice T) se afișează corect cu fontul Consolas în consolă
	print("transpusa(A) = A\u1d40 = " + matrix_to_text(transpose_matrix(a)))
	print("-A = " + matrix_to_text(scalar_multiply_matrix(-1, a)))
	print(f"Pentru simetrie trebuie ca A\u1d40 = A:\n\t{symmetry}.")
	print(f"\nPentru antisimetrie trebuie ca A\u1d40 = -A:\n\t{antisymmetry}.")
	#...
	input("\nApasă ENTER pentru a închide aplicația...")


#aplicația
print(__doc__) #afișează enunțul temei
example = """Forma acceptată pentru matricele cerute mai jos este:

	a, b, c; d, e, f; g, h, i

	- toate elementele sunt scrise pe aceeași linie
	- separatorul pentru elementele unui rând este virgula
	- separatorul pentru rânduri este punctul și virgula

		ex. -2, 1; 2, 0 reprezintă matricea
		-2	1
		 2	0
		"""
print(example)
display_results()