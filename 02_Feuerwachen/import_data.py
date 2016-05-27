import math

def dig_data(filename):
    old_firehouses = {}
    new_firehouses = {}
    boroughs = {}
    firehouses = []
    with open(filename) as f:
        section = 0
        for line in f:
            if '#' in line:
                section += 1
            else:
                if section ==1:
                    split = line.replace('\n', '').split(',')
                    nOldFirehouses = int(split[0])
                    nNewFirehouses = int(split[1])
                    nBoroughs      = int(split[2])
                    c              = float(split[3])
                    b              = int(split[4])
                elif section == 2:
                    split = line.replace('\n', '').split(',')
                    # loc_id, x, y, destruction cost
                    old_firehouses[split[0]] = [float(split[1]), float(split[2]), float(split[3])]
                    firehouses.append(split[0])
                elif section == 3:
                    split = line.replace('\n', '').split(',')
                    # loc_id, x, y, construction cost
                    new_firehouses[split[0]] = [float(split[1]), float(split[2]), float(split[3])]
                    firehouses.append(split[0])
                elif section == 4:
                    split = line.replace('\n', '').replace(' ', '').split(',')
                    # loc_id, x, y, currently protected by
                    boroughs[split[0]] = [float(split[1]), float(split[2]), split[3]]

    return nOldFirehouses, nNewFirehouses, nBoroughs, c, b, old_firehouses, new_firehouses, boroughs, firehouses

def calc_protection_cost(boroughs, old_firehouses, new_firehouses, c):
    protection_cost = {}

    for borough in boroughs:
        x_b = boroughs[borough][0]
        y_b = boroughs[borough][1]
        for fhouse in old_firehouses:
            x_f = old_firehouses[fhouse][0]
            y_f = old_firehouses[fhouse][1]

            protection_cost[fhouse,borough ] = c*math.sqrt( (x_b-x_f)**2 + (y_b - y_f)**2 )
        for fhouse in new_firehouses:
            x_f = new_firehouses[fhouse][0]
            y_f = new_firehouses[fhouse][1]

            protection_cost[fhouse, borough ] = c*math.sqrt( (x_b-x_f)**2 + (y_b - y_f)**2 )

    return protection_cost