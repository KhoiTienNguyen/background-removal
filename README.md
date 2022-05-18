# Background-Removal

Repository of the Rodan wrapper for Background Removal

# Python dependencies:
  * scikit-image (0.19.2)
  * opencv-python (4.5.5.64)
  * numpy (1.21.6)

# Rodan Job

This background removal task belongs inside py3-celery container.

# Local Usage
Use **BgRemovalLocalTask.py** to run this job locally.
Parameters:
  * **-psr** `Path to folder with the original images` (**Default:** *datasets/images*)
  * **-out** `Path to folder for output processed images` (**Default:** *datasets/output*)
  * **-pfx** `Postfix for output files <image_name><output_postfix>.png` (**Default:** *_nBg*)
  * **-w** `Window size for saulova algorithm. Must be an odd number integer.` (**Default:** *15*)
  * **-k** `Parameter for saulova algorithm. Must be positive` (**Default:** *0.2*)
  * **-c** `Amount to adjust contrast by. Can be negative.` (**Default:** *127.0*)
  * **-b** `Amount to adjust brightness by. Can be negative` (**Default:** *0.0*)
    
Example: `python3 BgRemovalLocalTask.py -psr datasets/images/MS73 -out datasets/output/MS73 -pfx _Bgr -w 101 -k 0.15 -c 150.0 -b 5.0`
