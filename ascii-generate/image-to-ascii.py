import cv2
import numpy as np
import json
import os

SYMBOLS    = ['  ','#'] #[' ','.','*','*',' ']
THRESHOLDS = [0,250] #[0, 50, 100, 150, 250]

def ConvertToAscii(img):
    symbols_len = len(SYMBOLS)

    frame = ''
    #Each line in the img
    for row in img:
        #Each character in the line
        for column in row:
            ascii_char = SYMBOLS[column % symbols_len]
            frame += ascii_char
        frame += ';'
    return [frame]

def GenerateAscii(img, res=tuple(), density=0):

    height, width = img.shape
    new_width = width // res[0]
    new_heigth = height // res[1]
    
    #Resizing image to fit in 1 GD Frame
    # blured_img = cv2.blur(img,(5,5))
    resized_img = cv2.resize(img, (new_width, new_heigth))
    
    threshold_arr = np.zeros(resized_img.shape)

    for i, threshold in enumerate(THRESHOLDS):
        threshold_arr[resized_img > threshold] = i+density
    
    return threshold_arr.astype(int)

if __name__ == "__main__":
    ANIMATION_PATH = 'animation/'
    PATH = 'badapple.mp4'
    json_output = 'output.json'
    max_frames = 1000 #This is the max amount of frames generated by the script.

    #Make the dir where the frames will go
    try:
        os.mkdir('animation')
    except:
        print('Dir already exists')

    capture = cv2.VideoCapture(PATH)

    #Split the video into frames
    frame_skip = 3
    frame_count = 0

    #Read the images
    while True:
        success, frame = capture.read()

        #If max frame reached
        if not success or frame_count > max_frames:
            break

        #If frame is divisible by frame skip
        if (frame_count % frame_skip) == 0:
            #Generate a new frame
            cv2.imwrite(f'animation/{frame_count//frame_skip}.jpg',frame)
        
        frame_count += 1

    capture.release()
    
    frame_count //= frame_skip
    animation = {}
    f_animation = open(json_output, 'w')

    max_frames = frame_count if max_frames >= frame_count else max_frames
    #For each generated frame convert to ascii into a file
    for i in range(0, max_frames):
        frame_path = ANIMATION_PATH + f'{i}.jpg'

        img = cv2.imread(frame_path, 0)
        ascii_art = GenerateAscii(img, (3,6))
        
        frame = ConvertToAscii(ascii_art)
        animation[i] = frame
        os.remove(frame_path)
    json.dump(animation, f_animation)