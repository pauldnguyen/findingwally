# findingwally

Finding Wally Web Application

An adaption of the work done by [Tadej Magajna](https://github.com/tadejmagajna/HereIsWally) as a web application on the PythonAnywhere webhosting service.

# Languages

Python, JavaScript, HTML, CSS

# Requirements

The images, annotations, model checkpoint, and trained model from [Tadej Magajna](https://github.com/tadejmagajna/HereIsWally); or alternatively, create separate similar images, annotations, to retrained the model derived from his checkpoint, or to trained a model from scratch. For simply implementing a Web application to predict Wally's location (and not training a new model), only a frozen inference graph (the trained model) is needed, and found on his repository.

[TensorFlow Object Detection API](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md) and its dependencies for both training and prediction

N.B. It does seem however, that the API has been misfunctioning for some time now (cf. https://github.com/tensorflow/models/issues/2952). In which case, the frozen_inference_graph.py file from Tadej Magajna can be your starting substitute, as I have in the online implementation of the Web app.

To generate detection plots:

[matplotlib](https://github.com/matplotlib/matplotlib)

[NumPy](https://github.com/numpy/numpy)

Backend framework:

[Django](https://github.com/django/django)

Frontend:

Bootstrap, provided in this repository as a min file

jQuery, provided in this repository as a min file
