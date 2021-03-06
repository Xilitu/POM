import matplotlib.pyplot as plt
from import_data import *

def graphics_output(model, x, y, full_path_instance):
    # get data from file
    nOldFirehouses, nNewFirehouses, nBoroughs, c, b, old_firehouses, new_firehouses, boroughs, firehouses = dig_data(full_path_instance)

    # set plot size
    plt.figure(figsize=(50,50))

    # only show firehouses that are in use
    for f in firehouses:
        # c: number of connections to firehouse
        c = 0
        for b in boroughs:
            if x[f,b].x == 1:
                c += 1
        if c == 0:
            try:
                # delete firehouse if no borough is connected
                old_firehouses.pop(f,None)
                new_firehouses.pop(f,None)
            except:
                print('error')

    # draw scatter points for boroughs and firehouses
    x_b = [boroughs[b][0] for b in boroughs]
    y_b = [boroughs[b][1] for b in boroughs]

    x_of = [old_firehouses[f][0] for f in old_firehouses]
    y_of = [old_firehouses[f][1] for f in old_firehouses]

    x_nf = [new_firehouses[f][0] for f in new_firehouses]
    y_nf = [new_firehouses[f][1] for f in new_firehouses]

    plt.scatter(x_b, y_b, color="blue", alpha=1, s=100)
    plt.scatter(x_of, y_of, color="brown", alpha=1, marker="v",s=100)
    plt.scatter(x_nf, y_nf, color="red", alpha=1, marker="^",s=100)

    # draw connection lines and annotations
    for b in boroughs:
        plt.annotate(b, (boroughs[b][0] + 2, boroughs[b][1]) )
        for f in old_firehouses:
            plt.annotate(f, (old_firehouses[f][0] + 2, old_firehouses[f][1]) )
            if x[f,b].x == 1:
                plt.plot([boroughs[b][0], old_firehouses[f][0]], [boroughs[b][1], old_firehouses[f][1]], color="black", alpha=0.3)
        for f in new_firehouses:
            plt.annotate(f, (new_firehouses[f][0] + 2, new_firehouses[f][1]) )
            if x[f,b].x == 1:
                plt.plot([boroughs[b][0], new_firehouses[f][0]], [boroughs[b][1], new_firehouses[f][1]], color="black", alpha=0.3)

    plt.grid(True)
    plt.show()