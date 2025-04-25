def find_x(A_n, n):
	if A_n > (n)*(n+1)/2:
		raise Exception("La valeur de A_n est trop grande")
	if A_n ==  (n)*(n+1)/2:
		return (n, 0)
	x = 0
	for k in range(n):
		i = n-k-1
		A_n -= i
		x += 1
		if A_n < 0:
			return (x-1, A_n + i)
		if A_n == 0:
			return (x, 0)


def main_loop():
	n = int(input("\nQuelle est la valeur de n ? (e pour quitter) "))
	A_n = int(input("\nQuelle est la valeur de A_n ? (e pour quitter)"))
	

	if A_n > (n)*(n+1)/2:
		print("\nLa valeur de A_n est trop grande\n\n")
	else : 
		x, r = find_x(A_n, n)
		c = x*n**2 - n*x**2 + (1/3)*x*(x-1)*(x+1) + r*(n-x)
		
		print("\nVoici les valeur de x et r :", 'x =', x, ", r =", r, "Et le coût maximal C_max = ", int(c), "\n\n")

	
while True:
	main_loop()


