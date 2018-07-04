import base64
from django.http import JsonResponse
from django.shortcuts import render
import io
import matplotlib
matplotlib.use("Agg") # Required to redirect locally
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import tensorflow as tf
from urllib.parse import urlparse
import urllib.request
from .models import URLImage

#   Helper functions for the view functions

def draw_box(box, image_np):
    '''
    This function a NumPy array for a box, and a NumPy array for an image and
    returns a matplotlib pyplot figure and matplotlib pyplot axes indicating a
    box drawn around those coordinates.
    '''

    #   Expand the box by 50%
    box += np.array([-(box[2] - box[0]) / 2,
                     -(box[3] - box[1]) / 2,
                     (box[2] - box[0]) / 2,
                     (box[3] - box[1]) / 2])

    #   Create a large figure to capture all the data
    fig = plt.figure(figsize = (8. * image_np.shape[1] / max(image_np.shape[0], image_np.shape[1]),
                                8. * image_np.shape[0] / max(image_np.shape[0], image_np.shape[1])))

    ax = plt.Axes(fig, [0., 0., 1., 1.])
    fig.add_axes(ax)

    #   Draw blurred boxes around the box
    ax.add_patch(patches.Rectangle((0, 0),
                                   box[1] * image_np.shape[1],
                                   image_np.shape[0],
                                   linewidth = 0,
                                   edgecolor = "none",
                                   facecolor = "w",
                                   alpha=2. / 3.))
    ax.add_patch(patches.Rectangle((box[3] * image_np.shape[1], 0),
                                   image_np.shape[1],
                                   image_np.shape[0],
                                   linewidth = 0,
                                   edgecolor = "none",
                                   facecolor = "w",
                                   alpha = 2. / 3.))
    ax.add_patch(patches.Rectangle((box[1] * image_np.shape[1], 0),
                                   (box[3] - box[1]) * image_np.shape[1],
                                   box[0] * image_np.shape[0],
                                   linewidth = 0,
                                   edgecolor = "none",
                                   facecolor = "w",
                                   alpha = 2. / 3.))
    ax.add_patch(patches.Rectangle((box[1] * image_np.shape[1], box[2] * image_np.shape[0]),
                                   (box[3] - box[1]) * image_np.shape[1],
                                   image_np.shape[0],
                                   linewidth = 0,
                                   edgecolor = "none",
                                   facecolor = "w",
                                   alpha = 2. / 3.))
    return fig, ax

def load_image_into_numpy_array(image):
    '''
    This function takes an image, and returns a Numpy array representation of
    that image.
    '''

    #   Convert 4 channel images into a RGB image for consistency
    if (image.mode == "RGBA") or (image.mode == "CMYK"):
        image = image.convert("RGB")

    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

def open_url_http(url):
    '''
    This function takes a url string and returns an open request from that url.
    '''

    #   Include http prefix if the url omits it
    parse_object = urlparse(url)
    if not parse_object.scheme:
        url = "http://" + url

    #   Request and open the url
    url_request = urllib.request.Request(url)
    return urllib.request.urlopen(url_request)


def go_find_wally(working_graph, url):
    '''
    This function takes a TensorFlow graph and a url string, and returns a Boolean
    indicating if Wally is found and shows an image with his location.
    '''

    tf_config = tf.ConfigProto(intra_op_parallelism_threads = 1,
                               inter_op_parallelism_threads = 1,
                               device_count={"CPU": 1})

    with tf.Session(config = tf_config, graph = working_graph) as sess:

        found = False

        #   Loading variables
        response = open_url_http(url)
        image_np = load_image_into_numpy_array(Image.open(response))
        image_tensor = working_graph.get_tensor_by_name("image_tensor:0")
        boxes = working_graph.get_tensor_by_name("detection_boxes:0")
        scores = working_graph.get_tensor_by_name("detection_scores:0")
        classes = working_graph.get_tensor_by_name("detection_classes:0")
        num_detections = working_graph.get_tensor_by_name("num_detections:0")

        #   Actual detection
        (boxes, scores, classes, num_detections) = sess.run(
            [boxes, scores, classes, num_detections],
            feed_dict = {image_tensor: np.expand_dims(image_np, axis = 0)})

        #   If there is a high enough largest score, draw a box around the prediction
        #   and indicate that Wally is found; otherwise, return an opaque image
        if scores[0][0] > 0.05:
            fig, ax = draw_box(boxes[0][0], image_np)
            found = True
        else:
            fig, ax = draw_box(boxes[0][0] * 0, image_np)

        #   Show image and return if found or not
        ax.imshow(image_np)
        plt.axis("off")
        plt.show()
        return found

#   View functions for the different Webpages on Finding Wally

def error_500(request):
    '''
    This function renders a custom 500 error page telling the user about the
    limitations of the free PythonAnywhere site.
    '''
    data = {}
    return render(request, "error_500.html", data)

def more_information(request):
    '''
    This function renders a request for the More Information page.
    '''

    return render(request, "more_information.html")

def home(request):
    '''
    This function renders a request for the Home page with a variable for all
    urls of the images in the Find Wally carousel.
    '''

    images = None

    #   If there is a POST request to add an image, get the submitted url,
    #   create a URLImage object, and add it to the collection
    if request.POST.get("url_image"):

        #   Get and open the url
        url_image = request.POST.get("url_image")
        response = open_url_http(url_image)

        #   Create the object if the url points to an image
        r = dict(response.getheaders())
        if "image" in r["Content-Type"]:
            URLImage.objects.get_or_create(url = url_image)

    images = URLImage.objects.all()

    #   Render the Home page with a list of all the image urls as a variable
    return render(request, "home.html", {
        "images": images,
    })

def find_wally(request):
    '''
    This function renders a request for a caption and image indicating the
    location of Wally from a search. (This reponse is found within a modal from
    clicking the FIND WALLY button.)
    '''

    #   Location of image and neural network
    image_url = request.GET.get("current_url")
    model_path = "/home/findingwally/mysite/findingwally/trained_model/frozen_inference_graph.pb"

    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()

        #   Read the frozen inference graph
        with tf.gfile.GFile(model_path, "rb") as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name = "")

        #   Find Wally, show image, and return Boolean
        is_found = go_find_wally(detection_graph, image_url)

    # Redirect the figure to a BytesIO object
    f = io.BytesIO()
    plt.savefig(f, format="png", facecolor = (0.95, 0.95, 0.95), dpi = 400) # High DPI to keep details, around 4K DPI
    plt.clf()
    encoded_img = base64.b64encode(f.getvalue()).decode("utf-8").replace("\n", "")
    f.close()

    # Add the contents of the BytesIO object to the response as a PNG
    if is_found:
        return JsonResponse('<div id="caption-here"></div> <img src="data:image/png;base64,%s" id="resultImage" class="modal-content"/>' % encoded_img, safe=False)
    else:
        return JsonResponse('<div id="caption-not-here"></div> <img src="data:image/png;base64,%s" id="resultImage" class="modal-content"/>' % encoded_img, safe=False)
