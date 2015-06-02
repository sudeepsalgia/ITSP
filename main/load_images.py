import cv2
# function to load images of letters and numbers from ITSP_image folder


def load_display_images(images):
    print "loading images"
    letters = [chr(i) for i in range(65, 90) if i != 74]
    for x in range(10):
        letters.append(str(x))

    for l in letters:
        img = cv2.imread("ITSP_images/" + l + ".jpg")
        images.update({l: img})
    print "images loaded"

