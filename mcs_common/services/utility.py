from random import randint

def generate_otp(length):
    range_start = 10**(length-1)
    range_end = (10**length)-1
    return randint(range_start, range_end)