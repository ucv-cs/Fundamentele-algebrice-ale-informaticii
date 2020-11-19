"""Tema 4: Pentru n ≥ 2, număr natural, realizați un program care:
a) să precizeze dacă n este prim sau nu. Dacă este compus, să se afișeze
toți divizorii lui n;
b) să scrie descompunerea canonică în factori primi a lui n;
c) să afișeze tabelele operațiilor \u039b și V definite pe mulțimea Dn a
divizorilor lui n aflată la a);
d) să testeze dacă n este liber de pătrate (este diferit de 1 și nu se divide
cu pătratul unui număr prim). Dacă da, să se afișeze complementele elementelor
din Dn.

Indicație: Dacă n are cel puțin un divizor prim ≤ \u221a\u0305n, atunci n este
compus. Altfel, n este prim.
Pentru d1, d2 in Dn: d1 \u039b d2 = c.m.m.d.c.{d1,d2}, d1 V d2 = c.m.m.m.c.{d1,d2}
și, dacă n este liber de pătrate, complementul oricărui d in Dn este d'=n/d.
"""
import copy


def or_Dn_table(n):
	"""
	Generează o matrice reprezentând \u039b în Dn
	 param n: număr natural
	 return: matricea tabelei \u039b
	 rtype: list
	"""
	elements = get_divisors(n)
	return [[gcd(i, j) for i in elements] for j in elements]


def and_Dn_table(n):
	"""
	Generează o matrice reprezentând V în Dn
	 param n: număr natural
	 return: matricea tabelei V
	 rtype: list
	"""
	elements = get_divisors(n)
	return [[lcm(i, j) for i in elements] for j in elements]


def gcd(a, b):
	"""
	Calculează c.m.m.d.c. pentru două numere naturale nenule
	 param a: număr natural nenul
	 param b: număr natural nenul
	 return: număr reprezentând c.m.m.d.c.(a, b)
	 rtype: int
	"""
	#algoritmul lui Euclid:
	# "https://en.wikipedia.org/wiki/Greatest_common_divisor"

	#inversează termenii pentru a ca primul să fie întotdeauna
	# cel mai mare
	if a < b:
		(a, b) = (b, a)

	#varianta 1: folosind o 'traducere' a algoritmului lui Euclid
	while ((a % b) != 0):
		rest = a % b
		a = b
		b = rest

	#varianta 2: v. https://djangocentral.com/gcd-using-euclid-algorithm-in-python/
	#	while (a % b != 0):
	#		(a, b) = (b, a % b)

	return b


def lcm(a, b):
	"""
	Calculează c.m.m.m.c. pentru două numere naturale nenule
	 param a: număr natural nenul
	 param b: număr natural nenul
	 return: număr reprezentând c.m.m.m.c.(a, b)
	 rtype: int
	"""
	#algoritm: folosim relația a * b = c.m.m.d.c.(a, b) *
	# c.m.m.m.c.(a, b) => c.m.m.m.c.(a, b) = a * b / c.m.m.d.c.(a, b)
	return int(a * b / gcd(a, b))


def get_divisors(n):
	"""
	Găsește divizorii unui număr
	 param n: număr natural
	 return: list
	 rtype: list
	"""

	return sorted([i for i in range(1, n + 1) if n % i == 0])


def decompose(number):
	"""
	Descompune un număr în factori primi și returnează lista lor
	 param number: numărul de descompus
	 return: lista factorilor primi
	 rtype: list
	"""
	#algoritm: v. https://en.wikipedia.org/wiki/Trial_division
	result = []

	#dacă restul împărțirii numărului la 2 este 0, numărul este
	# divizibil cu 2, deci adaugă la listă 2 ca divizor și reduce
	# numărul prin împărțire la 2 (repetând verificarea inițială)
	while number % 2 == 0:
		result.append(2)
		number /= 2

	#folosind proprietatea din indicație (v. divizor prim ≤ sqrt(n))
	# verifică dacă un factor începând cu 3 (incrementat cu 2, pentru
	# a obține mereu un număr impar) este divizibil cu numărul redus
	# anterior, adaugă divizorul la rezultat și reduce numărul prin
	# împărțire la factor
	factor = 3
	while factor * factor <= number:
		if number % factor == 0:
			result.append(int(factor))
			number /= factor
		else:
			factor += 2

	if number != 1:
		result.append(int(number))

	return result


def display_factors(factors):
	"""
	Afișează factorii primi în formă canonică
	 param factors: lista de factori primi
	 return: text cu forma canonică
	 rtype: string
	"""
	factor_dict = dict() #{baza: exponent}
	for i in range(len(factors)):
		base = factors[i]
		if base not in factor_dict:
			exponent = 0
			for j in range(len(factors)):
				if base == factors[j]:
					exponent += 1
			factor_dict[base] = exponent

	result = []
	for i in sorted(factor_dict.keys()):
		exp = to_superscript(factor_dict[i]) if factor_dict[i] > 1 else ''
		result += [f'{i}{exp}']

	return ' * '.join(result)


def is_squarefree(number):
	"""
	Verifică dacă un număr este liber de pătrate
	 param number: numărul din input
	 return: boolean
	 rtype: bool
	"""
	#algoritm: descompune numărul în factori primi
	# - generează un dicționar de tip {baza: exponent}
	# - returnează False (= nu e liber de pătrate) la prima
	# incidență a unui exponent 2, altfel returnează True
	factors = decompose(number)
	factor_dict = dict() #{baza: exponent}

	for i in range(len(factors)):
		base = factors[i]
		if base not in factor_dict:
			exponent = 0
			for j in range(len(factors)):
				if base == factors[j]:
					exponent += 1
				if exponent == 2:
					return False
			factor_dict[base] = exponent

	return True


def display_list(a_list):
	"""
	Afișează o listă folosind acolade.
	 param a_list: lista sau setul de afișat
	 rtype: str
	"""
	return str(list(a_list)).replace('[', '{').replace(']', '}')


def display_table(grid, operator):
	"""
	Afișează tabela pentru matricea și operația dată
	 param grid: lista de afișat
	 param operator: operatorul care va fi afișat în colțul tabelei
	"""
	matrix = copy.deepcopy(grid)

	#găsește numărul cel mai mare dintr-un rând al matricei
	n = max(matrix[len(matrix) - 1])
	elements = get_divisors(n) #cap de tabel
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


def to_superscript(e):
	"""
	Convertește un indice numeric în superscript
	(în consolă, numai cu fonturi care suportă UTF-8,
	ex. Consolas, nu Lucida Console)
	 param e: string reprezentând un număr
	 return: string cu numărul superscript
	 rtype: string
	"""
	#transformă inputul numeric în string, apoi stringul
	# într-o listă conținând ca element fiecare caracter
	s = list(str(e))
	e = '' #rezultatul

	#iterează în listă și înlocuiește fiecare caracter numeric
	# cu forma lui de exponent (superscript)
	for c in s:
		if c == '0':
			e += '\u2070'
		elif c == '1':
			e += '\u00b9'
		elif c == '2':
			e += '\u00b2'
		elif c == '3':
			e += '\u00b3'
		elif c == '4':
			e += '\u2074'
		elif c == '5':
			e += '\u2075'
		elif c == '6':
			e += '\u2076'
		elif c == '7':
			e += '\u2077'
		elif c == '8':
			e += '\u2078'
		elif c == '9':
			e += '\u2079'

	return e


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
	Afișează inputul și rezultatul
	"""
	n = validate_input(input("Scrie numărul n ≥ 2: "))
	show_composite_operations = True
	divider = '\n----------------------\n'

	#a) să precizeze dacă n este prim sau nu. Dacă este compus, să se
	#  afișeze toți divizorii lui n
	factors = decompose(n)
	if len(factors) == 1:
		print(f"a) {n} este prim.\n")
		show_composite_operations = False
	else:
		divisors = display_list(get_divisors(n))
		print(f"a) {n} este compus.\n\tDivizorii lui {n} sunt: {divisors}\n")

	if show_composite_operations:
		#b) să scrie descompunerea canonică în factori primi a lui n
		factors_string = display_factors(factors)
		print(
		    f"b) Descompunerea canonică în factori primi este:\n\t{n} = {factors_string}\n\t"
		)

		#c) să afișeze tabelele operațiilor \u039b și V definite pe
		#  mulțimea Dn a divizorilor lui n aflată la a)
		print("c) ")
		matrix = or_Dn_table(n)
		print(f"\n\t\t\u039b în D{to_subscript(n)}")
		display_table(matrix, '\u039b')

		matrix = and_Dn_table(n)
		print(f"\n\t\tV în D{to_subscript(n)}")
		display_table(matrix, 'V')

		#d) să testeze dacă n este liber de pătrate (este diferit de 1 și
		#  nu se divide cu pătratul unui număr prim). Dacă da, să se
		#  afișeze complementele elementelor din Dn
		test = is_squarefree(n)
		print(f"d) {n}{' ' if test else ' nu '}este liber de pătrate.")
		if test:
			complements = display_list([n // d for d in get_divisors(n)])
			print(f'\tComplementele divizorilor sunt: {complements}')
		print(divider)


#aplicația
print(__doc__) #afișează enunțul temei
while True:
	display_results()