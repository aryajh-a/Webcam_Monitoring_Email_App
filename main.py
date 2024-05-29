import cv2
import glob
import os

from mail import send_mail
from threading import Thread

# To start webcam... 0 to use main camers, 1 to use other attached camera
video = cv2.VideoCapture(0)

# first_frame, other frames will be compared against this frame
first_frame = None

# store object status
status_obj=0
status_list=[]
count = 1

# initializing clear thread
clear_thread = None

# function to delete all the images from the images folder after the email is sent
def clear_images_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
# while loop because -
# A video is basically a series of frames so to capture a video we need to capture frames continuously and not just once
while True:
    # set status_obj 0  for each frame
    status_obj=0
    # check returns true or false
    # frame captures the frames
    check, frame = video.read()
    
    
    # ALGORITHMS FOR COMPARISON
    # to conver frame pixels to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # # another tranformation to make calculation more efficient
    # # (21,21) means amount of blurness, 0 is std. deviation
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (5,5), 0)

    
    # set the first frame 
    if first_frame is None:
        first_frame = gray_frame_gau
        
    # get the difference of first_frame and current frames
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    
    # if a pixel has a value of 30, or more than 30, we reassign a value of 255 to it 
    # (black pixel has values close to 0, so we are converting the gray pixels to white)
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    # now we dilate the frame, iteration no. means number of processings done
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    
    
    # set contour to whitify object parts not whitified
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Recatngle the objects
    for contour in contours:
        if cv2.contourArea(contour)<5000:
            continue
        x,y,w,h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)
        
        # we send email when the object exits the window
        if rectangle.any():
            status_obj=1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count+1
            # glob package used to earch for files with a specific patter
            all_images = glob.glob("images/*.png")
            # the proper image will be somewhere in the middle... in sequence from entry to exit of an object
            index = int(len(all_images)/2)
            image_of_object = all_images[index]
        
    status_list.append(status_obj)
    status_list = status_list[-2:]
    
    # now when object just exits... list[0] is 1 but list[1] becomes 0, that is when we send the email
    if status_list[0]==1 and status_list[1]==0:
        print("Email sent")
        # send_mail(image_of_object)
        # doing threading to avoid video freezing because of two processes running.. this and the send_email()..
        # the send_email() method takes a lot of time leading to freezing of video
        email_thread = Thread(target=send_mail, args=(image_of_object, ))
        email_thread.daemon = True
        # function call to delete images
        # clear_images_folder()
        clear_thread = Thread(target=clear_images_folder)
        clear_thread.daemon = True
        
        # thread.start
        email_thread.start()
    
    
    
    # displays the video
    cv2.imshow("My video",frame)
    
    # key is a Key object basically which is storing the key being pressed in keyboard
    key = cv2.waitKey(1)
    # if the user presses 'q' key then terminate the app
    if key == ord('q'):
        break
    
# exit the video
video.release()

# clear thread is executed here so that all images are cleared out of images folder after video is quitted
clear_thread.start()
clear_thread.join()
