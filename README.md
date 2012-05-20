# pngvideo -- Efficient png animations

**pngvideo** is a canvas-based animation player, based on PNGs. It provides the following over animated gifs:

* **Control over playback.** pngvideo loads all frames upfront so it will either play the animation properly, or it will wait. Additionally, you can start and stop playback.
* **Compression.** PNGs have much better compression than GIFs.
* **Alpha-channel** support.
* **Ease of assembly.** Creating an animated gif can be tricky. pngvideo just requires you to pass your frames to a python script which will do the rest.

pngvideo is also efficient, because it only sends the parts of the image that have changed.

## License

WTFPL.

