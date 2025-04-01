def construct_SAR(s):
    """construct the suffix array of a string"""
    n = len(s)

    ranks = [ord(c) for c in s]
    
    sa = list(range(n))
    
    tmp = [0] * n
    
    step = 1
    while step < n:

        sa.sort(key=lambda idx: (ranks[idx], ranks[idx+step] if idx+step < n else -1))
        
        tmp[sa[0]] = 0
        for i in range(1, n):
            prev, curr = sa[i-1], sa[i]
            left_pair  = (ranks[prev], ranks[prev+step] if prev+step < n else -1)
            right_pair = (ranks[curr], ranks[curr+step] if curr+step < n else -1)
            tmp[curr] = tmp[prev] + (1 if right_pair != left_pair else 0)
        
        for i in range(n):
            ranks[i] = tmp[i]
        
        step <<= 1 
        
        if ranks[sa[-1]] == n-1:
            break
    
    return sa

def construct_BWT(s):
    """construct the Burrows-Wheeler Transform of a string"""
    s = s + '$'
    sa = construct_SAR(s)
    bwt = [s[i-1] for i in sa]
    
    return "".join(bwt)