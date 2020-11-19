"""Tema 7: Să se realizeze un program care să calculeze
suma și produsul a două numere complexe, modulul unui număr complex
și inversul său, dacă numărul este nenul.\n"""

import math, re


def sum_complex(a, b):
	"""calculează suma a două numere complexe, folosind reprezentarea
	 lor ca tuple de forma (x, y)"""
	#algoritm: folosind forma algebrică, avem (a + bi) + (c + di) =
	#  a + c + (b + d)i

	#descompune cele două tuple în parte reală și parte imaginară
	(ax, ay, bx, by) = (a[0], a[1], b[0], b[1])

	#returnează suma ca tuple
	#variantă specifică limbajului: return complex(ax, ay) + complex(bx, by)
	return (ax + bx, ay + by)


def product_complex(a, b):
	"""calculează produsul a două numere complexe, folosind
	reprezentarea lor ca tuple de forma (x, y)"""
	#algoritm: folosind forma algebrică, avem (a + bi)(c + di) =
	# ac + adi + bci + bidi = ac - bd + (ad + bc)i

	#descompune cele două tuple în parte reală și parte imaginară
	(ax, ay, bx, by) = (a[0], a[1], b[0], b[1])

	#returnează produsul ca tuple
	#variantă specifică limbajului: return complex(ax, ay) * complex(bx, by)
	return (ax * bx - ay * by, ax * by + ay * bx)


def module_complex(a):
	"""calculează modulul unui număr complex, folosind reprezentarea
	lui ca tuple de forma (x, y)"""
	#algoritm: |(a, b)| = sqrt(a^2 + b^2)

	#dacă numărul e nul nu are modul
	if is_zero(a):
		return "nedeterminat pentru (0, 0)"

	#descompune tuple în parte reală și parte imaginară
	(ax, ay) = (a[0], a[1])

	#returnează un număr real reprezentând modulul numărului complex
	#variantă specifică limbajului: return abs(complex(ax, ay))
	return math.sqrt(pow(ax, 2) + pow(ay, 2))


def inverse_complex(a):
	"""calculează inversul unui număr complex, folosind reprezentarea
	 lui ca tuple de forma (x, y)"""
	#algoritm: 1 / c = a / (pow(a, 2) + pow(b ,2)) - b / (pow(a, 2) + pow(b ,2))i
	#v. https://www.mathportal.org/calculators/complex-numbers-calculator/complex-unary-operations-calculator.php

	#dacă numărul e nul nu are invers
	if is_zero(a):
		return "nedeterminat pentru (0, 0)"

	#descompune tuple în parte reală și parte imaginară
	(ax, ay) = (a[0], a[1])

	#calculează componentele inversului
	cx = ax / pow(module_complex(a), 2) #partea reală
	cy = -ay / pow(module_complex(a), 2) #partea imaginară
	if ay == 0:
		cy = 0 #evită afișarea de tip +-0i

	#returnează inversul ca tuple
	#variantă specifică limbajului: return 1/complex(ax, ay)
	return (cx, cy)


def complex_to_string(a):
	"""convertește reprezentarea unui număr complex ca tuple în
	reprezentarea matematică pentru afișare"""

	#când a nu este tuple; ci, de regulă, string (ex. dacă provine
	# din inverse_complex()) returnează a
	if not isinstance(a, tuple):
		return a

	#descompune tuple în parte reală și parte imaginară
	(ax, ay) = (a[0], a[1])

	#pregătește semnul pentru partea imaginară
	sy = ""
	if ay >= 0:
		sy = "+"

	#returnează un string pentru afișare; ex. -1-2i
	return f"{ax:g}{sy}{ay:g}i"


def is_zero(a):
	"""verifică dacă numărul complex introdus este nul"""
	if ((a[0] == 0) and (a[1] == 0)):
		return True
	else:
		return False


def display_results(m, n):
	"""afișează rezultatele"""

	#calculează fiecare cerință și crează variablilele pentu afișare
	sum = complex_to_string(sum_complex(m, n))
	product = complex_to_string(product_complex(m, n))
	mod_m = module_complex(m)
	mod_n = module_complex(n)
	inverse_m = complex_to_string(inverse_complex(m))
	inverse_n = complex_to_string(inverse_complex(n))

	#afișarea propriu-zisă
	print("\n\nm = " + complex_to_string(m))
	print("n = " + complex_to_string(n) + "\n-------------")
	print(f"m+n = {sum}")
	print(f"m*n = {product}")
	print(f"|m| = {mod_m}")
	print(f"|n| = {mod_n}")
	print(f"1/m = {inverse_m}")
	print(f"1/n = {inverse_n}")

	#...
	input("\nApasă ENTER pentru a închide aplicația...")


def validate_input(a):
	"""verifică dacă inputul este în forma acceptată:
	număr, număr; ex. -1, 2 sau 0.3,-5.34"""
	#configurează o expresie regulată pentru a testa forma inputului
	#teste: https://regex101.com/
	pattern = r"^([+-]?\d+?\.*?\d*?),([+-]?\d+?\.*?[\d]*?)$"

	#declară componentele tuple
	(ax, ay) = (0, 0)

	while True:
		#elimină spațiile
		a = a.replace(' ', '')
		result = re.match(pattern, a)
		if result == None:
			print("Trebuie să scrii două numere separate prin virgulă!")
			a = input("Mai încearcă: ")
			continue
		else:
			ax = float(result.groups()[0])
			ay = float(result.groups()[1])
			break

	return (ax, ay)


#aplicația
print(__doc__) #afișează enunțul temei

#obține numerele de la tastatură
print(
    "Scrie coordonatele celor două numere complexe, separate prin virgulă (ex. a, b):\n"
)
m = validate_input(input("m = "))
n = validate_input(input("n = "))
display_results(m, n)