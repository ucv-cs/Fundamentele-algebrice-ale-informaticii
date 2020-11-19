"""Tema 5: Listați toate numerele prime mai mici sau egale cu 1000.
Folosind lista creată, pentru 1 < n ≤ 1000, stabiliți dacă un n dat
este număr prim sau compus.
"""


def sieve(number):
	"""
	Generează un dicționar cu chei numerele naturale de la 2 la n și
	valori True (pentru prime) sau False (pentru compuse)
	 param n: număr natural > 2
	 return: dicționar cu perechi de tip {int: bool}
	 rtype: dict
	"""
	#algoritm: (implementare a ciurului lui Eratostene)
	# - generează un dicționar de numere naturale consecutive > 2 până la
	# 		un număr dat, fiecare cu o valoare True (semnificând număr prim)
	# - în dicționar află multiplii fiecărui element și schimbă-le valoarea
	# 		în False (fiind multipli nu pot fi numere prime)

	number_sieve = dict()

	#completează dicționarul cu perechi {număr: True}
	for i in range(2, number + 1):
		number_sieve[i] = True

	#pentru multiplii fiecărui element din dicționar, dă valoarea False
	for i in number_sieve:
		multiple = 2
		while i * multiple <= number:
			number_sieve[i * multiple] = False
			multiple += 1
	return number_sieve


def positive_matcher(string):
	"""
	Verifică dacă stringul introdus este un număr natural între 2 și 1000
	 param string: input
	 return: int sau False
	 rtype: int sau False
	"""
	result = False
	try:
		number = int(string)
		result = number if (number > 1) and (number <= 1000) else result
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
			print("Trebuie să scrii un număr natural între 2 și 1000!")
			string = input("Mai încearcă: ")


def pretty_print(primes):
	"""
	Afișează lista de numere în câte 10 coloane, cu numerele aliniate
	la dreapta
	 param primes: dicționarul cu numere clasificate ca prime sau compuse
	"""
	primes_string = '\t'
	counter = 1
	width = len(str(primes[len(primes) - 1]))
	for i in primes.keys():
		if primes[i] == True:
			primes_string += f'{i:>{width}}' + ('\n\t' if counter % 10 == 0 else '\t')
			counter += 1
	print(primes_string)


#nu face parte din cerințe...
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


# / nu face parte din cerințe


def display_results():
	"""
	Afișează cerințele, inputul și rezultatul
	"""
	print("Numerele prime până la 1000 sunt:\n")
	primes = sieve(1000)
	pretty_print(primes)

	while True:
		number = validate_input(
		    input(
		        "\nVerifică dacă un număr natural 2 < n ≤ 1000 este prim sau compus.\nScrie numărul: "
		    ))
		message = f'este compus (= {display_factors(decompose(number))})'
		if primes[number]:
			message = 'este prim'
		print(f'\t{number} {message}.\n')


#aplicația
print(__doc__) #afișează enunțul temei
display_results()