k = 1.0*10.0**3
M = 1.0*10.0**6
m = 1.0*10.0**(-3)

def parallel(*argv):
    i = 1
    Req = argv[i-1]*argv[i]/(argv[i-1]+argv[i])
    if len(argv)>2:
        i = i+1
        for arg in range(len(argv)-2):
            Req = Req*argv[i]/(Req+argv[i])
    return Req

# givens
beta = 100.0
g_m = 1.6*m
r_pi = beta/g_m
R_B = 100.0*k
R_1 = 750.0
r_o = 2.125*M
R_C = 62.0*k
R_3 = 100.0*k
R_L = parallel(r_o, R_C, R_3)
R_E = 2.0*k

# without R_E
R_iB = r_pi
R_out = R_C
R_iC = r_o

# now including R_E
R_iBRE = r_pi+(beta+1)*R_E
R_inRE = parallel(R_iBRE, R_B)
R_iCRE = r_o*(1+g_m*parallel(r_pi, R_E))
R_outRE = parallel(R_iCRE, R_C)

gain = -((parallel(R_B, r_pi))/(R_1+ parallel(R_B, r_pi)))*g_m*R_L

R_Lprime = parallel(R_C, R_3)
gain_RE = -g_m*R_Lprime/(1+g_m*R_E)
