NEURON {
    POINT_PROCESS Izhi2003b
    RANGE a,b,c,d,f,g,Iin,fflag,thresh,cellid
    NONSPECIFIC_CURRENT i
}

UNITS {
    (mV) = (millivolt)
    (nA) = (nanoamp)
    (nF) = (nanofarad)
}

INITIAL {
  v=-65
  u=0.0
  net_send(0,1)  
}

PARAMETER {
    a       = 0.02 (/ms)
    b       = 0.2  (/ms)
    c       = -68  (mV)   : reset potential after a spike
    d       = 60    (mV/ms)
    f = 5
    g = 140
    Iin = 509.7
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
    i = -0.005*0.001*(-12.0*(v+70.0) + 12.0*2.0*exp((v+50.0)/2.0) - u + Iin)
}

DERIVATIVE states {
    u' = (2.0/300.0)*(v+70.0)  - (u/300.0)
}

NET_RECEIVE (w) {
    if (flag == 1) {
        WATCH (v > thresh) 2
    } else if (flag == 2) {
        net_event(t)
        v = c
        u = u + d
    }
}
