# findingwally

Finding Wally Web Application

URL: http://findingwally.pythonanywhere.com

A facial-recognition (image detection) web-application using a convolutional neural network to solve puzzles from the children’s picture-book series Where’s Wally.

An adaption of the work done by [Tadej Magajna](https://github.com/tadejmagajna/HereIsWally) as a web application on the PythonAnywhere webhosting service.

# Languages

Python 3.5+, JavaScript, HTML, CSS

# Requirements

The images, annotations, model checkpoint, and trained model from [Tadej Magajna](https://github.com/tadejmagajna/HereIsWally); or alternatively, you can create separate similar images and annotations to retrain the model derived from his checkpoint, or to train a model from scratch. For simply implementing a Web application to predict Wally's location (and not training a new model), only a frozen inference graph (the trained model) is needed, and found on his repository. His images and annotations come from [Valentino Constantinou](https://github.com/vc1492a/Hey-Waldo).

[TensorFlow Object Detection API](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md) and its dependencies for both training and prediction; TensorFlow 1.3+. Read Tadej's post about his work to get started [here](https://towardsdatascience.com/how-to-find-wally-neural-network-eddbb20b0b90). A similar explination on the use of TensorFlow's Object Detection API by Dat Tran can be found [here](https://towardsdatascience.com/how-to-train-your-own-object-detector-with-tensorflows-object-detector-api-bec72ecfe1d9).

N.B. It does seem however, that the API has been malfunctioning for some time now. It appears to be training (in this case, a transfer learning from a pretrained model, with progressively decreasing losses as expected), but in reality, training through the Object Detection API incurs a deleterious effect on the parameters of the model (cf. the issue as described here https://github.com/tensorflow/models/issues/2952). In which case, the frozen_inference_graph.py file from Tadej Magajna can be an initial substitute to get you started assembling a similar Web app.

To generate detection plots:

[matplotlib](https://github.com/matplotlib/matplotlib)

[NumPy](https://github.com/numpy/numpy)

PIL

Backend framework:

[Django](https://github.com/django/django)

A web hosting service; I used [PythonAnywhere.com](https://www.pythonanywhere.com/), and followed its provided procedures to set up the website. 

Frontend:

Bootstrap, provided in this repository as a min file

jQuery, provided in this repository as a min file
