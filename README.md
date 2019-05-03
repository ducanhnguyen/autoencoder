# autoencoder
Autoencoder is used widely in dimensionality reduction. Unlike PCA, it is a non-linear transformation technique.

An autoencoder network only has one hidden layer in which the number of hidden units is smaller than the number of features. Autoencoder tries to represent the input into a more compact representation. The input and the output of an autoencoder network are the same.

<img src="https://github.com/ducanhnguyen/autoencoder/blob/master/img/autoencoder.png" width="350">

### Stacked autoencoder

Scientists tend to use more than one layer of autoencoder to train the model, which is known as stacked autoencoder or deep autoencoder. This greedy layerwise approach for pretraining a deep network works by training each layer in turn.

<img src="https://github.com/ducanhnguyen/autoencoder/blob/master/img/deep_autoencoder.png" width="450">

### Environment
Mac osx, jre 1.8, pycharm 2018

### Experiments

I try to encode images, then restore them using autoencoder.

<img src="https://github.com/ducanhnguyen/autoencoder/blob/master/img/cost.png" width="550">

The left image is the original one. The right image is the reconstructed image.

<img src="https://github.com/ducanhnguyen/autoencoder/blob/master/img/0_reconstruction.png" width="350">
<img src="https://github.com/ducanhnguyen/autoencoder/blob/master/img/9_reconstruction.png" width="350">
<img src="https://github.com/ducanhnguyen/autoencoder/blob/master/img/8_reconstruction.png" width="350">
