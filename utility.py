def ecc_width(width):
    if width <= 0: return 0         # 不需要ECC
    elif width == 1: return 3       # 使用多数判决算法
    elif width < 12 : return 5
    elif width < 27: return 6
    elif width < 58: return 7
    elif width < 121: return 8
    elif width < 248: return 9
    elif width < 503: return 10
    elif width < 1014: return 11
    elif width < 2037: return 12
    elif width < 4084: return 13
    elif width < 8179: return 14
    else: return 15
    
def bit_width(width):
    base = 2
    for i in range(32):
        if width <= base:
            return i
        base *= 2
    raise Exception('Overflow')