"""Tema 1: Pentru două mulțimi finite să se realizeze
un program care să calculeze reuniunea, intersecția, diferența și
diferența simetrică a acestora.\n"""


def display_results(A, B):
	"""afișează rezultatele operațiilor cu mulțimi"""
	A = convert_string_to_set(A)
	B = convert_string_to_set(B)
	print("\nA = " + display_set(A))
	print("B = " + display_set(B) + "\n-------------")
	print("A U B = " + display_set(do_union(A, B))) #\u222a ...
	print("A \u2229 B = " + display_set(do_intersection(A, B)))
	print("A \u005c B = " + display_set(do_difference(A, B)))
	print("B \u005c A = " + display_set(do_difference(B, A)))
	print("A \u0394 B = " + display_set(do_symmetric_difference(A, B)))
	print("\nBonus:\nA x B = " + display_set(do_cartesian_product(A, B)))
	print("B x A = " + display_set(do_cartesian_product(B, A)))
	input("\nApasă ENTER pentru a închide aplicația...")


def display_set(my_set):
	"""afișează un set; dacă mulțimea este vidă, va afișa simbolul
	acesteia ca 0"""
	if my_set == set(): #empty set
		return "0" #\u2205 nu se afișează corect în Windows 10
	else:
		#convertește setul în listă, apoi sortează lista pentru afișare
		my_set = sorted(list(my_set))

		#afișează cu acolade
		return str(my_set).replace("'", '').replace('[', '{').replace(']', '}')


def convert_string_to_set(string):
	"""transformă un string într-un set"""
	#elimină spațiile
	string = string.replace(' ', '')

	#split() pornind de la , => listă
	result_list = string.split(",")

	#elimină elementele goale (rezultate din input incorect: ex. "2,,")
	result_list = list(filter(None, result_list))

	#returnează un set
	return set(result_list)


def do_union(a, b):
	"""realizează reuniunea a două seturi și returnează setul
	rezultat"""
	#declară setul returnat și alocă primul set
	result = a.copy()

	#metoda generică: ciclează cel de-al doilea set și adaugă fiecare
	# element la rezultat
	for x in b:
		result.add(x)

	#metoda specifică limbajului: union()
	#result = a.union(b)

	#returnează setul rezultat
	return result


def do_intersection(a, b):
	"""realizează intersecția a două seturi și returnează setul
	rezultat"""
	#declară setul returnat
	result = set()

	#metoda generică: ciclează primul set, testează pentru
	# fiecare element din a dacă e și în b și adaugă la
	# rezultat numai elementele comune
	for x in a:
		if x in b:
			result.add(x)

	#metoda specifică limbajului: intersection()
	#result = a.intersection(b)

	#returnează setul rezultat
	return result


def do_difference(a, b):
	"""realizează diferența a două seturi și returnează setul
	rezultat"""
	#declară setul returnat
	result = set()

	#metoda generică: ciclează ambele seturi și adaugă la rezultat
	# numai elementele care sunt în a și nu sunt în b
	for x in a:
		if not (x in b):
			result.add(x)

	#metoda specifică limbajului: difference()
	#result = a.difference(b)

	#returnează setul rezultat
	return result


def do_symmetric_difference(a, b):
	"""realizează diferența simetrică a două seturi și returnează
	setul rezultat"""
	#declară setul returnat
	result = set()

	#metoda generică: ciclează ambele seturi și adaugă la rezultat
	# numai elementele care sunt în a și nu sunt în b
	#for x in a:
	#	if not(x in b):
	#		result.add(x)

	#for y in b:
	#	if not(y in a):
	#		result.add(y)

	#metoda specifică limbajului: symmetric_difference()
	#result = a.symmetric_difference(b)

	#metoda alternativă: utilizând funcțiile deja definite
	diff_ab = do_difference(a, b)
	diff_ba = do_difference(b, a)
	result = do_union(diff_ab, diff_ba)

	#returnează setul rezultat
	return result


def do_cartesian_product(a, b):
	"""realizează produsul cartezian al două seturi și returnează
	setul rezultat"""
	#declară setul returnat
	result = set()

	#metoda generică: ciclează ambele seturi și adaugă la rezultat
	# perechile formate din fiecare element din a și fiecare element din b
	for i in a:
		for j in b:
			result.add((i, j))

	#returnează setul rezultat
	return result


#aplicația
print(__doc__) #afișează enunțul temei
print("Scrie elementele celor două mulțimi, separate prin ,:\n")
A = input("A = ")
B = input("B = ")
display_results(A, B)