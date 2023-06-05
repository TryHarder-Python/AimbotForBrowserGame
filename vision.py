from window_capture import WindowCapture
import cv2 as cv


class Vision:
    def __init__(self, window_name, target_image, debug=False):
        self.wincap = WindowCapture(window_name)
        self.target_image = cv.imread(target_image, cv.IMREAD_GRAYSCALE)
        self.target_image_w = self.target_image.shape[1]
        self.target_image_h = self.target_image.shape[0]
        self.debug = debug

    def find_object(self, find_method=cv.TM_CCOEFF_NORMED, threshold=0.8):
        screenshot = self.wincap.get_image_from_window()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2GRAY)
        h, w = screenshot.shape
        result = cv.matchTemplate(screenshot, self.target_image, find_method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val > threshold:
            if self.debug:
                top_left = max_loc
                bottom_right = (top_left[0] + self.target_image_w, top_left[1] + self.target_image_h)
                cv.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)
                cv.imshow('Computer Vision', screenshot)
            return self.calculate_center_coordinates(max_loc, w, h)
        return None

    def calculate_center_coordinates(self, max_loc, w, h):
        window_x = self.wincap.window_x
        window_y = self.wincap.window_y
        window_width = self.wincap.window_width
        window_height = self.wincap.window_height

        # Calculate the scaling factors for x and y coordinates
        x_scale = window_width / w
        y_scale = window_height / h

        # Convert the screenshot coordinates to window coordinates
        top_window_x_coord = int(window_x + (max_loc[0] * x_scale))
        top_window_y_coord = int(window_y + (max_loc[1] * y_scale))
        center_window_x_coord = top_window_x_coord + self.target_image_w * x_scale // 2
        center_window_y_coord = top_window_y_coord + self.target_image_w * x_scale // 2
        return center_window_x_coord, center_window_y_coord
