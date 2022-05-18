import argparse
import os.path as osp
import glob

from background_removal_engine import remove_background
from LoaderWriter import load_image, write_image

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-psr", type=str, default="./datasets/images", 
                        help="Load <image_name>.png in this folder.")
    parser.add_argument("-out", type=str, default="./datasets/output",
                        help="Write <image_name><output_postfix>.png to this folder.")
    parser.add_argument("-pfx", type=str, default="_nBg",
                        help="Write to <image_name><output_postfix>.png")
    parser.add_argument("-w", type=int, default=15,
                        help="Parameter for saulova algorithm. Must be an odd number.")
    parser.add_argument("-k", type=float, default=0.2,
                        help="Paramter for saulova algorithm")
    parser.add_argument("-c", type=float, default=127.0,
                        help="Amount to adjust contrast by. Can be negative.")
    parser.add_argument("-b", type=float, default=0.0,
                        help="Amount to adjust brightness by. Can be negative")
    args = parser.parse_args()
    return args

def loader(args):
    """ A generator to load *.png locating inside <args.psr>.

    Parameters:
        args (argparse.Namespace): A namespace with <dataset_path> argument.
    Returns:
        str: Load image name.
        np.ndarray: Load image with shape (W, H, 3) with dtype=uint8. The channel order is RGB. 
    """
    image_path_list = [p for p in sorted(glob.glob(osp.join(args.psr, "*.png"))) if args.pfx not in p]
    for image_path in image_path_list:
        # Load image
        image_name = image_path.split("/")[-1]
        image_rgb = load_image(image_path)
        yield image_name, image_rgb

def main():
    args = getArgs()

    for image_name, image_rgb in loader(args):
        image_processed = remove_background(image_rgb, args.w, args.k, args.c, args.b)

        filename, filetype = image_name.split(".")
        new_image_name = "{}{}.{}".format(filename, args.pfx, filetype)
        output_path = osp.join(args.out, new_image_name)
        print ("Write to {}".format(output_path))

        write_image(output_path, image_processed)

if __name__ == "__main__":
    main()