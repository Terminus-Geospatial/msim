

def velocity( dt, v_init, a_cur ):

    return v_init + a_cur * dt 

def position( dt, p_init, v_cur ):

    return p_init + v_cur * dt
