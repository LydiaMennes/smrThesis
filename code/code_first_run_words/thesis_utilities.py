def four_digit_string(i):
	if i == 0:
		return "0000"
	elif i >=10000:
		return "TOO LARGE NUMBER"
	s = ""
	start = 1000
	while i/start < 1:
		s += "0"
		start = start / 10
	return s + str(i)