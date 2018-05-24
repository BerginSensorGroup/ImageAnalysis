import cv2

def video_to_frames(video_filename):
    vidcap = cv2.VideoCapture(video_filename)
    success,image = vidcap.read()
    count = 0
    success = True
    while success:
      cv2.imwrite("frames/frame%d.jpg" % count, image)     # save frame as JPEG file
      success,image = vidcap.read()
      print('Read a new frame: ', success)
      count += 1

video_to_frames('CrowdStockFootage.mp4')
