# Background-Removal

Repository of the Rodan wrapper for Background Removal

# Python dependencies:
  * scikit-image (0.19.2)
  * opencv-python (4.5.5.64)
  * numpy (1.21.6)
  * tensorflow (2.5.1)
  * keras (2.5.0rc0)

# Rodan Job

This background removal task belongs inside gpu-celery container.

# Local Usage
For local usage, Sauvola Algorithm method and SAE Binarization method are separate.

## Sauvola Algorithm
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

## SAE Binarization
The `binarize.py` script performs the binarization of an input image using a trained model. The parameters of this script are the following:


| Parameter    | Default | Description                      |
| ------------ | ------- | -------------------------------- |
| `-imgpath`   |         | Path to the image to process     |
| `-modelpath` |  (*)       | Path to the model to load        |
| `-w`         |  256    | Input window size                |
| `-s`         |  -1     | Step size. -1 to use window size |
| `-f`         |  64     | Number of filters                |
| `-k`         |  5      | Kernel size                      |
| `-drop`      |  0      | Dropout percentage               |
| `-stride`    |  2      | Convolution stride size          |
| `-every`     |  1      | Residual connections every x layers |
| `-th`        |  0.5    | Selectional threshold            |
| `-save`      |         | Output image filename            |

> (*) By default, the model trained with all datasets will be used.

The only mandatory parameter is `-imgpath`, the rest are optional. You also have to choose if you want to save (`-save`) the binarized image.

For example, to binarize the image `img01.png` you can run the following command:

```
$ python binarize.py -imgpath img01.png -save out.png
```
