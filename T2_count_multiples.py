"""Tema 2: Determinați numărul numerelor naturale ≤ n, nenule, care sunt
divizibile cu p sau q sau r, unde p, q, r sunt trei numere prime distincte
(se va testa dacă cele trei numere date p, q și r sunt prime).
"""
import re


def group_matcher(string):
	"""
	Verifică dacă stringul introdus este un grup de 3 numere
	naturale ≥ 1, separate prin virgulă (ex. 2, 3, 5)
	 param string: input
	 return: (int, int, int) sau False
	 rtype: (int, int, int) sau False
	"""
	string = re.sub(r'\s', '', string.lower())
	pattern = r'^(\d+),(\d+),(\d+)$'
	regex = re.compile(pattern, re.X)
	matcher = regex.search(string)

	if not matcher:
		print("Inputul nu este corect.")
		return False
	else:
		numbers = (p, q, r) = (int(matcher.group(1)), int(matcher.group(2)),
		                       int(matcher.group(3)))
		for num in numbers:
			if not is_prime(num):
				print(f'{num} nu este prim.')
				return False
		if p == q or p == r or q == r:
			print("Numerele trebuie să fie distincte!")
			return False

		return numbers


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

	#folosind proprietatea că un număr compus trebuie să aibă cel
	# puțin un divizor prim ≤ sqrt(n):
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


def is_prime(number):
	"""
	Verifică dacă un număr natural > 1 este prim
	 param number: numărul
	 return: bool
	 rtype: bool
	"""
	return True if len(decompose(number)) == 1 else False


def positive_matcher(string):
	result = False
	try:
		number = int(string)
		if number < 6:
			print("Numărul trebuie să fie > 5!")
		else:
			result = number
	except:
		print("Trebuie să scrii un număr natural și > 5!")

	return result


def validate_input(string, matcher_callback):
	"""
	Verifică dacă inputul este valid
	 param string: input
	 return: numărul rezultat în urma validării
	 rtype: int
	"""
	while True:
		output = matcher_callback(string)
		if output:
			return output
		else:
			string = input("\nMai încearcă: ")


def pretty_print(divisors):
	"""
	Afișează lista de divizori în câte 10 coloane, cu numerele aliniate
	la dreapta
	 param divisors: lista cu numere
	"""
	divisors_string = '\t'
	counter = 1
	width = len(str(divisors[len(divisors) - 1]))
	for i in divisors:
		divisors_string += f'{i:>{width}}' + ('\n\t' if counter % 10 == 0 else '\t')
		counter += 1

	print(divisors_string)


def display_results():
	"""
	Afișează inputul și rezultatul
	"""

	while True:
		number = validate_input(
		    input("Scrie numărul natural n > 5: "), positive_matcher)
		group = validate_input(
		    input(
		        "Acum scrie trei numere prime distincte, separate prin virgulă:\n\t(p, q, r) = "
		    ), group_matcher)

		#află multiplii fiecărui număr prim, mai mici decât number
		# și adaugă-i într-o listă (care poate conține duplicate)
		multiples = []
		for i in group:
			n = 1
			while i * n <= number:
				multiples += [i * n]
				n += 1

		#elimină duplicatele prin conversie din listă în set
		multiples = set(multiples)

		#reconvertește setul (nesortabil) în listă și sorteaz-o
		multiples = sorted(list(multiples))

		#afișează lista de numere ≤ n, divizibile cu p sau q sau r, apoi numărul lor
		print(
		    f"Numerele ≤ {number}, divizibile cu {group[0]} sau {group[1]} sau {group[2]} sunt:\n"
		)
		pretty_print(multiples)
		print(f'\nNumărul lor este: {len(multiples)}\n------------------------\n')


#aplicația
print(__doc__) #afișează enunțul temei
display_results()