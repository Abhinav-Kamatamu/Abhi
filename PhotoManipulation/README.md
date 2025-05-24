The following programs are to be used as follows.


---
> PhotoExtractor.py

* This program is used to extract smaller photos from a png containing various other photos. 


* To use the program, Firstly, keep all the images to be extracted inside a folder named `OriginalScans`. Within this each photo has to be named as `-01.png`, `-21.png`, `-123.png`, etc.
* Run the extractor code and create a new folder(the program will do this for you). Select a red bounding box around the image you want. The program will try to auto-detect an image for you (kinda doesn't work all the time).
* In that case, you can feel free to save red-selection.
* Keep a setting `ROI buffer` at 0.
* Sometimes, messing with the `Min Contour Area`. But preferably keep it as low as possible.
---

> Descriptions.py

This program is used to merge 2 images, an image.png file and a description.png file into a single png.

To use the program,
* Keep all the images in a directory named `images`. Each image within this directory is to be named as `1.png`, etc.
* Keep all the descriptions for an image in a directory `descriptions`. Here too, the descriptions are to be labelled as `1.png`, etc.
* When you run the program, just select the image, the description, and preview it before hitting save.
* The final images will be saved with the name of the file from the `images` directory within a directory named `Final`
---

> Combine.py

This program just renames and moves files from one folder to another.

* Files will be stored in a directory labelled `1`.
* Files will be moved from directories `2` or `3` or so on into `1` and will be renamed accordingly.
* Files in `2` and `3` must be named `1.png` and so on. It is okay for there to be numbers missing within these directories.
*  If `1` already contains files from `1.png` up to `n.png`, the new files will be saved starting from `n+1.png`
