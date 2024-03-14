import math, random

def generate_number():
    digits = "0123456789"
    OTP = ""
    for ـ in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP