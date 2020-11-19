"""Tema 8: Să se realizeze un program care calculează suma
și produsul a două polinoame.

Notă: pentru afișare corectă schimbă fontul consolei în Consolas!
"""
"""specificație:
- intern, polinomul este reprezentat printr-un dicționar de tipul
{ exponent : coeficient }, exponentul fiind unic într-un dicționar

ex.
	3x5 - x3 - 2x2 + 5x - 1 => {5: 3,   ->  3x5
								3: -1,  -> -1x3
								2: -2,  -> -2x2
								1: 5,   ->  5x1
								0: -1}  -> -1x0

"""

import re


def sort_poly(p):
	"""sortează elementele unui dicționar descrescător după chei =
	exponenți (similar formei convenționale pentru polinoame)"""
	result = dict() #inițializează rezultatul

	for key in sorted(p.keys(), reverse=True):
		result[key] = p[key]

	return result


def poly_to_text(p):
	"""transformă un dicționar ce reprezintă un polinom, într-un text
	ce corespunde formei convenționale a polinomului"""
	result = "" #inițializează rezultatul

	p = sort_poly(p) #sortează dicționarul/polinom

	for exponent, coefficient in p.items():
		sign = ''
		x = 'X'

		#cazuri particulare
		#nu afișa termenul cu coeficient 0
		if coefficient == 0:
			continue
		elif coefficient > 0:
			sign = '+'

		#nu afișa coeficientul 1 sau -1, dacă exponentul lui X e 0
		if (coefficient == 1) and (exponent != 0):
			coefficient = ''
		if (coefficient == -1) and (exponent != 0):
			coefficient = '-'

		#nu afișa exponentul 1
		if exponent == 1:
			exponent = ''

		#dacă exponentul este 0, nu afișa nici X, nici exponentul
		if exponent == 0:
			x = ''
			exponent = ''

		#dacă exponentul se afișează, formatează-l ca superscript
		if exponent != '':
			exponent = to_superscript(exponent)

		result += f'{sign}{coefficient}{x}{exponent}'

	if result in ['-', '', '+']:
		result = '0'

	#din rezultat elimină semnul + dacă este la început
	#adaugă spații în jurul semnelor pentru lizibilitate
	return result.lstrip(" +").replace('+', ' + ').replace('-', ' - ')


def to_superscript(e):
	"""(în consolă, numai cu fonturi care suportă UTF-8,
	ex. Consolas, nu Lucida Console) convertește un exponent
	numeric în superscript"""
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


def add_polys(x, y):
	"""calculează suma a două polinoame"""
	#algoritm: utilizând dicționare de tip {exponent : coeficient}:
	# - iterează primul dicționar și pentru fiecare exponent verifică
	# 		dacă există în cel de-al doilea dicționar
	# - dacă există exponenți comuni, adună coeficienții corespunzători
	sum = x.copy() #inițializează rezultatul

	for exponent, coefficient in y.items():
		if exponent in x.keys():
			#dacă exponentul este comun, adună coeficienții în rezultat
			sum[exponent] += y[exponent]
		else:
			#dacă exponentul există doar în al doilea polinom, adaugă-l
			# la rezultat și asociază-l cu coeficientul corespunzător
			sum[exponent] = y[exponent]

	return sum


def multiply_polys(x, y):
	"""calculează produsul a două polinoame"""
	#algoritm: iterează primul polinom și pentru fiecare element din el,
	# iterează în cel de-al doilea polinom realizând înmulțirea termen cu termen
	product = dict() #inițializează rezultatul

	for exponent_x, coefficient_x in x.items():
		for exponent_y, coefficient_y in y.items():
			temp = dict() #reprezentarea unui monom temporar
			exponent_prod = exponent_x + exponent_y #adună exponenții
			coefficient_prod = coefficient_x * coefficient_y #înmulțește coeficienții
			temp[exponent_prod] = coefficient_prod
			product = add_polys(product, temp)

	return product


def validate_input(s):
	"""verifică dacă inputul este în forma acceptată: axm + bxn + cxo
	..., coeficienții sunt întregi; ex. 3x5 - x3 - 2x2 + 5x - 1"""

	while True:
		#crează o listă ale cărei elemente sunt monoamele din polinom
		#elimină spațiile și convertește caracterele la minuscule
		monomials = s.replace(' ', '').lower().replace('-', '+-').split('+')
		p = monomial_matcher(monomials)

		if p:
			return p
		else:
			print("Trebuie să scrii polinomul în forma acceptată!")
			s = input("Mai încearcă: ")


def monomial_matcher(monomials):
	"""verifică dacă fiecare element dintr-o listă este monom,
	iar dacă da returnează un polinom conținând elementele listei"""
	p = dict() #inițializează rezultatul

	#configurează o expresie regulată pentru a testa forma inputului
	#teste: https://regex101.com/
	pattern = r"^([-\+]?)(\d*)(x?)(\d*)$"

	#iterează lista și află pozițiile elementelor fiecărui monom
	#adaugă la un dicționar final datele numerice
	for m in monomials:
		term = re.match(pattern, m)

		#dacă monomul curent nu are formatul acceptat, reia funcția;
		# inclusiv dacă "monomul" e format doar dintr-un semn
		if (term is None) or (m == '+') or (m == '-'):
			return False

		#alocă grupurile în variabile denumite mai inteligibil
		t = (sign, coefficient, x, exponent) = (term.group(1), term.group(2),
		                                        term.group(3), term.group(4))

		#ignoră elementul gol, pentru că patternul permite match
		if t == ('', '', '', ''):
			continue

		#cazuri particulare
		#coeficientul 0 transformă tot monomul în 0 și poate fi ignorat
		if coefficient == 0:
			continue

		#coeficientul nespecificat este 1 sau -1, în funcție de semn
		if coefficient == '':
			coefficient = int(f'{sign}1')
			sign = '' #evită duplicarea semnului

		#X fără exponent are exponentul 1
		if (x == 'x'):
			if (exponent == ""):
				exponent = 1
		else: #X nescris are expnentul 0; X0 = 1
			exponent = 0 #ex. -2 = -2x0

		#dicționar temporar utilizat pentru acumulare
		d = {int(exponent): int(f'{sign}{coefficient}')}

		#optimizare
		if p == {}:
			p = d
		else:
			p = add_polys(p, d)

	return p


def display_results():
	"""afișează rezultatele"""

	#obține polinoamele de la utilizator
	x = validate_input(input("\nA = "))
	y = validate_input(input("B = "))

	sum_p = poly_to_text(add_polys(x, y))
	product_p = poly_to_text(multiply_polys(x, y))

	print("\nA = " + poly_to_text(x))
	print("B = " + poly_to_text(y) + "\n-------------")
	print("A + B = " + sum_p)
	print("A \u00d7 B = " + product_p)

	#...
	input("\nApasă ENTER pentru a închide aplicația...")


#aplicația
print(__doc__) #afișează enunțul temei
example = """Forma acceptată pentru polinoamele cerute mai jos este:

	axm + bxn + cxo ... (coeficienții sunt întregi);
		ex. 3x5 - x3 - 2x2 + 5x - 1"""
print(example)
display_results()