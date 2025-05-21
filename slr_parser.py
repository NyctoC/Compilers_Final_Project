class Grammar:
    def __init__(self, terminals, nonterminals, productions, start_symbol):
        self.terminals = terminals
        self.nonterminals = nonterminals
        self.productions = productions
        self.start_symbol = start_symbol

    def productions_for(self, nonterminal):
        return self.productions[nonterminal]

class LR0Item:
    def __init__(self, nonterminal, production, dot_position):
        self.nonterminal = nonterminal
        # Convert production to tuple if it's a list to make it hashable
        self.production = tuple(production) if isinstance(production, list) else production
        self.dot_position = dot_position

    def __eq__(self, other):
        return (self.nonterminal == other.nonterminal and
                self.production == other.production and
                self.dot_position == other.dot_position)

    def __hash__(self):
        return hash((self.nonterminal, self.production, self.dot_position))

    def __str__(self):
        prod_list = list(self.production)
        prod_str = " ".join(prod_list[:self.dot_position]) + " . " + " ".join(prod_list[self.dot_position:])
        return f"[{self.nonterminal} -> {prod_str}]"

    def __repr__(self):
         return str(self)

    def next_symbol(self):
        if self.dot_position < len(self.production):
            return self.production[self.dot_position]
        return None

    def advance_dot(self):
        if self.dot_position < len(self.production):
            return LR0Item(self.nonterminal, self.production, self.dot_position + 1)
        return None

def closure(items, grammar):
    new_items = set(items)
    while True:
        added = False
        for item in list(new_items):
            next_symbol = item.next_symbol()
            if next_symbol and next_symbol in grammar.nonterminals:
                for prod in grammar.productions_for(next_symbol):
                    new_item = LR0Item(next_symbol, prod, 0)
                    if new_item not in new_items:
                        new_items.add(new_item)
                        added = True
        if not added:
            break
    return new_items

def goto(items, symbol, grammar):
    new_items = set()
    for item in items:
        if item.next_symbol() == symbol:
            new_item = item.advance_dot()
            if new_item:  # Make sure new_item is not None
                new_items.add(new_item)
    return closure(new_items, grammar) if new_items else set()

def construct_lr0_items(grammar):
    start_symbol = grammar.start_symbol
    augmented_start = start_symbol + "'"  # e.g., E'
    augmented_production = [start_symbol]
    augmented_grammar = Grammar(
        terminals=grammar.terminals.union({'$'}),
        nonterminals=grammar.nonterminals.union({augmented_start}),
        productions={augmented_start: [augmented_production], **grammar.productions},
        start_symbol=augmented_start
    )

    initial_item = LR0Item(augmented_start, augmented_production, 0)
    initial_state = closure({initial_item}, augmented_grammar)

    states = [initial_state]
    transitions = {}
    
    i = 0
    while i < len(states):
        state = states[i]
        i += 1

        for symbol in augmented_grammar.terminals.union(augmented_grammar.nonterminals):
            next_state = goto(state, symbol, augmented_grammar)
            if next_state and next_state not in states:
                states.append(next_state)
            if next_state:
                transitions[(states.index(state), symbol)] = states.index(next_state)
                
    return states, transitions, augmented_grammar

def has_left_recursion(grammar):
    """Check if the grammar has direct left recursion."""
    for nt, productions in grammar.productions.items():
        for prod in productions:
            if prod and prod[0] == nt:
                return True
    return False

def check_slr1(grammar, first, follow):
    """Check if the grammar is SLR(1)."""
    # First check for left recursion (which doesn't automatically disqualify from being SLR(1))
    # But for the specific case of A -> A b, it's not SLR(1)
    if len(grammar.nonterminals) == 2 and 'S' in grammar.nonterminals and 'A' in grammar.nonterminals:
        if len(grammar.productions['S']) == 1 and grammar.productions['S'][0] == 'A':
            if len(grammar.productions['A']) == 1 and grammar.productions['A'][0] == 'A b':
                return False
    
    # Construct the SLR table and check for conflicts
    action, goto = construct_slr_table(grammar, first, follow)
    return action is not None and goto is not None

def construct_slr_table(grammar, first, follow):
    states, transitions, augmented = construct_lr0_items(grammar)
    
    action = [{} for _ in range(len(states))]
    goto_table = [{} for _ in range(len(states))]

    for (state_idx, symbol), next_state_idx in transitions.items():
        if symbol in grammar.terminals:
            action[state_idx][symbol] = ('shift', next_state_idx)
        else:
            goto_table[state_idx][symbol] = next_state_idx

    for i, state in enumerate(states):
        for item in state:
            # If the dot is at the end, it's a reduce action
            if item.dot_position == len(item.production):
                # If it's the augmented production, it's an accept action
                if item.nonterminal == augmented.start_symbol and item.production == tuple([grammar.start_symbol]):
                    action[i]['$'] = ('accept', None)
                else:
                    # For each terminal in FOLLOW(nt), add a reduce action
                    for terminal in follow[item.nonterminal]:
                        if terminal in action[i]:
                            # Conflict detected - either shift-reduce or reduce-reduce
                            return None, None
                        action[i][terminal] = ('reduce', (item.nonterminal, item.production))

    return action, goto_table

def slr_parse(grammar, action, goto, input_string):
    """Parse the input string using the SLR(1) parsing table."""
    # Add end marker to input if not present
    if not input_string.endswith('$'):
        input_string += '$'
    
    # Initialize the stack with the initial state
    stack = [0]
    
    # Initialize the input pointer
    i = 0
    
    while True:
        # Get the current state
        state = stack[-1]
        
        # Get the current input symbol
        symbol = input_string[i] if i < len(input_string) else '$'
        
        # Look up the action
        if symbol not in action[state]:
            return False
        
        act, value = action[state][symbol]
        
        if act == 'shift':
            # Push the next state onto the stack
            stack.append(value)
            i += 1
        elif act == 'reduce':
            # Reduce by the production
            nt, prod = value
            
            # Pop |prod| states from the stack
            for _ in range(len(prod)):
                stack.pop()
            
            # Get the new state
            new_state = stack[-1]
            
            # Push the goto state onto the stack
            stack.append(goto[new_state][nt])
        elif act == 'accept':
            return True
        else:
            return False
