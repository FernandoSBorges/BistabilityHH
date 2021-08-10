NEURON {
    POINT_PROCESS Izhi2003b
    RANGE a,b,C,Vr,Iin,fflag,thresh,cellid
    NONSPECIFIC_CURRENT i
}

UNITS {
    (mV) = (millivolt)
    (pA) = (picoamp)
    (pF) = (picofarad)
    (nS) = (nanosiemens)
}

INITIAL {
  v=-65
  u=0.0
  net_send(0,1)  
}

PARAMETER {
    a       = 2.0 (nS)
    b       = 60.0 (pA)
    C       = 200.0 (pF)
    Vr       = -68  (mV)   : reset potential after a spike
    Iin = 509.7 (pA)
    thresh = -40  (mV)   : spike threshold
    fflag = 1
    cellid = -1 : A parameter for storing the cell ID, if required (useful for diagnostic information)
}

ASSIGNED {
    v (mV)
    i (nA)
}

STATE {
    u (mV/ms)
}

BREAKPOINT {
    SOLVE states METHOD cnexp  :  derivimplicit # either method works
    i = -0.001*(1.0/C)*(-12.0*(v+70.0) + 12.0*2.0*exp((v+50.0)/2.0) - u + Iin)
}

DERIVATIVE states {
    u' = (2.0/300.0)*(v+70.0)  - (u/300.0)
}

NET_RECEIVE (w) {
    if (flag == 1) {
        WATCH (v > thresh) 2
    } else if (flag == 2) {
        net_event(t)
        v = Vr
        u = u + b
    }
}
