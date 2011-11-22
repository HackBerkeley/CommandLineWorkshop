#!/usr/bin/python

import random

def generate_ints(n):
	return ''.join([str(random.randint(0, 9)) for k in range(n)])

def generate_number():
	fmts = ['({0}) {1} {2}', '{0}{1}{2}', '{0}-{1}-{2}', '({0})({1})({2})', '{2}{0}{1}']
	return random.choice(fmts).format(generate_ints(3), generate_ints(3), generate_ints(4))

def html_number():
	def tag(name, s):
		return '<{0}>{1}</{2}>'.format(name, s, name)

	entry = generate_number()
	tag_pool = ['p', 'div', 'li']
	random.shuffle(tag_pool)
	while len(tag_pool):
		entry = tag(tag_pool.pop(), entry)
	return entry

if __name__ == '__main__':
	nr = 5
	nr_lines = 2500
	fmt, ext = random.choice([
		(html_number, 'html'),
		(generate_number, 'log'),
	])
	for k in range(nr):
		with open("nr_{0}.{1}".format(k, ext), 'w') as f:
			for j in range(nr_lines):
				f.write(fmt())
				f.write('\n')
