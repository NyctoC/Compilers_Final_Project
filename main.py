from collections import defaultdict

class Grammar:
    def __init__(self):
        self.non_terminals = set()
        self.terminals = set()
        self.productions = defaultdict(list)
        self.start_symbol = 'S'  # Siempre es 'S' según la especificación
        self.first_sets = defaultdict(set)
        self.follow_sets = defaultdict(set)
        self.epsilon = 'e'
        self.end_marker = '$'

    def add_production(self, head, body):
        self.non_terminals.add(head)
        for symbol in body.split():
            if symbol.isupper() and symbol != self.epsilon:
                self.non_terminals.add(symbol)
            elif symbol != self.epsilon:
                self.terminals.add(symbol)
        self.productions[head].append(body)


    # IMPORTANTE: Dado que las alternativas se separan por espacios, y cada alternativa es una secuencia completa de símbolos,
    # hay que definir una convención explícita. 
    # La mejor opción para este input es usar | como separador entre alternativas, y no espacios, para evitar ambigüedad.
    # Esta fue una dificultad en el input original, ya que no se especificó cómo separar las alternativas. Esto va en el LATEX.

    def load_from_file(self, path):
        with open(path, 'r') as file:
            n = int(file.readline().strip())
            for _ in range(n):
                line = file.readline().strip()
                head, body = line.split('->')
                head = head.strip()
                alternatives = body.strip().split('|')
                for alt in alternatives:
                    self.add_production(head, alt.strip())


    def compute_first_sets(self):
        for nt in self.non_terminals:
            self.first_sets[nt] = set()
        for t in self.terminals:
            self.first_sets[t].add(t)
        
        changed = True
        while changed:
            changed = False
            for head in self.productions:
                for production in self.productions[head]:
                    for symbol in production.split():
                        if symbol in self.terminals:
                            before = len(self.first_sets[head])
                            self.first_sets[head].add(symbol)
                            if len(self.first_sets[head]) > before:
                                changed = True
                            break
                        elif symbol in self.non_terminals:
                            before = len(self.first_sets[head])
                            self.first_sets[head].update(self.first_sets[symbol] - {self.epsilon})
                            if len(self.first_sets[head]) > before:
                                changed = True
                            if self.epsilon not in self.first_sets[symbol]:
                                break
                    else:
                        if self.epsilon not in self.first_sets[head]:
                            self.first_sets[head].add(self.epsilon)
                            changed = True

    def compute_follow_sets(self):
        for nt in self.non_terminals:
            self.follow_sets[nt] = set()
        self.follow_sets[self.start_symbol].add(self.end_marker)
        
        changed = True
        while changed:
            changed = False
            for head in self.productions:
                for production in self.productions[head]:
                    symbols = production.split()
                    for i, current in enumerate(symbols):
                        if current not in self.non_terminals:
                            continue
                        if i < len(symbols) - 1:
                            next_sym = symbols[i+1]
                            if next_sym in self.terminals:
                                before = len(self.follow_sets[current])
                                self.follow_sets[current].add(next_sym)
                                if len(self.follow_sets[current]) > before:
                                    changed = True
                            else:
                                before = len(self.follow_sets[current])
                                first_beta = set()
                                for sym in symbols[i+1:]:
                                    if sym in self.terminals:
                                        first_beta.add(sym)
                                        break
                                    first_beta.update(self.first_sets[sym] - {self.epsilon})
                                    if self.epsilon not in self.first_sets[sym]:
                                        break
                                else:
                                    first_beta.add(self.epsilon)
                                
                                self.follow_sets[current].update(first_beta - {self.epsilon})
                                if len(self.follow_sets[current]) > before:
                                    changed = True
                        if i == len(symbols) - 1 or all(self.epsilon in self.first_sets[sym] for sym in symbols[i+1:]):
                            before = len(self.follow_sets[current])
                            self.follow_sets[current].update(self.follow_sets[head])
                            if len(self.follow_sets[current]) > before:
                                changed = True

g = Grammar()
g.load_from_file('input.txt')
g.compute_first_sets()
g.compute_follow_sets()

print("FIRST sets:")
for nt in sorted(g.non_terminals):
    print(f"FIRST({nt}) = {g.first_sets[nt]}")

print("\nFOLLOW sets:")
for nt in sorted(g.non_terminals):
    print(f"FOLLOW({nt}) = {g.follow_sets[nt]}")