from NAGenerator import NAGenerator
import random as rd


def test_na(na: NAGenerator):
    nums = dict()
    ind = 0
    while True:
        num = na.next()
        if num in nums:
            break
        nums[num] = 1
        ind += 1
    return ind

def main():
    seed = 1664525
    multi = 1013904223
    mod = 2**32
    na = NAGenerator(seed, multi, mod)
    p = test_na(na)
    print(f"Test 1 has {p} numbers before repeating.")
    print(f"Seed: {seed}, Multiplier: {multi}, Modulus: {mod}\n")

if __name__ == "__main__":
    main()