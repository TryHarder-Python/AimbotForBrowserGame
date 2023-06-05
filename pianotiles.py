from utils import get_coordinate_color, click
from keyboard import is_pressed


def click_piano_tile(x, y):
    if get_coordinate_color(x, y) == (0, 0, 0):
        click(x, y)


def main():
    while not is_pressed('esc'):
        click_piano_tile(670, 460)
        click_piano_tile(750, 460)
        click_piano_tile(850, 460)
        click_piano_tile(930, 460)


if __name__ == '__main__':
    main()
