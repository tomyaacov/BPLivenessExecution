# import numpy
# a = numpy.load("lane-bridge/save-00065094/replay-buffer" + '/states.npy')
# numpy.savetxt("test_folder/states.csv", a, delimiter=",")
# a = numpy.load("lane-bridge/save-00065094/replay-buffer" + '/actions.npy')
# numpy.savetxt("test_folder/actions.csv", a, delimiter=",")
# a = numpy.load("lane-bridge/save-00065094/replay-buffer" + '/rewards.npy')
# numpy.savetxt("test_folder/rewards.csv", a, delimiter=",")
# a = numpy.load("lane-bridge/save-00065094/replay-buffer" + '/terminal_flags.npy')
# numpy.savetxt("test_folder/terminal_flags.csv", a, delimiter=",")
# a = numpy.load("lane-bridge/save-00065094/replay-buffer" + '/is_last.npy')
# numpy.savetxt("test_folder/is_last.csv", a, delimiter=",")

import numpy as np
import os
s = np.load("lane-bridge/save-00067484/replay-buffer" + '/states.npy')
a = np.load("lane-bridge/save-00067484/replay-buffer" + '/actions.npy')
r = np.load("lane-bridge/save-00067484/replay-buffer" + '/rewards.npy')
t = np.load("lane-bridge/save-00067484/replay-buffer" + '/terminal_flags.npy')
i = np.load("lane-bridge/save-00067484/replay-buffer" + '/is_last.npy')

def unique_rows(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))

s = s[:67000,:]
a = a[:67000]
r = r[:67000]
t = t[:67000]
i = i[:67000]

print(s.shape)
print(a.reshape((-1,1)).shape)
print(r.reshape((-1,1)).shape)
s = s[i == False]
a = a[i == False]
r = r[i == False]
t = t[i == False]
i = i[i == False]
# # u1 = np.concatenate((x,a.reshape((-1,1))), axis=1)
u = np.concatenate((s,a.reshape((-1,1)),r.reshape((-1,1)),t.reshape((-1,1)),i.reshape((-1,1))), axis=1)
u1 = np.concatenate((s,a.reshape((-1,1))), axis=1)
print(u.shape)
print(unique_rows(u1).shape)
print(unique_rows(u).shape)
u = unique_rows(u)
s = u[:,:3]
a = u[:,3]
r = u[:,4]
t = u[:,5]
i = u[:,6]

folder_name = "/Users/tomyaacov/university/BPLivenessRL/test_folder"
if not os.path.isdir(folder_name):
    os.mkdir(folder_name)

np.save(folder_name + '/actions.npy', a)
np.save(folder_name + '/states.npy', s)
np.save(folder_name + '/rewards.npy', r)
np.save(folder_name + '/terminal_flags.npy', t)
np.save(folder_name + '/is_last.npy', i)
# print(u2.shape)
# print(unique_rows(u1).shape)
# print(unique_rows(u2).shape)
# data = unique_rows(u2)
# x = data[:,0:4]
# y = data[:,4]
# print(x.shape)
# print(y.shape)

# from sklearn import linear_model
# reg = linear_model.LinearRegression()
# from sklearn.metrics import mean_squared_error
# print(mean_squared_error(y, np.zeros((102,))))
# reg.fit(x, y)
# print(mean_squared_error(y, reg.predict(x)))
# np.savetxt("test_folder/data.csv", u2, delimiter=",")