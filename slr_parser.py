def construct_lr0_items(grammar):
    """Construct the canonical collection of LR(0) items for the grammar."""
    # Augment the grammar
    augmented = grammar.augment_grammar()
    
    # Define the closure function
    def closure(items):
        result = items.copy()
        
        while True:
            new_items = set()
            
            for item in result:
                nt, prod, dot = item
                
                # If the dot is at the end or the symbol after the dot is a terminal, skip
                if dot >= len(prod) or prod[dot] not in augmented.nonterminals:
                    continue
                
                # Add all productions of the nonterminal after the dot
                next_symbol = prod[dot]
                for p in augmented.productions[next_symbol]:
                    new_item = (next_symbol, p, 0)
                    if new_item not in result:
                        new_items.add(new_item)
            
            if not new_items:
                break
            
            result.update(new_items)
        
        return frozenset(result)
    
    # Define the goto function
    def goto(items, symbol):
        result = set()
        
        for item in items:
            nt, prod, dot = item
            
            # If the dot is at the end or the symbol after the dot is not the given symbol, skip
            if dot >= len(prod) or prod[dot] != symbol:
                continue
            
            # Move the dot one position to the right
            result.add((nt, prod, dot + 1))
        
        return closure(result) if result else None
    
    # Start with the closure of the initial item
    initial_item = (augmented.start_symbol, "S", 0)
    initial_set = closure({initial_item})
    
    # Initialize the collection with the initial set
    collection = [initial_set]
    goto_table = {}
    
    # Compute the collection
    i = 0
    while i < len(collection):
        items = collection[i]
        
        # Compute goto for each grammar symbol
        for symbol in augmented.terminals.union(augmented.nonterminals):
            next_items = goto(items, symbol)
            
            if next_items:
                # If the set is not already in the collection, add it
                if next_items not in collection:
                    collection.append(next_items)
                
                # Add the goto transition
                goto_table[(i, symbol)] = collection.index(next_items)
        
        i += 1
    
    return collection, goto_table, augmented

def construct_slr_table(grammar, first, follow):
    """Construct the SLR(1) parsing table for the grammar."""
    # Construct the LR(0) items
    collection, goto_table, augmented = construct_lr0_items(grammar)
    
    # Initialize the action and goto tables
    action = {}
    goto = {}
    
    # Fill in the tables
    for i, items in enumerate(collection):
        action[i] = {}
        goto[i] = {}
        
        for item in items:
            nt, prod, dot = item
            
            # If the dot is at the end, it's a reduce action
            if dot == len(prod):
                # If it's the augmented production, it's an accept action
                if nt == augmented.start_symbol and prod == "S":
                    action[i]['$'] = ('accept', None)
                else:
                    # For each terminal in FOLLOW(nt), add a reduce action
                    for terminal in follow[nt]:
                        if terminal in action[i] and action[i][terminal][0] != 'reduce':
                            # Conflict detected
                            return None, None
                        action[i][terminal] = ('reduce', (nt, prod))
            
            # If the dot is not at the end, it could be a shift action
            elif dot < len(prod):
                symbol = prod[dot]
                
                # If the symbol is a terminal, add a shift action
                if symbol in augmented.terminals:
                    if (i, symbol) in goto_table:
                        next_state = goto_table[(i, symbol)]
                        
                        if symbol in action[i]:
                            # Conflict detected
                            return None, None
                        
                        action[i][symbol] = ('shift', next_state)
        
        # Fill in the goto table
        for nt in augmented.nonterminals:
            if (i, nt) in goto_table:
                goto[i][nt] = goto_table[(i, nt)]
    
    return action, goto

def slr_parse(grammar, action, goto, input_string):
    """Parse the input string using the SLR(1) parsing table."""
    # Add end marker to input
    if input_string[-1] != '$':
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