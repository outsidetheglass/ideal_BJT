import math

# these are the units
k = 1.0*10.0**3
M = 1.0*10.0**6
m = 1.0*10.0**(-3)
p = 1.0*10.0**(-12)

# this function calculates parallel resistance
def parallel(*argv):
    i = 1
    Req = argv[i-1]*argv[i]/(argv[i-1]+argv[i])
    if len(argv)>2:
        i = i+1
        for arg in range(len(argv)-2):
            Req = Req*argv[i]/(Req+argv[i])
    return Req

# this function takes the input and converts it into units
# using kilo and Mega and some rounding to the third decimal place
def pretty(val):
    isNegative = False
    isKilo = False
    isMega = False
    isMilli = False
    isMicro = False
    if val < 0:
        isNegative = True
        val = abs(val)
    if val < 0.001:
        ans = math.ceil(val*10000000)/10.0
        isMicro = True
    elif val < 1:
        ans = math.ceil(val*100000)/100.0
        isMilli = True
    elif val < 100:
        ans = math.ceil(val*10.0)/10.0
    elif val < 999:
        ans = math.ceil(val*100.0)/100.0
    elif val < 1000000:
        ans = math.ceil(val)/1000.0
        isKilo = True
    elif val < 1000000000:
        ans = math.ceil(val/10000.0)/100.0
        isMega = True
    if isNegative:
        ans = -ans
    if isKilo:
        ans = str(ans) + 'k'
    elif isMega:
        ans = str(ans) + 'M'
    elif isMicro:
        ans = str(ans) + 'mu'
    elif isMilli:
        ans = str(ans) + 'm'
    else:
        ans = str(ans)
    return ans

# assumed based on parameters given
A_v = 120.0 # going for 100, adding 20% for tolerance
R_in = 120.0*k # going for 100k, adding 20% for tolerance
beta = 311.0
V_A = 99.0
I_C = 0.01*m
V_CC = 12.0
V_C = V_CC / 2.0 # a good Q point is halfway down V_CC
V_CE = 3.0 #just putting anything down between 2-4

#Calculated values
R_C = (V_CC - V_C) / I_C
g_m = 40.0 * I_C
r_pi = beta / g_m
if r_pi < R_in:
    needRE = True
    print('r_pi is less than R_in, so we need R_E, don\'t forget to include it.')
r_o = (V_A + V_CE) / I_C
R_L = (math.floor((1.0 / R_C)+(1.0 / r_o)))^(-1)
R_E = -(A_v - g_m * R_L) / (A_v * g_m)
r_iB = r_pi + (beta + 1) * R_E
if r_iB < R_in:
    print("This r_iB won't work, it is less than R_in, use lower current.")
else:
    print('r_iB: ' + str(r_iB))
V_E = V_CC - V_C - V_CE
V_B = V_E + 0.7
R_B = (r_iB * R_in) / (r_iB - R_in)
R_1 = -(R_B * V_CC) / (V_B - V_CC)
I_bias = V_B / R_1
R_2 = (V_CC - V_B) / I_bias
R_4 = V_E / I_C - R_E
# R_ic with R_E and R_out with R_E
R_iCRE = r_o * ( 1 + g_m * parallel(r_pi, R_E) )
R_outRE = parallel(R_iCRE, R_C)



# to convert to AC
C_1 = 100.0*p
C_3 = C_1
C_2 = C_1
R_3 = 9999999999999999999999.0 # as close to infinity as possible
R_I = 0.0

print('g_m: ' + str(pretty(g_m)))
print('V_E: ' + str(V_E) + 'V')
print('V_B: ' + str(V_B) + 'V')
print('I_bias: ' + str(pretty(I_bias)))
print('----------Resistances in ohms----------')
print('R_C: ' + str(pretty(R_C)))
print('R_1: ' + str(pretty(R_1)))
print('R_2: ' + str(pretty(R_2)))
print('R_B: ' + str(pretty(R_B)))
print('R_4: ' + str(pretty(R_4)))
print('R_E: ' + str(pretty(R_E)))
print('r_pi: ' + str(pretty(r_pi)))
print('r_o: ' + str(pretty(r_o)))
print('R_L: ' + str(pretty(R_L)))
print('R_out: ' + str(pretty(R_outRE)))

# convert gain given in dB into linear form
dBintoLinear = 10**(115.573/20)
print('gain dB into Linear: ' + str(pretty(dBintoLinear)))
