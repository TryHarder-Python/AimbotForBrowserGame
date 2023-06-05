from time import sleep

from keyboard import is_pressed

from vision import Vision
from utils import click


def main(window_name='AimBooster', target_image='target1.png'):
    vision_object = Vision(window_name, target_image)
    sleep(2)
    while not is_pressed('esc'):
        result = vision_object.find_object(threshold=0.9)
        if result is None:
            continue
        click(*result)


# loop_time = time()
# while True:
#     # get an updated image of the game
#     screenshot = wincap.get_image_from_window()
#     screenshot = cv.cvtColor(screenshot, cv.COLOR_RGBA2GRAY)
#
#     # display the processed image
#     cv.imshow('Computer Vision', screenshot)
#     # result = cv.matchTemplate(screenshot, target_image, cv.TM_CCOEFF_NORMED)
#     # debug the loop rate
#     print('FPS {}'.format(1 / (time() - loop_time)))
#     loop_time = time()

# hold 'q' with the output window focused to exit.
# waits 1 ms every loop to process key presses


if __name__ == '__main__':
    main()
