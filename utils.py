from time import sleep

from Quartz import CoreGraphics as CG
import numpy as np
import Quartz as QZ
import mss


def click(x, y):
    event = CG.CGEventCreateMouseEvent(
        None,
        CG.kCGEventMouseMoved,
        (x, y),
        CG.kCGEventLeftMouseDown,
    )
    CG.CGEventPost(CG.kCGHIDEventTap, event)
    CG.CGEventSetType(event, CG.kCGEventLeftMouseDown)
    CG.CGEventPost(CG.kCGHIDEventTap, event)
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
    core_graphics_image = QZ.CGWindowListCreateImage(
        QZ.CGRectInfinite,
        QZ.kCGWindowListOptionOnScreenOnly,
        QZ.kCGNullWindowID,
        QZ.kCGWindowImageDefault
    )

    bytes_per_row = QZ.CGImageGetBytesPerRow(core_graphics_image)
    width = QZ.CGImageGetWidth(core_graphics_image)
    height = QZ.CGImageGetHeight(core_graphics_image)

    core_graphics_data_provider = QZ.CGImageGetDataProvider(core_graphics_image)
    core_graphics_data = QZ.CGDataProviderCopyData(core_graphics_data_provider)

    np_raw_data = np.frombuffer(core_graphics_data, dtype=np.uint8)
    numpy_data = np.lib.stride_tricks.as_strided(np_raw_data,
                                                 shape=(height, width, 4),
                                                 strides=(bytes_per_row, 4, 1),
                                                 writeable=False)
    final_output = np.ascontiguousarray(numpy_data, dtype=np.uint8)
    return final_output
