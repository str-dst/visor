#!/usr/bin/python3

from PIL import Image
import numpy as np
from rpi_ws281x import PixelStrip, Color
import serial
import time

# LED strip configuration:
LED_COUNT = 512      # Number of LED pixels.
LED_PIN = 18         # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000 # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10         # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 32  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0      # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Load and process the bitmap, our matrix is mounted upside down so we rotate the image
def load_and_process_bitmap(image_path):
    img = Image.open(image_path).convert("1")
    img_flip = img.rotate(180)
    bitmap = np.array(img_flip)
    return process_bitmap(bitmap)

# Process the bitmap
def process_bitmap(bitmap):
    height, width = bitmap.shape
    processed_pixels = []

    for col in range(width):
        if col % 2 == 0:
            # Even columns: read from top to bottom
            column_pixels = bitmap[:, col]
        else:
            # Odd columns: read from bottom to top
            column_pixels = bitmap[::-1, col]

        processed_pixels.extend(column_pixels)

    return processed_pixels

# Add color to active white pixels
def add_color(processed_pixels, color):
    colored_pixels = []
    for pixel in processed_pixels:
        if pixel == 1:  # White pixel
            colored_pixels.append(color)
        else:
            colored_pixels.append((0, 0, 0))  # Black pixel
    return colored_pixels

# Display on WS2812B LED matrix
def display_on_led_matrix(pixel_values):
    # Create PixelStrip object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

    # Initialize the LED panel
    strip.begin()

    # Iterate over each pixel value and set the LED color
    for i, pixel in enumerate(pixel_values):
        if i >= LED_COUNT:
            break  # Ensure we do not exceed the number of LEDs
        # Assuming pixel is in the format (R, G, B)
        strip.setPixelColor(i, Color(pixel[0], pixel[1], pixel[2]))

    # Show the LED colors
    strip.show()

    # Clean up
    time.sleep(0.3)
    strip._cleanup()

# Main function
def main():
    # Mapping of serial data codes to image file paths
    image_mapping = {
        b'\x01': 'faces/01_happy.bmp',
        b'\x02': 'faces/02_wide.bmp',
        b'\x03': 'faces/03_sleepy.bmp',
        b'\x04': 'faces/04_wink.bmp',
        b'\x05': 'faces/05_boop.bmp',
        b'\x06': 'faces/06_dizzy.bmp',
        b'\x07': 'faces/07_flat.bmp',
        b'\x08': 'faces/08_small.bmp',
        b'\x09': 'faces/09_hearts.bmp',
        b'\x0A': 'faces/10_dead.bmp',
        b'\x0B': 'faces/11_angry.bmp',
        b'\x0D': 'faces/12_beep.bmp',
        b'\x0E': 'faces/13_awoo.bmp',
        b'\x0F': 'faces/14_no.bmp',
        b'\x10': 'faces/15_face.bmp',
    }

    # Preset color indexes for some of the faces
    color_mapping = {
        b'\x09': 5,
        b'\x0A': 6,
        b'\x0B': 6,
        b'\x0D': 0,
        b'\x0E': 7,
        b'\x0F': 6,
        b'\x10': 2,
    }

    # Color set that we can loop through
    color_values = [
        (0, 255, 0),    # Green
        (0, 255, 128),  # Turquoise
        (0, 64, 255),   # Light blue
        (0, 0, 255),    # Blue
        (48, 0, 255),   # Purple
        (192, 0, 255),  # Pink
        (255, 0, 0),    # Red
        (255, 48, 0),   # Orange
        (255, 192, 0),  # Yellow
        (64, 255, 0),   # Lime
        (255, 255, 255) # White
    ]

    # Define the color index for active white pixels (e.g., red)
    current_color_index = 0
    previous_color_index = 0
    color_was_preset = False

    # Initialize serial connection
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

    current_image_path = image_mapping[b'\x01']  # Default image

    # Initial display load
    processed_pixels = load_and_process_bitmap(current_image_path)
    colored_pixels = add_color(processed_pixels, color_values[current_color_index])
    display_on_led_matrix(colored_pixels)

    try:
        while True:
            # Read data from serial
            data = ser.read(1)

            if data:
                # Ignore the key-release code for now
                if data == b'\x00':
                    continue

                # Cycle through the preset colors on 0x0C
                if data == b'\x0C':
                    if current_color_index == 10:
                        current_color_index = 0
                    else:
                        current_color_index += 1

                # All other keycodes check against image and color mapping
                else:
                    if data in color_mapping:
                        if color_was_preset == False:
                            previous_color_index = current_color_index
                        color_was_preset = True
                        current_color_index = color_mapping[data]
                    else:
                        color_was_preset = False
                        current_color_index = previous_color_index

                    if data in image_mapping:
                        current_image_path = image_mapping[data]

                # Print some debug info...
                print("Data recv: "+str(data)+", Image: "+str(current_image_path)+", Color: "+str(current_color_index))

                # Load and process the selected image
                processed_pixels = load_and_process_bitmap(current_image_path)
                colored_pixels = add_color(processed_pixels, color_values[current_color_index])
                display_on_led_matrix(colored_pixels)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()

# Run the main function
if __name__ == "__main__":
    main()