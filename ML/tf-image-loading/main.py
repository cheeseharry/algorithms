#!/usr/bin/env python

import tensorflow as tf
from PIL import Image
import numpy as np

#  list of files to read
filenames = ['Aurelia-aurita-3.jpg']
filename_queue = tf.train.string_input_producer(filenames)

reader = tf.WholeFileReader()
key, value = reader.read(filename_queue)

my_img = tf.image.decode_jpeg(value)

init_op = tf.initialize_all_variables()
with tf.Session() as sess:
    sess.run(init_op)

    # Start populating the filename queue.
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)

    for i in range(len(filenames)):
        image = my_img.eval()  # image is an image tensor

    # Create tf.train.Example
    bytes_list = tf.train.BytesList(value=image.tobytes())
    feat = tf.train.Feature(bytes_list=bytes_list)
    ex = tf.train.Example(features=tf.train.Features(feature={'image': feat}))

    # Write tf.train.Example
    writer = tf.python_io.TFRecordWriter("example.tfrecords")
    writer.write(ex.SerializeToString())

    # Read tf.train.Example
    # TODO

    print(image.shape)
    im = Image.fromarray(np.asarray(image))
    im.show()

    coord.request_stop()
    coord.join(threads)
