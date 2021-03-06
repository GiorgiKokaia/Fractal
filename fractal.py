import numpy as np
import pylab as plt
from mpl_toolkits.mplot3d import Axes3D

""" Description from Goodwin & Whitman (2004):

Fractal distributions are generated by defining an ur-cube
with side 2, and placing an ur-parent at the centre of the
3 equal sub-ur-cube. Next, the ur-cube is divided into N_div^3
cubes, and a child is placed at the centre of each sub-cube
(the first generation). Normally we use N_div = 2, in which
case there are 8 sub-cubes and 8 first-generation children.
The probability that a child matures to become a parent in its own
right is (N_div)^(D−3), where D is the fractal dimension; for
lower D, the probability that a child matures to become a par-
ent is lower. Children that do not mature are deleted, along
with the ur-parent. A little noise is then added to the posi-
tions of the remaining children, to avoid an obviously gridded
structure, and they become the parents of the next generation,
each one spawning N_div^3 children (the second generation) at
the centres of N_div^3 equal-volume sub-sub-cubes, and each second-
generation child having a probability (N_div)^(D−3) of maturing to be-
come a parent. This process is repeated recursively until there
is a sufficiently large generation that, even after pruning to im-
pose a spherical envelope of radius 1 within the ur-cube, there
are more children than the required number of stars. Children
are then culled randomly until the required number is left, and
the survivng children are identified with the stars of the cluster.
"""




"""With N_div = 2, index of children:
Child 1: x_low, y_low, z_low
Child 2: x_low, y_low, z_high
Child 3: x_low, y_high, z_low
Child 4: x_low, y_high, z_high
Child 5: x_high, y_low, z_low
Child 6: x_high, y_low, z_high
Child 7: x_high, y_high, z_low
Child 8: x_high, y_high, z_high"""
def fractal_generator(D, N_points):
    
    x0 = np.linspace(-1, 1, 1000)
    y0 = np.linspace(-1, 1, 1000)
    z0 = np.linspace(-1, 1, 1000)
    n_box = 0
    while(n_box==0):
        p = np.random.random(8)
        pp = p > 2**(D-3)
        box = cuber(x0, y0, z0, pp)
        n_box = np.sum(pp)
    while(n_box<N_points):
        p = np.random.random((n_box, 8))
        pp = p > 2**(D-3)
        n_nextgen = np.sum(pp)
        box_temp = np.zeros((n_nextgen, 3, 1000))
        ind_temp = 0
        for i in range(n_box):
            inds = pp[i,:]
            box_temp_temp = cuber(box[i,0,:], box[i,1,:], box[i,2,:], inds)
            for j in range(sum(inds)):
                box_temp[ind_temp,:,:] = box_temp_temp[j,:,:]+np.array([np.ones(1000)*np.random.random()*0.1,
                                                                        np.ones(1000)*np.random.random()*0.1,
                                                                        np.ones(1000)*np.random.random()*0.1])
                ind_temp += 1
        box = box_temp
        n_box = n_nextgen
    return box, n_box
    print("made fractal")


def splitter(x):
    xx = np.split(x, 2)
    x_low = np.linspace(xx[0][0], xx[0][-1], len(x))
    x_high = np.linspace(xx[1][0], xx[1][-1], len(x))
    return x_low, x_high

def cuber(x, y, z, inds):
    x_low, x_high = splitter(x)
    y_low, y_high = splitter(y)
    z_low, z_high = splitter(z)
    box = np.array([[x_low, y_low, z_low], [x_low, y_low, z_high], [x_low, y_high, z_low], [x_low, y_high, z_high],
           [x_high, y_low, z_low], [x_high, y_low, z_high], [x_high, y_high, z_low], [x_high, y_high, z_high]])
    box = box[inds,:,:]
    return box

def point_maker(box, bb):
    points = np.zeros((bb, 3))
    for j in range(bb):
        points[j, 0] = (box[j, 0, 499]+box[j, 0, 500])/2
        points[j, 1] = (box[j, 1, 499]+box[j, 1, 500])/2
        points[j, 2] = (box[j, 2, 499]+box[j, 2, 500])/2
    return points

def pruner(points, N_points):
    d = 0
    while(d==0):
        i_temp = np.sqrt(points[:,0]**2+points[:,1]**2+points[:,2]**2)<1
        pruned_points = points[i_temp,:]
        i = np.full(sum(i_temp), False, dtype="bool")
        i[0:N_points] = True
        np.random.shuffle(i)
        if(d>=N_points):
            d = 1
        else:
            print("still looping")
    return pruned_points[i,:]

    
    
    
