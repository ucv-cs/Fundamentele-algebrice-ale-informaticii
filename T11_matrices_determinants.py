"""Tema 11: Să se realizeze un program care:
a) calculează un determinant de ordin n = {2, 3, 4, 5} și
testează dacă o matrice pătratică cu elemente numere reale, de
ordin n = {2, 3, 4, 5}, este inversabilă sau nu;
b) rezolvă un sistem cramerian cu matricea sistemului pătratică,
de ordin n = {2, 3, 4, 5}.\n"""
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
import copy, re


def matrix_determinant(a):
	"""
	Calculează determinantul unei matrice pătratice folosind dezvoltarea
	după prima coloană (Laplace expansion https://en.wikipedia.org/wiki/Laplace_expansion )
	 param a: matricea
	 result: determinantul matricei
	 rtype: float
	"""
	#algoritm:
	# - pentru elementele din primul rând (se putea alege orice rând sau coloană)
	# din matrice, calculează minorul (submatricea rezultată din eliminarea rândului
	# și coloanei elementului) - v. reduce_row_column(a, r, c);
	# - calculează complementul algebric al elementului:
	# 		a[0][i], dacă 0+i este par
	# 		-a[0][i], dacă 0+i este impar
	# - determinantul se va calcula prin recurență, reapelând funcția cu
	# matrice de ordin descrescător, până la 2 (care se calculează ușor):
	# det = det + complement_0i * matrix_determinant(minor_0i)
	# v. https://www.blogcyberini.com/2017/09/teorema-de-laplace-em-c.html

	order_a = len(a)
	determinant = 0

	if order_a == 1:
		return a[0][0]
	elif order_a == 2:
		return a[0][0] * a[1][1] - a[1][0] * a[0][1]
	else:
		#calculează dezvoltarea determinantului după rândul 0
		for i in range(len(a[0])):
			if a[0][i] != 0:
				#minorul lui a[0][i]
				minor = reduce_row_column(a, 0, i)
				#complementul algebric al lui a[0][i]
				complement = a[0][i] if (i % 2) == 0 else -a[0][i]
				#determinantul calculat prin recurență
				determinant = determinant + complement * matrix_determinant(minor)

	return determinant


def scalar_multiply_matrix(number, a):
	"""
	Înmulțește un scalar cu o matrice
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


def reduce_row_column(a, row, column):
	"""
	Generează o submatrice prin eliminarea unui rând și a unei coloane
	ale căror indexuri sunt date
	 param a: matricea
	 row: indexul rândului de eliminat
	 column: indexul coloanei de eliminat
	 return: matricea modificată
	 rtype: list
	"""
	#clonează matricea inițială
	reduced = copy.deepcopy(a)

	#elimină coloana cu indexul specificat din toate rândurile
	for i in range(len(a)):
		for j in range(len(a[0])):
			if j == column:
				reduced[i].pop(j)

	#elimină rândul cu indexul specificat
	for i in range(len(reduced)):
		if i == row:
			reduced.pop(i)

	return reduced


def inverse_matrix(a):
	"""
	Calculează inversa unei matrice pătratice
	 param a: matricea
	 return: inversa matricei a
	 rtype: list
	"""
	#algoritm: inversa matricei este produsul dintre scalarul 1/det(a)
	# și matricea adjunctă
	# v. https://en.wikipedia.org/wiki/Invertible_matrix

	return scalar_multiply_matrix(1 / matrix_determinant(a), adjoint_matrix(a))


def adjoint_matrix(a):
	"""
	Calculează adjuncta (adjugata) unei matrice pătratice
	 param a: matricea
	 return: adjuncta matricei a
	 rtype: list
	"""
	#algoritm: adjuncta matricei este transpusa matricei cofactorilor
	# v. https://en.wikipedia.org/wiki/Adjugate_matrix

	#rezultatul
	cofactors = null_matrix_rc(len(a), len(a[0]))

	#matricea cofactorilor
	for i in range(len(a)):
		for j in range(len(a[0])):
			minor_ij = reduce_row_column(a, i, j)
			factor_ij = 1 if ((i + j) % 2) == 0 else -1
			cofactors[i][j] = factor_ij * matrix_determinant(minor_ij)

	#transpusa matricei cofactorilor
	return transpose_matrix(cofactors)


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


def column_modifier(a, b, i):
	"""
	Înlocuiește în matricea a, coloana i, cu matricea coloană b
	 param a: matrice pătratică de ordin n
	 param b: matrice coloană de ordin n x n
	 param i: indexul coloanei de modificat (>= 0)
	 return: matricea modificată
	 rtype: list
	"""
	#clonează matricea inițială
	modified = copy.deepcopy(a)

	#înlocuiește elementul din fiecare coloană cu indexul specificat,
	# cu elementul corepunzător din b
	for row in range(len(modified)):
		for column in range(len(modified[0])):
			if column == i:
				modified[row][column] = b[row][0]

	return modified


def cramerian_solver(A, b):
	"""
	Rezolvă un sistem de n ecuații cu n necunoscute, folosind regula lui Cramer
	 param A: matrice pătratică de ordin <= 5
	 param b: matrice coloană
	 return: matrice coloană cu soluțiile sistemului
	 rtype: list
	"""
	#varianta 1: folosind regula lui Cramer
	#algoritm: pentru un sistem de tip Ax = b, soluțiile au forma
	# xn = det(Anb) / det(A), unde Anb este matricea A în care
	# coloana n este înlocuită cu matricea coloană b
	# v. https://mathcracker.com/cramers-rule

	det_A = matrix_determinant(A)

	if det_A == 0:
		return "Sistemul de ecuații este incompatibil"

	solutions = null_matrix_rc(len(A), 1)

	for i in range(len(A[0])):
		modified_A = column_modifier(A, b, i)
		det_mA = matrix_determinant(modified_A)
		solutions[i][0] = det_mA / det_A

	#varianta 2: folosind inversa matricei coeficienților
	#algoritm: în sistemul de tip Ax = b se înmulțesc ambii membrii cu A^-1 (inversa lui A)
	# => inv(A)*A*x = inv(A)*b
	# - inv(A)*A este o matrice identitate de ordinul lui A (ex. [1, 0; 0, 1]), care
	# înmulțită cu vectorul x, va lăsa x neschimbat
	# - în membrul drept se va calcula produsul matricelor inv(A) și b
	# det_A = matrix_determinant(A)

	# if det_A == 0:
	# 	return "Sistemul de ecuații este incompatibil"

	# solutions = multiply_matrices(inverse_matrix(A), b)

	return solutions


def sys_eq_converter(s, unknowns):
	"""
	Convertește o listă compusă, conținând reprezentarea ecuațiilor
	unui sistem, într-o listă de forma: [matrice, vector]
	 param a: lista compusă din reprezentarea ecuațiilor din input
	 param unknowns: lista cu necunoscute
	 return: listă conținând matricea pătratică a sistemului și vectorul
	 	format din membrul drept al ecuațiilor
	 rtype: list
	"""
	#normalizează dicționarele, prin adăugarea perechilor cheie-valoare lipsă
	for e in s:
		for u in unknowns:
			if u not in e[0]:
				e[0][u] = 0

	#sortează ascendent necunoscutele
	unknowns = sorted(unknowns)

	#extrage matricea coeficienților și vectorul drept
	matrix = []
	vector = []
	for e in s:
		row = []
		for k in unknowns:
			row.append(e[0][k])
		matrix.append(row)
		vector.append([e[1]])

	return [matrix, vector]


def sys_eq_to_text(s, unknowns):
	"""
	Transformă o listă ce reprezintă un sistem de ecuații, într-un text
	ce corespunde formei convenționale a sistemului
	 param s: sistemul de ecuații ca listă
	 param unknowns: lista cu necunoscute
	 return: text reprezentând sistemul
	 rtype: string
	"""
	result = '\n'
	for i in range(len(s[0])):
		result += '\t'
		for j in range(len(s[0][i])):
			sign = ''
			x = unknowns[j]
			coefficient = s[0][i][j]

			#cazuri particulare
			#nu afișa termenul cu coeficient 0
			if coefficient == 0:
				continue
			elif coefficient > 0:
				sign = '+'

			#nu afișa coeficientul 1 sau -1
			if coefficient == 1:
				coefficient = ''
			if coefficient == -1:
				coefficient = '-'

			#nu afișa semnul + la început de linie
			if (j == 0) and (sign == '+'):
				sign = ''
			try:
				#dacă e convertibil la float, formatează stringul
				coefficient = f'{float(coefficient):g}'
			except:
				pass
			result += f'{sign}{coefficient}{x}'

		#aliniază ecuația
		result = f'{result:>{len(str(result))}} = {s[1][i][0]:>{len(str(s[1][i][0]))}g}\n'

		#adaugă spații doar în jurul semnelor + - de legătură
		result = re.sub(r'([a-z])([-\+])', r'\1 \2 ', result)

	return result


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


def square_matrix_matcher(s, data=None):
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
		#verifică dacă matricea este pătratică și de ordin între 2 și 5
		if len(matrix[i]) != len(matrix):
			print(
			    f"Matricea introdusă nu este pătratică (are ordinul: {len(matrix)} x {len(matrix[i])})!"
			)
			return False
		if len(matrix) not in range(2, 6):
			print(
			    f"Matricea introdusă are ordinul {len(matrix)} (trebuie să fie între 2 și 5)!"
			)
			return False

	return matrix


def unknowns_matcher(s, data=None):
	"""
	Verifică dacă un text conține un șir de litere distincte (între
	2 și 5), separate prin virgulă
	 params s: textul primit din input
	 return: lista de litere sau False
	 rtype: list or bool
	"""
	#elimină spațiile și convertește caracterele la minuscule
	unknowns = s.replace(' ', '').lower().split(',')
	if len(unknowns) not in range(2, 6):
		print(
		    "Trebuie să scrii între 2 și 5 litere diferite, separate prin virgulă!")
		return False

	for letter in unknowns:
		if (not letter.isalpha()) or (len(letter) != 1) or (len(set(unknowns)) !=
		                                                    len(unknowns)):
			print(
			    "Trebuie să scrii doar litere diferite, separate prin virgulă (ex. x,y,z)!"
			)
			return False

	return unknowns


def equation_matcher(s, unknowns):
	"""
	Verifică dacă un text corespunde formei acceptate pentru ecuații
	 param s: text primit din input, reprezentând ecuația
	 return: matricea augmentată ca listă sau False
	 rtype: list or bool
	"""
	#elimină spațiile și convertește caracterele la minuscule
	members = s.replace(' ', '').lower().split('=')
	monomials = members[0].replace('-', '+-').split('+')
	if len(members) != 2:
		print("Ecuația trebuie să aibă doi membri!")
		return False

	#validează membrul drept al ecuației
	try:
		right_member = int(members[1])
	except:
		print("Membrul drept al ecuației trebuie să fie un număr întreg!")
		return False

	p = dict() #rezultatul

	#configurează o expresie regulată pentru a testa forma inputului
	#teste: https://regex101.com/
	pattern = r"^([-\+]?)(\d*\.*?\d*)([a-zA-Z]?)$"

	#iterează lista și află pozițiile elementelor fiecărui monom
	#adaugă la un dicționar final datele numerice
	for m in monomials:
		term = re.match(pattern, m)

		#dacă monomul curent nu are formatul acceptat, reia funcția;
		# inclusiv dacă "monomul" e format doar dintr-un semn
		if (term is None) or (m == '+') or (m == '-'):
			return False

		#alocă grupurile în variabile denumite mai inteligibil
		t = (sign, coefficient, x) = (term.group(1), term.group(2), term.group(3))

		#ignoră elementul gol, pentru că patternul permite match
		if t == ('', '', ''):
			continue

		#verifică dacă litera din ecuație există în grupul declarat
		if x not in unknowns:
			print(f"Necunoscuta {x} nu se află în lista declarată: {unknowns}")
			return False

		#cazuri particulare
		#coeficientul 0 transformă tot monomul în 0 și poate fi ignorat
		if coefficient == 0:
			continue

		#coeficientul nespecificat este 1 sau -1, în funcție de semn
		if coefficient == '':
			coefficient = float(f'{sign}1')
			sign = '' #evită duplicarea semnului

		#coeficientul nu poate fi convertit în float
		try:
			coefficient = float(f'{sign}{coefficient}')
		except:
			print("Un coeficient nu este scris în forma acceptată!")
			return False

		#dicționar temporar utilizat pentru acumulare
		d = {x: coefficient}

		#optimizare
		if p == {}:
			p = d
		else:
			for x, coefficient in d.items():
				if x in p.keys():
					#dacă necunoscuta este comună, adună coeficienții în rezultat
					p[x] += d[x]
				else:
					#dacă necunoscuta există doar în al doilea dicționar, adaugă-l
					# la rezultat și asociază-l cu coeficientul corespunzător
					p[x] = d[x]

	return [p, right_member]


def validate_input(s, matcher_callback, data=None):
	"""
	Verifică dacă inputul corespunde formatului acceptat conform funcției
	matcher_callback
	 param s: text primit din input
	 param matcher_callback: nume de funcție folosită la validare
	 return: obiectul rezultat din matcher_callback
	"""
	while True:
		output = matcher_callback(s, data)
		if output:
			return output
		else:
			print("Trebuie să scrii inputul în forma acceptată!")
			s = input("Mai încearcă: ")


def display_results():
	"""
	Afișează cerințele, inputul și rezultatul
	"""

	#cerința a)
	print("""\na) calculează un determinant de ordin n = {2, 3, 4, 5} și
		testează dacă o matrice pătratică cu elemente numere reale, de
		ordin n = {2, 3, 4, 5}, este inversabilă sau nu\n""")
	print("Scrie o matrice pătratică:")
	a = validate_input(input("\nA = "), square_matrix_matcher)

	det_a_n = matrix_determinant(a)
	det_a = f'{det_a_n:g}'

	print("\nA = " + matrix_to_text(a) + "\n-------------")
	invertible = "|A| = 0, deci matricea nu este inversabilă.\n"
	inverse_a = ""
	if det_a_n != 0:
		inverse_a_n = inverse_matrix(a)
		inverse_a = matrix_to_text(inverse_a_n)
		invertible = f"|A| \u2260 0, deci matricea este inversabilă. Inversa lui A este:\nA\u207b\u00b9 = {inverse_a}"
		invertible += f"\nTest al inversei:\nAA\u207b\u00b9 = {matrix_to_text(multiply_matrices(a, inverse_a_n))}"

	print(f'Determinantul matricei este: |A| = {det_a}\n\t{invertible}')

	#cerința b)
	print("""\nb) rezolvă un sistem cramerian cu matricea sistemului pătratică,
		de ordin n = {2, 3, 4, 5}.

		Formatul acceptat pentru fiecare ecuație este: ax + by + cz + dt + eu = f
			ex. 2x - 3y + z = 3
		""")
	print(
	    "Scrie între 2 și 5 necunoscute (câte o literă pentru fiecare), separate prin virgulă: "
	)
	unknowns = validate_input(input(), unknowns_matcher)
	unknowns = sorted(unknowns)

	print(
	    f"\nScrie {len(unknowns)} ecuații cu {len(unknowns)} necunoscute din seria specificată, în formatul acceptat:"
	)

	#declară numărul de ordine al ecuației și o listă pentru sistemul de ecuații
	n = 0
	sys_eq = []

	while True:
		n += 1
		#validează forma fiecărei ecuații, iar apoi adaugă ecuația la sistem
		equation = validate_input(
		    input(f"ecuația {n}: "), equation_matcher, unknowns)
		sys_eq.append(equation)

		#întrerupe loopul când numărul de necunoscute este egal cu cel de ecuații
		if n == len(unknowns):
			break

	#extrage matricea sistemului de ecuații
	sys_matrix = sys_eq_converter(sys_eq, unknowns)

	#afișează sistemul de ecuații
	print(sys_eq_to_text(sys_matrix, unknowns))

	#rezolvă sistemul, adaugă soluția într-o listă și afișează
	print('\nMatricea coeficienților sistemului este:\nA = ')
	print(matrix_to_text(sys_matrix[0]))
	det_a = matrix_determinant(sys_matrix[0])
	print(f'\nDeterminantul este: |A| = {det_a:g}')

	if det_a != 0:
		sys_solution = cramerian_solver(sys_matrix[0], sys_matrix[1])
		print('\nSoluția sistemului este:')
		for u in range(len(unknowns)):
			print(f'\t{unknowns[u]} = {sys_solution[u][0]:g}')
		print(f'\nTest:\n\tA: {matrix_to_text(sys_matrix[0])}\n\tX')
		print(f'\n\tx: {matrix_to_text(sys_solution)}\n\t=')
		print(
		    f'\n\tb: {matrix_to_text(multiply_matrices(sys_matrix[0], sys_solution))}'
		)
	else:
		print('\nÎntrucât |A| = 0, sistemul este incompatibil.')

	#...
	input("\nApasă ENTER pentru a închide aplicația...")


#aplicația
print(__doc__) #afișează enunțul temei
example = """Forma acceptată pentru matricea cerută mai jos este:

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