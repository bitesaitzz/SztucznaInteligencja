import numpy as np
import matplotlib.pyplot as plt

from data import get_data, inspect_data, split_data

data = get_data()
inspect_data(data)

train_data, test_data = split_data(data)

# Simple Linear Regression
# predict MPG (y, dependent variable) using Weight (x, independent variable) using closed-form solution
# y = theta_0 + theta_1 * x - we want to find theta_0 andtheta_1 parameters that minimize the prediction error

# We can calculate the error using MSE metric:
# MSE = SUM (from i=1 to n) (actual_output - predicted_output) ** 2

# get the columns
y_train = train_data['MPG'].to_numpy()
x_train = train_data['Weight'].to_numpy()

y_test = test_data['MPG'].to_numpy()
x_test = test_data['Weight'].to_numpy()

# TODO: calculate closed-form solution
theta_best = [0, 0]
X = np.ones(len(x_train))
X = np.c_[X, x_train]
Y = np.c_[y_train]
theta_best = (np.linalg.inv(X.T.dot(X))).dot(X.T).dot(Y)
print(theta_best)

# TODO: calculate error
#MSE = SUM (from i=1 to n) (actual_output - predicted_output) ** 2
actual_output = y_test
predicted_output = theta_best[1]*x_test+theta_best[0]
MSE = np.mean((actual_output-predicted_output)**2)
print(MSE)
# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
y = float(theta_best[0]) + float(theta_best[1]) * x
plt.plot(x, y)
plt.scatter(x_test, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()

# TODO: standardization
x_train_temp = x_train
y_train_temp = y_train
x_train = (x_train - np.mean(x_train))/np.std(x_train)
y_train = (y_train - np.mean(y_train))/np.std(y_train)



# TODO: calculate theta using Batch Gradient Descent
X = np.ones(len(x_train))
X = np.c_[X, x_train]
Y = np.c_[y_train]
learning_rate = 0.01
max_epochs = 1000
m = len(x_train)
theta = np.random.rand(2,1)
for epoch in range(max_epochs):
    grad = 2/m*X.T.dot((X.dot(theta)-Y))
    theta -= learning_rate*grad
    actual_output = y_train
    predicted_output = theta[1]*x_train+theta[0]
    MSE = np.mean((actual_output-predicted_output)**2)
    print(MSE)


theta = np.array(theta.T)[0]

print(theta)
theta_best = theta
x_train = x_train_temp
y_train = y_train_temp
# TODO: calculate error
x_test = (x_test - np.mean(x_train))/np.std(x_train)
y_test = (y_test - np.mean(y_train))/np.std(y_train)




# actual_output = y_test
# predicted_output = theta_best[1]*x_test+theta_best[0]
# MSE = np.mean((actual_output-predicted_output)**2)

actual_output = y_test
actual_output_restan = actual_output*np.std(y_train_temp)+np.mean(y_train_temp)
predicted_output = theta_best[1]*x_test+theta_best[0]
predicted_output_restandartize = predicted_output*np.std(y_train_temp)+np.mean(y_train_temp)
MSE = np.mean((actual_output_restan-predicted_output_restandartize)**2)
print(MSE)

# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
y = float(theta_best[0]) + float(theta_best[1]) * x
plt.plot(x, y)
plt.scatter(x_test, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()