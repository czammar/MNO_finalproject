import cupy as cp

def inc_index(vec,index,h):
    '''
    Funcion auxiliar para calculo gradiente y hessiano.
    Args:
        vec (array): array de cupy.
        index (int): indice.
        h (float):   cantidad del vec[index] que sera incrementada.
    Returns:
        vec (array): array vec de cupy con vec[index] incrementado con h.
    '''
    vec[index] +=h
    return vec

def dec_index(vec,index,h=1):
    '''
    Funcion auxiliar para calculo gradiente y hessiano.
    Args:
        vec (array): array de cupy.
        index (int): indice.
        h (float):   antidad del vec[index] que sera disminuida.
    Returns:
        vec (array): array vec de cupy con vec[index] disminuida con h.
    '''
    vec[index] -=h
    return vec

def compute_error(x_obj,x_approx):
    '''
    Error absoluto o relativo entre x_obj y x_approx.
    '''
    if cp.linalg.norm(x_obj) > cp.nextafter(0,1):
        Err=cp.linalg.norm(x_obj-x_approx)/cp.linalg.norm(x_obj)
    else:
        Err=cp.linalg.norm(x_obj-x_approx)
    return Err

def norm_residual(feas_primal, feas_dual):
    '''
    Calcula la norma de residuos para el método de punto inicial no factible de Newton
    '''
    return cp.sqrt(cp.linalg.norm(feas_primal)**2 +\
                   cp.linalg.norm(feas_dual)**2
                   )

def condicion_cupy(A):
    A_inv = cp.linalg.inv(A)
    NAi = cp.linalg.norm(A_inv)
    NA = cp.linalg.norm(A)
    return NAi*NA