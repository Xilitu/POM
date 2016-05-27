from import_data import *
from gurobipy import *
from generate_output import *

def solve(full_path_instance):
    nOldFirehouses, nNewFirehouses, nBoroughs, c, b, old_firehouses, new_firehouses, boroughs, firehouses = dig_data(full_path_instance)
    protection_cost = calc_protection_cost(boroughs, old_firehouses, new_firehouses, c)

    model = Model("Firehouses")

    # set up model variables
    x = {}
    for j in boroughs:
        for i in old_firehouses:
            x[i,j] = model.addVar(
                vtype=GRB.BINARY, name="x_"+i+"_"+j, obj=( protection_cost[i,j])
            )
        for i in new_firehouses:
            x[i,j] = model.addVar(
                vtype=GRB.BINARY, name="x_"+i+"_"+j, obj=( protection_cost[i,j])
            )

    y = {}
    for j in old_firehouses:
        y[j] = model.addVar(
            vtype=GRB.BINARY, name="y_" + j, obj= old_firehouses[j][2]
        )
    for j in new_firehouses:
        y[j] = model.addVar(
            vtype=GRB.BINARY, name="y_" + j, obj= new_firehouses[j][2]
        )
    model.modelSense = GRB.MINIMIZE
    model.update()

    # set up constraints
    # every borough gets one firehouse
    for j in boroughs:
        model.addConstr(
            quicksum(x[i,j] for i in firehouses) == 1
        )

    # limit maximum of boroughs per firehouse
    for i in firehouses:
        model.addConstr(
            quicksum(x[i,j] for j in boroughs) <= b
        )

    # linking constraint
    for j in boroughs:
        i = boroughs[j][2]
        model.addConstr(
            1-x[i,j] <= y[i]
        )

        # connection to other old firehouses is forbidden
        for f in old_firehouses:
            if not(i == f):
                model.addConstr(
                    x[f,j] <= 0
                )

    for i in new_firehouses:
        for j in boroughs:
            model.addConstr(
                x[i,j] <= y[i]
            )

    model.update()
    model.write('model.lp')
    model.optimize()

    return model, x, y

fname = 'firedata1.csv'
model, x, y = solve(fname)
graphics_output(model, x,y, fname)
