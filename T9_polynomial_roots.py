"""Tema 9: Să se realizeze un program care să calculeze valoarea unui
polinom într-un punct. Folosind acest lucru, să se cerceteze dacă un
polinom cu coeficienți întregi are sau nu rădăcini întregi.

Indicație: dacă f = a0 + a1X + ... + anX\u207f in Z[X], pentru a vedea dacă
 f are rădăcini întregi aflăm divizorii întregi ai lui a0 și calculăm
 valoarea lui f în aceștia; obținem rădăcini atunci când valoarea este 0.

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
	"""
	Sortează elementele unui dicționar descrescător după chei =
	exponenți (similar formei convenționale pentru polinoame)
	"""
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


def get_divisors(n):
	""""
	Află divizorii unui număr întreg
	 param n: numărul întreg
	 return: listă cu divizorii
	 rtype: list
	"""
	divisors = []
	for i in range(-abs(n), abs(n) + 1):
		if (i != 0) and (n % i == 0):
			divisors.append(i)
	#sau, mai compact: return sorted([i for i in range(-abs(n), abs(n)+1) if i != 0 if n%i == 0])
	return sorted(divisors)


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


def eval_poly(p, x):
	""""
	Calculează valoarea unui polinom p în punctul x
	 param p: polinom reprezentat ca dicționar
	 param x: număr (real)
	 return: rezultatul înlocuirii numărului în expresia p
	 rtype: float
	"""
	value = 0
	for exponent, coefficient in p.items():
		value += coefficient * x**exponent
	return value


def validate_input(s):
	"""
	Verifică dacă inputul este în forma acceptată: axm + bxn + cxo
	..., coeficienții sunt întregi; ex. 3x5 - x3 - 2x2 + 5x - 1
	 param s: inputul text de validat
	 return: polinom reprezentat printr-un dicționar
	 rtype: dict
	"""
	while True:
		#crează o listă ale cărei elemente sunt monoamele din polinom
		#elimină spațiile și convertește caracterele la minuscule
		monomials = s.replace(' ', '').lower().replace('-', '+-').split('+')
		p = monomial_matcher(monomials)

		if p:
			return p
		else:
			s = input(
			    "Trebuie să scrii polinomul în forma acceptată!\nMai încearcă: ")


def monomial_matcher(monomials):
	"""
	Verifică dacă fiecare element dintr-o listă este monom,
	iar dacă da returnează un polinom conținând elementele listei
	"""
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

	#ne asigurăm că există un monom cu exponentul 0
	return add_polys(p, {0: 0})


def display_results():
	"""
	Afișează rezultatele
	"""

	#obține polinomul de la utilizator
	f = validate_input(input("\nf = "))

	divisors = get_divisors(f[0])
	divisors_string = f'{divisors}' if f[0] != 0 else '[]'

	eval_poly_divisors = [
	    (d, eval_poly(f, d)) for d in divisors if divisors != []
	]
	eval_poly_divisors_string = ''
	for e in eval_poly_divisors:
		eval_poly_divisors_string += f'f({e[0]}) = {e[1]}\n\t'

	f_roots_string = 'x = 0' if f[0] == 0 else ''
	counter = 1
	for e in eval_poly_divisors:
		if e[1] == 0: #int?
			f_roots_string += f'x{to_subscript(counter)} = {e[0]}\n\t'
			counter += 1
	if f_roots_string == '':
		f_roots_string = '[]'

	print("\nf = " + poly_to_text(f))
	print(f"Divizorii întregi ai lui {f[0]} sunt: {divisors_string}")
	print(
	    f"Valorile lui f pentru acești divizori sunt:\n\t{eval_poly_divisors_string}"
	)
	print(f"Rădăcinile întregi ale lui f sunt:\n\t{f_roots_string}")


#aplicația
print(__doc__) #afișează enunțul temei
example = """Forma acceptată pentru polinomul cerut mai jos este:

	axm + bxn + cxo ... (coeficienții sunt întregi);
		ex. 3x5 - x3 - 2x2 + 5x - 1"""
print(example)
while True:
	display_results()