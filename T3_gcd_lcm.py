"""Tema 3: Pentru două numere naturale m și n, să se
realizeze un program care să determine c.m.m.d.c. și c.m.m.m.c.
Indicație: Pentru calculul cm.m.m.d.c. folosim algoritmul lui
Euclid, iar pentru c.m.m.m.c. folosim relația a*b =
c.m.m.d.c.(a, b)*c.m.m.m.c.(a, b)\n"""


def gcd(a, b):
	"""
	Calculează c.m.m.d.c. pentru două numere naturale
	 param a: număr natural
	 param b: număr natural
	 return: număr reprezentând c.m.m.d.c.(a, b)
	 rtype: int
	"""
	#elimină rapid combinațiile cu 0
	if a == 0 or b == 0:
		return a if a >= b else b

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
	Calculează c.m.m.m.c. pentru două numere naturale
	 param a: număr natural
	 param b: număr natural
	 return: număr reprezentând c.m.m.m.c.(a, b)
	 rtype: int
	"""
	#elimină rapid combinațiile cu 0
	if a == 0 or b == 0:
		#Octave returnează pentru lcm(0,0): "warning: division by zero"
		#v. https://en.wikipedia.org/wiki/Least_common_multiple
		# "some authors define LCM (a,0) as 0 for all a, which is the
		# result of taking the LCM to be the least upper bound in the
		# lattice of divisibility"
		return 0

	#algoritm: folosim relația a * b = c.m.m.d.c.(a, b) *
	# c.m.m.m.c.(a, b) => c.m.m.m.c.(a, b) = a * b / c.m.m.d.c.(a, b)
	return int(a * b / gcd(a, b))


def display_results(m, n):
	"""
	Afișează inputul și rezultatul
	"""
	#calculează c.m.m.d.c. și c.m.m.m.c.
	gd = gcd(m, n)
	lm = lcm(m, n)

	#observație
	gd_note = ""
	if gd == 1: # and (m != 1 or n != 1): #v. https://en.wikipedia.org/wiki/Coprime_integers
		gd_note = f". Numerele {m} și {n} sunt coprime (prime între ele)."

	#afișează numerele
	print(f"--------------\nPentru m = {m} și n = {n}:")
	print(f"\tc.m.m.d.c. = {gd}{gd_note}")
	print(f"\tc.m.m.m.c. = {lm}\n")


def check_natural_number(a):
	"""
	Verifică dacă inputul este valid (număr natural)
	 param a: input
	 return: numărul rezultat în urma validării
	 rtype: int
	"""
	while (not a.isdigit() or (int(a) < 0)):
		a = input("Numărul trebuie să fie natural\nMai încearcă: ")
	return int(a)


#aplicația
print(__doc__) #afișează enunțul temei
while True:
	print("Scrie cele două numere naturale:")
	m = check_natural_number(input("m = "))
	n = check_natural_number(input("n = "))
	display_results(m, n)