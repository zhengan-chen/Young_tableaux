from young import *

if __name__ == '__main__':
    print("Please enter a standard permutation (an integer sequence separated by spaces, e.g., 1 3 2 4):")
    user_input = input().strip()
    
    try:
        # Parse the user input into a list of integers.
        permutation = list(map(int, user_input.split()))
        
        # Check if the input is a standard permutation (each number is unique and within the range from 1 to n).
        n = len(permutation)
        if sorted(permutation) != list(range(1, n + 1)):
            raise ValueError("The input sequence is not a standard permutation; it should be a permutation of numbers from 1 to n.")
        
        # Calculate smooth elements and non-smooth elements.
        # Step1: Generate the Young diagram and calculate the size of the right cell using the hook formula.
        P, Q = robinson_schensted(permutation)
        print("P tableau:")
        print_tableau(P)
        print("\nQ tableau:")
        print_tableau(Q)

        shape = get_shape(P)
        hooks = hook_lengths(shape)
        print("Hook lengths:")
        print_hook_lengths(hooks)

        num_tableaux = hook_formula(shape)
        print(f"\nNumber of standard Young tableaux for shape {shape}: {num_tableaux}")

        # Step2: Initialization
        S = set()
        N = set()

        if ifsmooth(permutation):
            # print("The permutation is smooth.")
            S.add(tuple(permutation))
        else:
            # print("The permutation is not smooth.")
            N.add(tuple(permutation))

        # Step3: Iteration step
        while len(S) + len(N) < num_tableaux:
            for perm in knuth_step(S, N):
                perm_tuple = tuple(perm)  # turn into tuple 
                if ifsmooth(perm):
                    S.add(perm_tuple)
                else:
                    N.add(perm_tuple)
            
            assert len(S) + len(N) <= num_tableaux, "The number of permutations exceeds the number of standard Young tableaux."
        
        print(f"Number of smooth permutations: {len(S)}")
        print(f"Number of non-smooth permutations: {len(N)}")
    
    except Exception as e:
        print(f"Error: {e}")
