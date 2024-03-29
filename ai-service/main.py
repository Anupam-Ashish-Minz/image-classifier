import sys
import math
import socket
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from PIL import Image


def train_with_keras():
    num_classes = 20
    input_shape = (28, 28, 1)

    (x_train, y_train), (x_test, y_test) = mnist.npz
    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255

    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)

    y_train = keras.utils.to_categorical(y_train, num_classes)

    model = keras.Sequential(
        [
            keras.Input(shape=input_shape),
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation="relu"),
            layers.Dense(num_classes, activation="softmax"),
        ]
    )



def read_data():
    with np.load("mnist.npz") as f:
        x, y = f["x_train"], f["y_train"]

    # change data from int between 0 and 255 to float between 0 and 1
    x = x.astype("float32") / 255

    # reshape the new sample to 60_000, 784 for x
    x = np.reshape(
        x,
        (x.shape[0], x.shape[1] * x.shape[2]),
    )

    # transform y form label number to output array collection of 0's and 1's
    # 10 per image
    y = np.eye(10)[y]

    return x, y


def read_testing_data():
    with np.load("mnist.npz") as f:
        x, y = f["x_test"], f["y_test"]
    x = x.astype("float32") / 255
    x = np.reshape(
        x, (
            x.shape[0],
            x.shape[1] * x.shape[2]
        )
    )

    y = np.eye(10)[y]

    return x, y


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def init_model():
    with np.load("trained_model.npz") as f:
        w1 = f["w1"]
        b1 = f["b1"]
        w2 = f["w2"]
        b2 = f["b2"]

    def forward_prop(x):
        z1 = w1.dot(x) + b1
        h = sigmoid(z1)

        z2 = w2.dot(h) + b2
        o = sigmoid(z2)
        return o

    return forward_prop


def train():
    x_train, y_train = read_data()

    epochs = 5
    learning_rate = 0.01

    nr_correct = 0

    w1 = np.random.uniform(-0.5, 0.5, (20, 784))
    w2 = np.random.uniform(-0.5, 0.5, (10, 20))
    b1 = np.random.rand(20, 1)
    b2 = np.random.rand(10, 1)

    for epoch in range(epochs):
        for x, y in zip(x_train, y_train):

            # make x and y both single dimention matix not array
            x.shape += (1,)
            y.shape += (1,)

            z1 = w1.dot(x) + b1
            h = sigmoid(z1)

            z2 = w2.dot(h) + b2
            o = sigmoid(z2)

            # backpropogation for output to hidden layer
            # mean squared error
            # err = np.mean((o - y)**2)

            # max value in actual output and max value in expected output
            nr_correct += int(np.argmax(o) == np.argmax(y))

            # derivitive of mean squared error with respect to output
            # shape 10x1
            _err = 2 * (o - y)
            # derivitive of sigmoid with respect to total input(z2)
            # shape 10x1
            _sig_o = (o * (1 - o))
            # derivitive of total input(z2) with respect to weight
            # shape 20x1
            _wei = h

            # loss_w = learning_rate * np.transpose((_err * _sig), h)
            # note: x * y where x and y are both matrices results in
            # submission(x_i_j * y_i_j) i.e. every field in the first matrix is
            # multiplied with the corresponding field in the second matrix
            loss_o_w = np.dot((_err * _sig_o), np.transpose(h))
            loss_o_b = _err * _sig_o

            w2 -= learning_rate * loss_o_w
            b2 -= learning_rate * loss_o_b

            # backpropogation for hidden to input layer
            _sig_h = (h * (1 - h))
            loss_h_w = np.dot(
                np.transpose(w2).dot(_err * _sig_o) * _sig_h,
                np.transpose(x)
            )
            loss_h_b = np.transpose(w2).dot(_err * _sig_o) * _sig_h

            w1 -= learning_rate * loss_h_w
            b1 -= learning_rate * loss_h_b

        print(
            f"Epoch {epoch} Training Acc: {round((nr_correct / x_train.shape[0]) * 100, 2)}%")
        nr_correct = 0

    # save
    # f_out = open("trained_model.npz", "w")
    np.savez_compressed("trained_model.npz", w1=w1, b1=b1, w2=w2, b2=b2)


def testing():
    x_test, y_test = read_testing_data()
    nr_correct = 0

    forward_prop = init_model()

    total_confid = 0
    for x, y in zip(x_test, y_test):
        x.shape += (1,)
        y.shape += (1,)

        o = forward_prop(x)

        nr_correct += int(np.argmax(o) == np.argmax(y))
        if np.argmax(o) == np.argmax(y):
            total_confid += round(float(o[o.argmax()] * 100), 2)

    print(
        f"Testing Acc: {round((nr_correct / x_test.shape[0]) * 100, 2)}%")
    print("avg confidence", total_confid/len(x_test))


def test_image(path):
    im = Image.open(path)
    pix_val = list(im.getdata())
    pix_val = [math.ceil((i+j+k)/3) for (i, j, k) in pix_val]
    x = np.matrix(pix_val).reshape(784, 1)
    x = x.astype("float32") / 255

    model = init_model()
    o = model(x)
    ans = int(o.argmax()) + 2
    confidence = round(float(o[o.argmax()] * 100), 2)
    # print("image of {} with confidence of {} %".format(o.argmax()+1, confidence))
    return ans, confidence


def test_png_imgs():
    print("white on black images")

    # ans, confidenece = test_image("images/2.png")
    # print("ans = {}, ai_ans = {}, confidence = {}".format(2, ans, confidenece))
    ans, confidenece = test_image("images/5.png")
    print("ans = {}, ai_ans = {}, confidence = {}".format(5, ans, confidenece))
    ans, confidenece = test_image("images/8.png")
    print("ans = {}, ai_ans = {}, confidence = {}".format(8, ans, confidenece))


def run():
    hostname = "localhost"
    port = 5533

    forward_prop = init_model()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((hostname, port))
    s.listen(5)
    numbers = list(range(10))

    print("server listening on port localhost", port)
    while True:
        c, addr = s.accept()
        x = np.array(list(c.recv(784)))

        x.shape += (1,)

        o = forward_prop(x)
        i = np.argmax(o)

        c.send(numbers[i].to_bytes(2, 'big'))

        c.close()


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "--server":
        run()
    elif sys.argv[1] == "--train":
        train()
    elif sys.argv[1] == "--test":
        testing()
        test_png_imgs()
    else:
        print("no such option", sys.argv[1])
