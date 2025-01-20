from young import *

if __name__ == '__main__':
    print("请输入一个标准置换(一个以空格分隔的整数序列,如:1 3 2 4):")
    user_input = input().strip()
    
    try:
        # 解析用户输入为整数列表
        permutation = list(map(int, user_input.split()))
        
        # 检查输入是否是一个标准置换（每个数字唯一，且在1到n范围内）
        n = len(permutation)
        if sorted(permutation) != list(range(1, n + 1)):
            raise ValueError("输入的序列不是一个标准置换,应该是1到n的一个排列")
        
        # 计算光滑元与非光滑元
        # Step1: 生成Young图 并通过hook formula计算右cell大小
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

        # Step2: 初始化
        S = set()
        N = set()

        if ifsmooth(permutation):
            # print("The permutation is smooth.")
            S.add(tuple(permutation))
        else:
            # print("The permutation is not smooth.")
            N.add(tuple(permutation))

        # Step3: 迭代
        while len(S) + len(N) < num_tableaux:
            for perm in knuth_step(S, N):
                perm_tuple = tuple(perm)  # 转为元组存储
                if ifsmooth(perm):
                    S.add(perm_tuple)
                else:
                    N.add(perm_tuple)
            
            assert len(S) + len(N) <= num_tableaux, "The number of permutations exceeds the number of standard Young tableaux."
        
        print(f"Number of smooth permutations: {len(S)}")
        print(f"Number of non-smooth permutations: {len(N)}")
    
    except Exception as e:
        print(f"发生错误: {e}")
