def compute_first(grammar):
    """Compute the FIRST set for all symbols in the grammar."""
    first = {nt: set() for nt in grammar.nonterminals}
    
    # Add FIRST for all terminals
    for terminal in grammar.terminals:
        first[terminal] = {terminal}
    
    # Add empty string to FIRST set
    first['e'] = {'e'}
    
    # Repeat until no changes are made
    while True:
        updated = False
        
        for nonterminal in grammar.nonterminals:
            for production in grammar.productions[nonterminal]:
                # If production is empty (e), add e to FIRST(nonterminal)
                if production == 'e':
                    if 'e' not in first[nonterminal]:
                        first[nonterminal].add('e')
                        updated = True
                    continue
                
                # Process each symbol in the production
                all_derive_e = True
                for i, symbol in enumerate(production):
                    # If symbol is a terminal, add it to FIRST(nonterminal) and break
                    if symbol not in grammar.nonterminals:
                        if symbol != 'e':  # Skip empty string
                            if symbol not in first[nonterminal]:
                                first[nonterminal].add(symbol)
                                updated = True
                        all_derive_e = False
                        break
                    
                    # If symbol is a nonterminal, add FIRST(symbol) - {e} to FIRST(nonterminal)
                    for terminal in first[symbol] - {'e'}:
                        if terminal not in first[nonterminal]:
                            first[nonterminal].add(terminal)
                            updated = True
                    
                    # If e is not in FIRST(symbol), we can't derive e from this production
                    if 'e' not in first[symbol]:
                        all_derive_e = False
                        break
                
                # If all symbols in the production can derive e, add e to FIRST(nonterminal)
                if all_derive_e and 'e' not in first[nonterminal]:
                    first[nonterminal].add('e')
                    updated = True
        
        if not updated:
            break
    
    return first

def compute_follow(grammar, first):
    """Compute the FOLLOW set for all nonterminals in the grammar."""
    follow = {nt: set() for nt in grammar.nonterminals}
    
    # Add $ to FOLLOW(S)
    follow[grammar.start_symbol].add('$')
    
    # Repeat until no changes are made
    while True:
        updated = False
        
        for nonterminal in grammar.nonterminals:
            for production in grammar.productions[nonterminal]:
                if production == 'e':
                    continue
                
                # Process each symbol in the production
                for i, symbol in enumerate(production):
                    if symbol in grammar.nonterminals:
                        # Get the first set of the rest of the production
                        rest = production[i+1:] if i+1 < len(production) else 'e'
                        
                        # Compute FIRST of the rest of the production
                        first_of_rest = set()
                        all_derive_e = True
                        
                        if rest == 'e':
                            first_of_rest.add('e')
                        else:
                            all_derive_e = True
                            for s in rest:
                                if s not in grammar.nonterminals:
                                    first_of_rest.add(s)
                                    all_derive_e = False
                                    break
                                
                                for t in first[s] - {'e'}:
                                    first_of_rest.add(t)
                                
                                if 'e' not in first[s]:
                                    all_derive_e = False
                                    break
                            
                            if all_derive_e:
                                first_of_rest.add('e')
                        
                        # Add FIRST(rest) - {e} to FOLLOW(symbol)
                        for terminal in first_of_rest - {'e'}:
                            if terminal not in follow[symbol]:
                                follow[symbol].add(terminal)
                                updated = True
                        
                        # If e is in FIRST(rest) or rest is empty, add FOLLOW(nonterminal) to FOLLOW(symbol)
                        if 'e' in first_of_rest:
                            for terminal in follow[nonterminal]:
                                if terminal not in follow[symbol]:
                                    follow[symbol].add(terminal)
                                    updated = True
        
        if not updated:
            break
    
    return follow

def compute_first_of_string(first, string):
    """Compute the FIRST set of a string of grammar symbols."""
    if not string or string == 'e':
        return {'e'}
    
    result = set()
    all_derive_e = True
    
    for symbol in string:
        if symbol not in first:  # Terminal
            result.add(symbol)
            all_derive_e = False
            break
        
        # Add all terminals except e
        for terminal in first[symbol] - {'e'}:
            result.add(terminal)
        
        # If this symbol cannot derive e, we're done
        if 'e' not in first[symbol]:
            all_derive_e = False
            break
    
    # If all symbols can derive e, add e to the result
    if all_derive_e:
        result.add('e')
    
    return result