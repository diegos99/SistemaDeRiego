import pandas as pd

dataset = pd.read_csv(
    "data.csv", encoding='utf-8', header=None)

# Neural network
X = np.asarray(dataset.iloc[:, 1:5]).astype(np.float32)
Y = np.asarray(dataset.iloc[:, 5]).astype(np.float32)

# select test data / last ten items from de data set
X_TEST = [[54,26.9,10,23], [52,27,10,27], [51,27.2,10,27], [49,27.2,11,24]]

# define model
model = Sequential()

# define activation functions
model.add(Dense(10, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# compile model binary_crossentropy
model.compile(loss='mean_squared_error',
              optimizer='adam', metrics=['accuracy'])

# fit model
model.fit(X, Y, epochs=500, batch_size=20)

# evaluate model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

Y_TRAIN = model.predict(X_TEST)

print(np.asarray(Y_TRAIN).astype(np.float32))

