class Grammar:
    def __init__(self, grammar):
        self.grammar = grammar
        self.non_terminals = list(self.grammar.keys())
        self.terminals = self.get_terminals()

    def get_terminals(self):
        terminals = []
        for key in self.grammar:
            for rule in self.grammar[key]:
                for char in rule:
                    if char not in self.non_terminals and char not in terminals:
                        terminals.append(char)
        return terminals

    def first(self, symbol):
        first_set = []
        if symbol in self.terminals:
            return [symbol]
        for rule in self.grammar[symbol]:
            if rule[0] in self.terminals:
                first_set.append(rule[0])
            else:
                first_set.extend(self.first(rule[0]))
        return list(set(first_set))

    def follow(self, symbol):
        follow_set = []
        if symbol == self.non_terminals[0]:
            follow_set.append('$')
        for key in self.grammar:
            for rule in self.grammar[key]:
                if symbol in rule:
                    next_index = rule.index(symbol) + 1
                    if next_index < len(rule):
                        if rule[next_index] in self.terminals:
                            follow_set.append(rule[next_index])
                        else:
                            follow_set.extend(self.first(rule[next_index]))
                    else:
                        if key != symbol:
                            follow_set.extend(self.follow(key))
        return list(set(follow_set))

    def check_string(self, string):
        if string[0] != self.first(self.non_terminals[0])[0] or string[-1] != self.follow(self.non_terminals[0])[0]:
            return False
        return True

grammar = {
    'S': ['aABC'],
    'A': ['b'],
    'B': ['c'],
    'C': ['d']
}

g = Grammar(grammar)
print("First sets:")
for non_terminal in g.non_terminals:
    print(f"First({non_terminal}): {g.first(non_terminal)}")

print("\nFollow sets:")
for non_terminal in g.non_terminals:
    print(f"Follow({non_terminal}): {g.follow(non_terminal)}")

input_string = input("\nEnter a string to check: ")
if g.check_string(input_string):
    print("The string is accepted.")
else:
    print("The string is not accepted.")