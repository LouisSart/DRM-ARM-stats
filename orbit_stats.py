import numpy as np

def unpack(line):
    values = line.split(",")
    assert(len(values) == 5)
    index_str, co_str, esl_str, depth, sol = values
    sol = sol.strip(" \n,")
    return int(index_str), co_str, esl_str, int(depth), sol

def get_drm(co, esl):
    c_drm = sum(int(o != '0') for o in co)
    e_drm = 8 - 2 * sum(int(esl[i]) for i in range(4, 8))
    return c_drm, e_drm

def get_carm(co):
    return sum (int(co[i] == '1') for i in (1, 3, 4, 6)) + \
                sum(int(co[i] == '2') for i in (0, 2, 5, 7))

def get_earm(esl):
    return sum(int(esl[i] == '1') for i in (0, 2, 8, 10))

def get_arm(co, esl):
    return get_carm(co), get_earm(esl)

# Orbit 1 : ULF, URB, DRF, DLB
# Orbit 2 : ULB, URF, DLF, DRB
orbit_1 = (0, 2, 5, 7)
orbit_2 = (1, 3, 4, 6)
def get_orbit_splits(co):
    orbit_1_bc = sum(int(co[i] != '0') for i in orbit_1)
    orbit_2_bc = sum(int(co[i] != '0') for i in orbit_2)
    return orbit_1_bc, orbit_2_bc

U_layer = (0, 1, 2, 3)
D_layer = (4, 5, 6, 7)
def get_UD_splits(co):
    U_bc = sum(int(co[i] != '0') for i in U_layer)
    D_bc = sum(int(co[i] != '0') for i in D_layer)
    return U_bc, D_bc

L_layer = (0, 3, 4, 7)
R_layer = (1, 2, 5, 6)
def get_LR_splits(co):
    L_bc = sum(int(co[i] != '0') for i in L_layer)
    R_bc = sum(int(co[i] != '0') for i in R_layer)
    return L_bc, R_bc

def get_corner_case(co):
    # 4a : R like (orbits (2,2), both UD and LR are either (2,2) or (0,4))
    # 4b : U' R like (orbits (2,2), any of UD, LR is (3,1))
    # 4c : U' R2 U R like (orbits (3,1), any of UD, LR is (3,1))
    # 4d : U F2 R like (orbits (0,4), UD and LR are (2,2))

    orbit_splits = get_orbit_splits(co)
    ca = get_carm(co)  # Corner arm
    if orbit_splits in ((3, 1), (1,3)):
        return '4c'
    elif orbit_splits in ((0, 4), (4, 0)):
        return '4d'
    else:
        ud_splits = get_UD_splits(co)
        lr_splits = get_LR_splits(co)
        if ud_splits in ((3, 1), (1, 3)) or lr_splits in ((3, 1), (1, 3)):
            if ca in (0, 4):
                return '4b'
            else:
                return '4b.2'
        else:
            if ca in (0, 4):
                return '4a'
            else:
                return '4a.2'
        
n_corner_cases = 6
cc_to_index = {
    '4a': 0,
    '4a.2': 1,
    '4b': 2,
    '4b.2': 3,
    '4c': 4,
    '4d': 5
}

def edge_index(cc, arm):
    if cc in ('4a', '4b') and arm[0] == 4:
        return 2 - arm[1]
    elif cc == '4c' and arm[0] == 3:
        return 2 - arm[1]
    elif cc == '4d':
        assert arm[0] == 2
    
    return arm[1]

if __name__ == "__main__":
    orbit_data = np.zeros((n_corner_cases, 3), 
        dtype=[("n_cases", int),
            ("avg_length", np.float64),
            ("sub6_probability", np.float64),
            ("sub7_probability", np.float64)])

    with open("full_data.csv", "r", encoding="utf-8") as file:

        for line in file:
            index, co, esl, d, sol = unpack(line)
            drm, arm, orbit = get_drm(co, esl), get_arm(co, esl), get_orbit_splits(co)
            cc = get_corner_case(co)
            if drm == (4, 4):
                ci = cc_to_index[cc]
                ei = edge_index(cc, arm)
                # if cc in ('4b.2'): print(sol, cc, ei)
                orbit_data[ci, ei]['n_cases'] += 1
                orbit_data[ci, ei]['avg_length'] += d
                if d < 6:
                    orbit_data[ci, ei]['sub6_probability'] += 1
                if d < 7:
                    orbit_data[ci, ei]['sub7_probability'] += 1

    for ci in range(n_corner_cases):
        for ei in range(3):
            if orbit_data[ci, ei]['n_cases'] != 0:
                orbit_data[ci, ei]['avg_length'] /= orbit_data[ci, ei]['n_cases']
                orbit_data[ci, ei]['sub6_probability'] /= orbit_data[ci, ei]['n_cases']
                orbit_data[ci, ei]['sub7_probability'] /= orbit_data[ci, ei]['n_cases']

    print(orbit_data['n_cases'])
    print(orbit_data['sub6_probability'])
    print(orbit_data['sub7_probability'])
    print(orbit_data['avg_length'])