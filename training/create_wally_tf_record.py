# Simple script to create a TF record specifically for the Finding Wally / Here is Wally data

import csv
import os
import tensorflow as tf
from object_detection.utils import dataset_util

# Initialize variables

image_format = b"jpg"
classes = [1]

filename = None
width = None
height = None
classes_text = ["waldo".encode('utf8')]
xmins = []
ymins = []
xmaxs = []
ymaxs = []

encoded_jpg = None

# Give paths for locations of the image directory and the annotations CSV
# The annotation CSV has information in the order of filename, width, height, class, xmin, ymin, xmax, ymax

annotations_path = "PATH_TO_ANNOTATIONS/annotations.csv"
images_path = "PATH_TO_IMAGES"

# Name of new file

tfrecord_filename = "FILE_NAME.tfrecord"

# Read annotations and write features

writer = tf.python_io.TFRecordWriter(tfrecord_filename)
with open(annotations_path, newline="") as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader, None)
    for row in reader:
        filename = row[0]
        width = int(row[1])
        height = int(row[2])
        # classes_text is already "waldo" throughout
        xmins = [float(row[4]) / width]
        ymins = [float(row[5]) / height]
        xmaxs = [float(row[6]) / width]
        ymaxs = [float(row[7]) / height]
        
        imgage_path = os.path.join(images_path, filename)
        encoded_image_data = tf.gfile.FastGFile(imgage_path, "rb").read()

        tf_example = tf.train.Example(features=tf.train.Features(feature={
            "image/height": dataset_util.int64_feature(height),
            "image/width": dataset_util.int64_feature(width),
            "image/filename": dataset_util.bytes_feature(filename.encode('utf8')),
            "image/source_id": dataset_util.bytes_feature(filename.encode('utf8')),
            "image/encoded": dataset_util.bytes_feature(encoded_image_data),
            "image/format": dataset_util.bytes_feature(image_format),
            "image/object/bbox/xmin": dataset_util.float_list_feature(xmins),
            "image/object/bbox/xmax": dataset_util.float_list_feature(xmaxs),
            "image/object/bbox/ymin": dataset_util.float_list_feature(ymins),
            "image/object/bbox/ymax": dataset_util.float_list_feature(ymaxs),
            "image/object/class/text": dataset_util.bytes_list_feature(classes_text),
            "image/object/class/label": dataset_util.int64_list_feature(classes),
        }))

        writer.write(tf_example.SerializeToString())

writer.close()