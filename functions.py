from ctypes.wintypes import RGB
import matplotlib.pyplot as plt
from skimage import io
from skimage.color import rgb2gray
import numpy as np
from scipy.ndimage import convolve
from functions import *



sx = np.array([
    [-0.125, -0.25, -0.125],
    [0.0, 0.0, 0.0],
    [0.125, 0.25, 0.125],
])

sy = np.array([ 
    [-0.125,  0.0,  0.125],
    [-0.25,   0.0,  0.25],
    [-0.125,  0.0,  0.125],
])

def least_edgy(e):
    n, m = e.shape
    dirs = np.zeros(e.shape, int)
    least_e = np.zeros(e.shape, np.float64)
    least_e[-1] = e[-1]
    
    for i in range(n - 2, -1, -1):
        for j in range(0, m):
            least_e[i][j] = min(
                least_e[i + 1][j], 
                least_e[i + 1][max(j - 1, 0)],
                least_e[i + 1][min(m - 1, j + 1)],
            ) + e[i][j] 
            dir = 0
            if j > 0 and least_e[i + 1][j - 1] < least_e[i + 1][j]:
                dir = -1
            if j < m - 1 and least_e[i + 1][j + dir] > least_e[i + 1][j + 1]:
                dir = 1
            dirs[i][j] = dir
    return least_e, dirs


def rmPath(dirs, img, minId):
    n,m,d = img.shape
    img_ = np.zeros((n, m - 1, d), np.uint16)
    path = []
    for i in range(n):
        img_[i][ : minId] = img[i][ : minId]
        img_[i][minId : ] = img[i][minId+1 : ]
        # np.delete(img[i], )
        path.append((i, minId))
        minId += dirs[i][minId]
    return img_, path



def shorten(img, n):
    img = io.imread(img)
    count = 0
    edge_vec = []
    e_map = []
    img_vec = []

    for i in range(n):
        greyimg = rgb2gray(img)
        convolved = np.absolute(convolve(greyimg, sx)) + np.absolute(convolve(greyimg, sy))
        least_e, dirs = least_edgy(convolved)
        minId = np.argmin(least_e[0])
        n,m,d = img.shape
        img_ = np.zeros((n, m - 1, d), np.uint16)
        

        for i in range(n):
            img_[i][ : minId] = img[i][ : minId]
            img_[i][minId : ] = img[i][minId + 1 : ]
            least_e[i][minId] = RGB(0, 0, 0)
            minId += dirs[i][minId]
        
        img = img_
        img_vec.append(img)
        edge_vec.append(convolved)
        e_map.append(least_e)
        count += 1
        print(count)
    return img_vec, edge_vec, e_map


