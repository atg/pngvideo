# pngvideo -- Efficient png animations

**pngvideo** is a canvas-based animation player, based on PNGs. It provides the following over animated gifs:

* **Control over playback.** pngvideo loads all frames upfront so it will either play the animation properly, or it will wait. Additionally, you can start and stop playback.
* **Compression.** PNGs have much better compression than GIFs.
* **Alpha-channel** support.
* **Ease of assembly.** Creating an animated gif can be tricky. pngvideo just requires you to pass your frames to a python script which will do the rest.

pngvideo is also efficient, because it only sends the parts of the image that have changed.

## License

WTFPL. Look it up if you care (I don't).

## Technical Details

A pngvideo has two components:

1. A JSON file describing dimensions, the length of each frame, etc.
2. A single tall PNG image of all frames. The frames should be delta-encoded: areas that do not change from the previous image are transparent. 

### Full frames

If there exists a pixel in the new frame for which

    pixel's alpha ≠ 1
    and
    pixel's alpha != last full frame pixel's alpha

Then this frame should be marked as "isFull": true and should not be delta-encoded.

