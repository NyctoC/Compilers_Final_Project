class Grammar:
    def __init__(self):
        self.productions = {}  # Dictionary mapping nonterminals to list of productions
        self.terminals = set()
        self.nonterminals = set()
        self.start_symbol = 'S'  # Default start symbol
        
    def add_production(self, nonterminal, alternatives):
        """Add a production rule to the grammar."""
        if nonterminal not in self.productions:
            self.productions[nonterminal] = []
            self.nonterminals.add(nonterminal)
        
        for alternative in alternatives:
            self.productions[nonterminal].append(alternative)
            
            # Add terminals to the set
            for symbol in alternative:
                if not symbol.isupper() and symbol != 'e':
                    self.terminals.add(symbol)
    
    def augment_grammar(self):
        """Create an augmented grammar by adding S' -> S."""
        augmented = Grammar()
        augmented.start_symbol = "S'"
        augmented.add_production(augmented.start_symbol, ["S"])
        
        # Copy all original productions
        for nt, prods in self.productions.items():
            for prod in prods:
                augmented.add_production(nt, [prod])
        
        augmented.nonterminals = self.nonterminals.copy()
        augmented.nonterminals.add(augmented.start_symbol)
        augmented.terminals = self.terminals.copy()
        
        return augmented
    
    def __str__(self):
        result = []
        for nt, prods in self.productions.items():
            alternatives = " | ".join(prods)
            result.append(f"{nt} -> {alternatives}")
        return "\n".join(result)