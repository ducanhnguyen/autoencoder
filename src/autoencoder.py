"""
Implementation of AutoEncoder with 1 hidden layer. I try to encode images, and then decode these images to get the original ones.
"""

import matplotlib.pylab as plt
import numpy as np
import sklearn
import tensorflow as tf

import src.utils as utils


class AutoEncoder:
    def __init__(self, M):
        """
        :param M: Number of units in the hidden layer
        """
        self.M = M

    def fit(self, Xtrain, learning_rate=0.01, epoch=100, batch_size=50):
        N, D = Xtrain.shape
        tf_X = tf.placeholder(dtype=tf.float32)

        self.tf_W = tf.Variable(dtype=tf.float32,
                                initial_value=tf.random.normal(shape=(D, self.M), mean=0,
                                                               stddev=tf.math.sqrt(1 / D)))  # xavier initialization
        self.tf_bh = tf.Variable(dtype=tf.float32, initial_value=tf.random.normal(shape=(self.M,)))
        self.tf_bo = tf.Variable(dtype=tf.float32, initial_value=tf.random.normal(shape=(D,)))

        tf_Xhat = self.forward(tf_X)

        # Two ways to define cost function: (1) least square, or (2) sigmoid cross entropy
        # Use traditional cross entropy raises an issue if X_hat = 0 or 1

        # tf_cost = tf.math.reduce_sum(tf.square(tf_X - tf_Xhat))

        tf_cost = tf.reduce_mean(
            tf.nn.sigmoid_cross_entropy_with_logits(
                labels=tf_X,
                logits=self.forwardLogits(tf_X),
            )
        )

        train_op = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(tf_cost)

        with tf.Session() as session:
            session.run(tf.global_variables_initializer())

            iteration = 0
            iterations = []
            costs = []

            nBatches = np.math.ceil(N * 1.0 / batch_size)

            for i in range(epoch):
                Xtrain = sklearn.utils.shuffle(Xtrain)

                for j in range(nBatches):

                    # mini-batch gradient descent
                    if j == nBatches:
                        session.run(train_op, feed_dict={tf_X: Xtrain[j * nBatches:N]})
                    else:
                        session.run(train_op, feed_dict={tf_X: Xtrain[j * nBatches:(j + 1) * nBatches]})

                    iteration += 1

                cost = session.run(tf_cost, feed_dict={tf_X: Xtrain})
                costs.append(cost)
                print("Epoch " + str(i) + "/ Iteration " + str(iteration) + "/ cost = " + str(cost))
                iterations.append(iteration)

            self.plotCost(iterations, costs)

            # show images
            Xhat = session.run(tf_Xhat, feed_dict={tf_X: Xtrain})
            self.plotComparison(Xtrain[0], Xhat[0])
            self.plotComparison(Xtrain[1], Xhat[1])
            self.plotComparison(Xtrain[2], Xhat[2])

    def forwardLogits(self, X):
        """
        Use in cost function
        :param X:
        :return:
        """
        tf_Z = tf.nn.sigmoid(tf.math.add(tf.matmul(a=X, b=self.tf_W), self.tf_bh))
        Xhat_net = tf.math.add(tf.matmul(a=tf_Z, b=tf.transpose(self.tf_W)), self.tf_bo)
        return Xhat_net

    def forward(self, X):
        tf_Z = tf.nn.sigmoid(tf.math.add(tf.matmul(a=X, b=self.tf_W), self.tf_bh))
        X_hat = tf.nn.sigmoid(tf.math.add(tf.matmul(a=tf_Z, b=tf.transpose(self.tf_W)), self.tf_bo))
        return X_hat

    def plotComparison(self, x, xhat):
        # original
        plt.subplot(1, 2, 1)
        plt.imshow(x.reshape(28, 28), cmap='gray')
        plt.title('Original')

        # reconstruction
        plt.subplot(1, 2, 2)
        plt.imshow(xhat.reshape(28, 28), cmap='gray')
        plt.title('Reconstructed')
        plt.show()

    def plotCost(self, iterations, costs):
        """
        Visualization
        :param scores: 1-D dimension of float numbers
        :param iterations:  1-D dimension of integer numbers
        :return:
        """
        plt.plot(iterations, costs, label="cost over iteration")
        plt.xlabel('Iteration')
        plt.ylabel('Cost')
        plt.title('Autoencoder (data = digit-recognizer)')
        plt.grid(True)
        plt.legend()
        plt.show()


def main():
    X, y = utils.readTrainingDigitRecognizer('../data/digit-recognizer/train.csv')
    ae = AutoEncoder(M=300)
    ae.fit(X)


main()
