from collections import deque, defaultdict

class Automaton:

	def __init__(self, keywords):

		self.root = {'output': [], 'fail_to': None}

		for keyword in keywords:
			self._add_keyword(keyword)

		self._build_failure_pointers()


	def _add_keyword(self, keyword):

		curr = self.root
		for char in keyword:
			if char not in curr:
				curr[char] = {'output': [], 'fail_to': None}
			curr = curr[char]
		curr['output'].append(len(keyword))

	def _build_failure_pointers(self):

		curr = self.root
		dq = deque([(curr, '', None)])
		while dq:
			curr, curr_val, parent = dq.popleft()
			
			if parent:
				parent_fail_to = parent['fail_to']

				while parent_fail_to and (curr_val not in parent_fail_to):
					parent = parent_fail_to
					parent_fail_to = parent_fail_to['fail_to']

				if parent_fail_to and curr_val in parent_fail_to:
					curr['fail_to'] = parent_fail_to[curr_val]
					for l in curr['fail_to']['output']:
						curr['output'].append(l)
				else:
					curr['fail_to'] = parent

			for key in curr:
				if key != 'output' and key != 'fail_to':
					dq.append((curr[key], key, curr))

	def search(self, text):

		curr = self.root
		res = defaultdict(list)
		for i, c in enumerate(text):

			if c in curr:
				curr = curr[c]
				for l in curr['output']:
					word = text[i-l+1: i+1]
					res[word].append(i-l+1)
			else:
				while curr['fail_to']:
					curr = curr['fail_to']
					if c in curr:
						curr = curr[c]
						for l in curr['output']:
							word = text[i-l+1: i+1]
							res[word].append(i-l+1)
						break
		return res



keywords = ['he', 'she', 'hers', 'his']
act = Automaton(keywords)
print(act.root)
res = act.search('ahishers')
print(res)

list2 = ['what', 'hat', 'ver', 'er']
act2 = Automaton(list2)
res2 = act2.search('whatever, err ... , wherever')
print(res2)


