import arcade
from managers import MyWindow
from constants.screen import WIDTH, HEIGHT, TITLE

def main():
    """Main function"""
    window = MyWindow(WIDTH, HEIGHT, TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
