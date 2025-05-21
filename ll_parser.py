from first_follow import compute_first_of_string

def construct_ll_table(grammar, first, follow):
    """Construct the LL(1) parsing table for the grammar."""
    table = {}
    
    # Initialize the table with empty dictionaries
    for nonterminal in grammar.nonterminals:
        table[nonterminal] = {}
    
    # Fill in the table
    for nonterminal in grammar.nonterminals:
        for i, production in enumerate(grammar.productions[nonterminal]):
            # Compute FIRST of the production
            first_of_production = compute_first_of_string(first, production)
            
            # For each terminal in FIRST(production), add the production to the table
            for terminal in first_of_production - {'e'}:
                if terminal in table[nonterminal]:
                    # Conflict detected
                    return None
                table[nonterminal][terminal] = production
            
            # If e is in FIRST(production), add the production to the table for each terminal in FOLLOW(nonterminal)
            if 'e' in first_of_production:
                for terminal in follow[nonterminal]:
                    if terminal in table[nonterminal]:
                        # Conflict detected
                        return None
                    table[nonterminal][terminal] = production
    
    return table

def ll_parse(grammar, table, input_string):
    """Parse the input string using the LL(1) parsing table."""
    # Add end marker to input
    if input_string[-1] != '$':
        input_string += '$'
    
    # Initialize the stack with the start symbol and end marker
    stack = ['$', grammar.start_symbol]
    
    # Initialize the input pointer
    i = 0
    
    while stack:
        # Get the top of the stack
        top = stack.pop()
        
        # If top is the end marker and input is fully consumed, accept
        if top == '$' and i == len(input_string):
            return True
        
        # If top is a terminal, match it with the current input symbol
        if top not in grammar.nonterminals:
            if i < len(input_string) and top == input_string[i]:
                i += 1
            else:
                return False
        else:
            # If top is a nonterminal, look up the production in the table
            if i < len(input_string) and input_string[i] in table[top]:
                production = table[top][input_string[i]]
                
                # Push the production in reverse order onto the stack
                if production != 'e':
                    for symbol in reversed(production):
                        stack.append(symbol)
            else:
                return False
    
    return i == len(input_string)