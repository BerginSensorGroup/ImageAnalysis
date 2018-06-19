from picamera import PiCamera
import datetime

def takePicture(camera, save_folder, stamp_folder, number_file, name):
    '''
    Parameters
    camera: the camera instance with which to take pictures
    number_file: a file that holds the current picture number so no two pictures
        will ever have the same name. A file is used instead of a variable so
        the number is maintained in the case of power loss
    
    Returns the picture number that was saved
    '''
    pic_num = 0
    try:
        file = open(number_file, 'r')
        pic_num = int(file.read())
        file.close()
    except IOError:
        #if we get IOError here, that means the file did not yet exist
        #in this case just start pic_num at zero
        pass
    
    now = datetime.datetime.now()    
        
    camera.capture(save_folder + ('{}_{}.jpg'.format(name,pic_num)))
    
    time_stamp_path = stamp_folder + ('{}.txt'.format(pic_num))
    time_stamp_file = open(time_stamp_path, 'w+')
    #Either store the current time for the picture or declare that we do not know the current time
    #Note that if we don't have the time, the default time is the beginning of Unix time (1970)
    if now.year < 2018:
        time_stamp_file.write('NO TIME (time unknown when picture was taken)')
    else:
        time_stamp_file.write(now.strftime("%I_%M%p on %B %d, %Y"))
    time_stamp_file.close()
    
    #finish the function by updating the picture number
    pic_num += 1
    
    file = open(number_file, 'w+')
    file.write(str(pic_num))
    file.close()
