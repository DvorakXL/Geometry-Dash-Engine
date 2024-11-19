import numpy as np

#Projection matrix 2x3
def ProjectionMatrix():
    return np.array([
        [1,0,0],
        [0,1,0]
    ])

def ScaleMatrix(scale):
    return np.array([
        [scale, 0, 0],
        [0, scale, 0],
        [0, 0, scale]
    ])

def RotationMatrixX(angle):
    return np.array([
        [1, 0, 0],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle), np.cos(angle)]
    ])

def RotationMatrixY(angle):
    return np.array([
        [np.cos(angle), 0, -np.sin(angle)],
        [0, 1, 0],
        [np.sin(angle), 0, np.cos(angle)]
    ])

def RotationMatrixZ(angle):
    return np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])