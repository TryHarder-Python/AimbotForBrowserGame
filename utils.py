from time import sleep
import numpy as np
import Quartz as Qz
import mss


def click(x, y):
    event = Qz.CGEventCreateMouseEvent(
        None,
        Qz.kCGEventMouseMoved,
        (x, y),
        Qz.kCGEventLeftMouseDown,
    )
    Qz.CGEventPost(Qz.kCGHIDEventTap, event)
    Qz.CGEventSetType(event, Qz.kCGEventLeftMouseDown)
    Qz.CGEventPost(Qz.kCGHIDEventTap, event)
    sleep(0.05)


def get_coordinate_color(x, y):
    with mss.mss() as sct:
        # Define the region around the mouse cursor
        monitor = {"top": y, "left": x, "width": 1, "height": 1}

        # Capture the pixel color
        sct_img = sct.grab(monitor)
        pixel_color = sct_img.pixel(0, 0)

    return pixel_color


def get_image_from_screen():
    core_graphics_image = Qz.CGWindowListCreateImage(
        Qz.CGRectInfinite,
        Qz.kCGWindowListOptionOnScreenOnly,
        Qz.kCGNullWindowID,
        Qz.kCGWindowImageDefault
    )

    bytes_per_row = Qz.CGImageGetBytesPerRow(core_graphics_image)
    width = Qz.CGImageGetWidth(core_graphics_image)
    height = Qz.CGImageGetHeight(core_graphics_image)

    core_graphics_data_provider = Qz.CGImageGetDataProvider(core_graphics_image)
    core_graphics_data = Qz.CGDataProviderCopyData(core_graphics_data_provider)

    np_raw_data = np.frombuffer(core_graphics_data, dtype=np.uint8)
    numpy_data = np.lib.stride_tricks.as_strided(np_raw_data,
                                                 shape=(height, width, 4),
                                                 strides=(bytes_per_row, 4, 1),
                                                 writeable=False)
    final_output = np.ascontiguousarray(numpy_data, dtype=np.uint8)
    return final_output
