def q_value_iteration(states, gamma, convergence_threshold):
    delta = 1
    J,_J = {}, {}
    for s in states:
        J[s.id] = 0
        _J[s.id] = 0
    while delta > convergence_threshold:
        _J = J
        Q = {}
        for s in states:
            Q[s.id] = {}
            for a in s.transitions:
                Q[s.id][a] = s.rewards[a] + gamma * _J[s.transitions[a].id]
        J = {}
        delta = 0
        for s in states:
            if len(Q[s.id]) > 0:
                J[s.id] = max(Q[s.id].values())
            else:
                J[s.id] = 0
            delta = max(delta, abs(J[s.id]-_J[s.id]))
    return Q


