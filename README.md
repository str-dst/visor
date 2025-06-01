# The digital face of 0x4C6F75

Visor based on a cheap 3M 6800 compatible gas mask

## What?

Two "see-through" 16x16 ws2812b LED panels mounted inside a full face gas mask.  
The mask was tinted using Rit-Dyemore Graphite-Black plastic dye to hide the electronics inside.  

The panels are controlled by a relatively simple Python script running on a RPi Zero 2W.  
A wired six-button remote strapped to my left hand is used change the displayed faces.  
Two of the buttons on the remote act as "modifiers", making a total of 16 combinations possible.  

## How?

The image files are first loaded with PIL and the pixel values are stored in a list.  
A preselect color is then added to the "active" white pixels of the loaded image.  
The list of pixel values is then simply displayed on the LED matrix.  

The remote controller is based on an Elite-C controller and hardwired to the Pi.  
For each keypress or keypress-combination a distinctive keycode is sent over a serial connection.  
On key release the code '0x00' is sent, though this has currently no real use.

The faces are stored as simple 16x32 1-bit black/white bitmap files.  
Every face is mapped to one of the remotes keycodes.  

Keycode 0x0C is an exception and cycles through different colors for the face.  
Some faces have a preset color that changes automatically for an added effect.  

## Currently implemented codes

 |Keycode|Display content|Color|
 |-|-|-|
 |0x01|Default, happy eyes|default|
 |0x02|Wide round eyes|default|
 |0x03|Sleepy drowsy looking|default|
 |0x04|Wink, left eye closed|default|
 |0x05|Flat eyed, annoyed|default|
 |0x06|Small eyes, focused|default|
 |0x07|Cheeky, pointy upwards|default|
 |0x08|BOOPED!, eyes inward|default|
 |0x09|Dead, X eyes|red|
 |0x0A|Angry, frowning|red|
 |0x0B|Targetmode, evil|red|
 |0x0D|Text: BEEP|green|
 |0x0E|Text: awoo|orange|
 |0x0F|Text: NO|red|
 |0x10|Text: FACE|blue|


## Possible additions / changes for the future

 - Add more key combos to the remote to be able to add more faces
 - Make it possible to create "compound faces" individually controlling the left or right eye
 - Adding a "boop sensor" to the nose of the mask
 - A microphone on the inside of the mask and a speaker on the outside for real-time voice changing
 - Eye detection inside the mask to automatically change the face / display a "blink" animation
