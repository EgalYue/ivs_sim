#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 14:58:01 2017

@author: lracuna
"""
import autograd.numpy as np

def get_matrix_conditioning_number(M):
 return  np.linalg.norm(M,2)*np.linalg.norm(np.linalg.pinv(M),2)

def h_norm2d(x):
  #Normalize points
  for i in range(3):
    x[i] = x[i]/x[2]
  return x

def d(x1, x2):
  return np.linalg.norm(h_norm2d(x1)-h_norm2d(x2))

def sym_transfer_error(Xo,Xi,H):
  """Symetric transfer error
  Xo: Object points in 2D Homogeneous Coordinates (3xn)
  Xi: Image points in 2D Homogeneous Coordinates (3xn)
  """
  Xo = np.copy(Xo)
  Xi = np.copy(Xi)
  H = np.copy(H)
  error1 = d(Xi,np.dot(H,Xo))
  error2 = d(Xo,np.dot(np.linalg.inv(H),Xi))
  return error1 + error2

def transfer_error(Xo,Xi,H):
  """transfer error including normalization
  Xo: Object points in 2D Homogeneous Coordinates (3xn)
  Xi: Image points in 2D Homogeneous Coordinates (3xn)
  """
  Xo = np.copy(Xo)
  Xi = np.copy(Xi)
  H = np.copy(H)
  return d(Xi,np.dot(H,Xo))

def algebraic_distance(Xo,Xi,H):
  """
  Xi point measured in the image
  Xo real value of the model point
  H an estimated homography
  as defined in Multiple View Geometry in Computer vision
  """
  Xo = np.copy(Xo)
  Xi = np.copy(Xi)
  H = np.copy(H)
#  a = np.cross(Xi,np.dot(H,Xo))
#  return a[0]**2 + a[1]**2
  Xio = np.dot(H,Xo)
  return (Xio[0]*Xi[2]-Xi[0]*Xio[2])**2 + (Xi[1]*Xio[2] - Xi[2]*Xio[1])**2

def geometric_distance(Xo,Xi,H):
  """
  Xi point measured in the image
  Xo real value of the model point
  H an estimated homography
  as defined in Multiple View Geometry in Computer vision
  """
  Xo = np.copy(Xo)
  Xi = np.copy(Xi)
  H = np.copy(H)
  Xio = np.dot(H,Xo)
  return np.sqrt((Xi[0]/Xi[2] - Xio[0]/Xio[2])**2+(Xi[1]/Xi[2] - Xio[1]/Xio[2])**2)

def geometric_distance_points(Xo,Xi,H):
  geom_distances = list()
  for i in range(Xo.shape[1]):
      geom_distances.append(geometric_distance(Xo[:,i],Xi[:,i],H))
  return np.mean(geom_distances)


def volker_metric(A):
  A = np.copy(A)

  # nomarlize each row
  #A = A/np.linalg.norm(A,axis=1, ord = 1, keepdims=True)
  for i in range(A.shape[0]):
    squared_sum = 0
    for j in range(A.shape[1]):
      squared_sum += np.sqrt(A[i,j]**2)
    A[i,:] = A[i,:] / squared_sum

  # compute the dot product
  As = np.dot(A,A.T)

  # we are interested only on the upper top triangular matrix coefficients
  metric = 0
  start = 1
  for i in range(As.shape[0]):
    for j in range(start,As.shape[0]):
      metric = metric +  As[i,j]**2
    start = start +1


  #An alternative would be to use only the coefficients which correspond
  # to different points.
  #metric = np.sqrt(np.sum(As[[0,2,4,6],[1,3,5,7]]**2))

  #X vs X
  metric = np.sum(As[[0,0,0,2,2,4],[2,4,6,4,6,6]]**2)

  #Y vs Y
  metric = metric + np.sum(As[[1,1,1,3,3,5],[3,5,7,5,7,7]]**2)

  return  metric

def calculate_A_matrix(Xo, Xi):
  """ Calculate the A matrix for the DLT algorithm:  A.H = 0
  Inputs:
    Xo: Object points in 3D Homogeneous Coordinates (3xn), Z coorinate removed
    since the points should be on a plane

    Xi: Image points in 2D Homogeneous Coordinates (3xn)
  """
  Npts = Xo.shape[1]
  A = np.zeros((2*Npts,9))
  O = np.zeros(3)

  for i in range(0, Npts):
      X = Xo[:,i].T
      u = Xi[0,i]
      v = Xi[1,i]
      w = Xi[2,i]
      A[2*i,:] = np.array([O, -w*X, v*X]).reshape(1, 9)
      A[2*i+1,:] = np.array([w*X, O, -u*X]).reshape(1, 9)
  return A