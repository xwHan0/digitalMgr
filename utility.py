def ecc_width(width):
    if width <= 0: return 0         # 不需要ECC
    elif width == 1: return 3       # 使用多数判决算法
    else: return 12
    
def bit_width(width):
    base = 2
    for i in range(32):
        if width <= base:
            return i
        base *= 2
    raise Exception('Overflow')