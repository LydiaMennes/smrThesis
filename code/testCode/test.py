import re
import codecs
import unicodedata


if __name__ == "__main__":
	f = codecs.open("weird_words.txt", "r", encoding='utf-8')
	out = open("weird_words_cleaned.txt", "w") #, encoding='utf-8'
	reg = re.compile("\W")
	for l in f:
		l = l.replace("\n", "")
		l2 = unicodedata.normalize('NFKD', l).encode('ascii', 'ignore')
		print type(l2)
		a = re.sub(reg, "", l2)
		out.write(l2 + "  -  " + a + "\n")
	f.close()
	out.close()
		