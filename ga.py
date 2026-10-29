e1 = [1,0,0]
e2 = [0,1,0]
e3 = [0,0,1]

def norma(v):
    norma=0
    for i in range(len(v)):
        norma+=v[i]*v[i]
    return norma**0.5

def diferenca(b,a):
    tam_g=len(a)
    tam_p=tam_g
    a_bigger=True
    if len(b)>tam_g:
        tam_g=len(b)
        a_bigger=False
    else:
        tam_p=len(b)
    v=[0]*tam_g
    for i in range(tam_g):
        if i<tam_p:
            v[i]=b[i]-a[i]
        else:
            if a_bigger:
                v[i]=-a[i]
            else:
                v[i]=b[i]
    return v

def soma(a,b):
    tam_g=len(a)
    tam_p=tam_g
    a_bigger=True
    if len(b)>tam_g:
        tam_g=len(b)
        a_bigger=False
    else:
        tam_p=len(b)
    v=[0]*tam_g
    for i in range(tam_g):
        if i<tam_p:
            v[i]=b[i]+a[i]
        else:
            if a_bigger:
                v[i]=a[i]
            else:
                v[i]=b[i]
    return v

def produto_escalar(l,v):
    r=[]
    for i in range(len(v)):
        r.append(v[i]*l)
    return r

def produto_interno(a,b):
    tam_p=len(a)
    if len(b)<tam_p:
        tam_p=len(b)
    r=0
    for i in range(tam_p):
        r+=a[i]*b[i]
    return r

def produto_vetorial(a,b):
    r = [0,0,0]
    if len(a)==3 and len(b)==3:
        r[0] = a[1]*b[2]-a[2]*b[1]
        r[1] = a[2]*b[0]-a[0]*b[2]
        r[2] = a[0]*b[1]-a[1]*b[0]
    return r

def projecao(v,u):
    return produto_escalar(produto_interno(v,u)/(norma(u)*norma(u)),u)


