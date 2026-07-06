import sys
sys.path.insert(0, 'src/python')
from z_band_prime_predictor.simple_pgs_generator_v2 import emit_record

def test():
    # p = 29 -> p+1 = 30 -> 30 % 30 == 0 -> should short-circuit and emit 31
    print(emit_record(29))
    
    # p = 89 -> p+1 = 90 -> 90 % 30 == 0 -> but p+2=91 is composite -> should fall back and emit 97
    print(emit_record(89))
    
if __name__ == '__main__':
    test()
