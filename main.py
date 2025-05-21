from grammar import Grammar
from first_follow import compute_first, compute_follow
from ll_parser import construct_ll_table, ll_parse
from slr_parser import construct_slr_table, slr_parse

def parse_grammar():
    """Parse the grammar from standard input."""
    n = int(input())
    grammar = Grammar()
    
    for _ in range(n):
        line = input().strip()
        nonterminal, productions = line.split(' -> ')
        alternatives = productions.split(' ')
        grammar.add_production(nonterminal, alternatives)
    
    return grammar

def main():
    # Parse the grammar
    grammar = parse_grammar()
    
    # Compute FIRST and FOLLOW sets
    first = compute_first(grammar)
    follow = compute_follow(grammar, first)
    
    # Construct the LL(1) and SLR(1) parsing tables
    ll_table = construct_ll_table(grammar, first, follow)
    slr_action, slr_goto = construct_slr_table(grammar, first, follow)
    
    # Determine the type of grammar
    is_ll1 = ll_table is not None
    is_slr1 = slr_action is not None and slr_goto is not None
    
    if is_ll1 and is_slr1:
        print("Select a parser (T: for LL(1), B: for SLR(1), Q: quit):")
        while True:
            choice = input().strip()
            
            if choice == 'Q':
                break
            
            if choice == 'T':
                # Parse using LL(1)
                while True:
                    input_string = input().strip()
                    if not input_string:
                        break
                    
                    result = ll_parse(grammar, ll_table, input_string)
                    print("yes" if result else "no")
                
                print("Select a parser (T: for LL(1), B: for SLR(1), Q: quit):")
            
            elif choice == 'B':
                # Parse using SLR(1)
                while True:
                    input_string = input().strip()
                    if not input_string:
                        break
                    
                    result = slr_parse(grammar, slr_action, slr_goto, input_string)
                    print("yes" if result else "no")
                
                print("Select a parser (T: for LL(1), B: for SLR(1), Q: quit):")
    
    elif is_ll1:
        print("Grammar is LL(1).")
        while True:
            input_string = input().strip()
            if not input_string:
                break
            
            result = ll_parse(grammar, ll_table, input_string)
            print("yes" if result else "no")
    
    elif is_slr1:
        print("Grammar is SLR(1).")
        while True:
            input_string = input().strip()
            if not input_string:
                break
            
            result = slr_parse(grammar, slr_action, slr_goto, input_string)
            print("yes" if result else "no")
    
    else:
        print("Grammar is neither LL(1) nor SLR(1).")

if __name__ == "__main__":
    main()
