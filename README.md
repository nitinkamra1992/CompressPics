# CompressPics

This is an image compression tool built on top of `imagemagick convert` tool. It adds support for compressing all images in a directory (recursively), along with a minimum size constraint.

## Compatibility

The tool has been tested on Ubuntu and Python3.5+.

## Dependencies

The tool requires python3.5+. While the `imagemagick` package might be pre-installed on Ubuntu, install it if needed:
```
sudo apt update
sudo apt install imagemagick
```
Also, install dependencies:
```
pip install filetype
```

## Usage

The tool can be run as a Python script, e.g.:
```
python3 compress_pics.py -d <data_dir> -o <out_dir> -m 1000000 -rec -v -resize 50% -quality 50%
```
It supports all arguments for the `imagemagick convert` tool, and additionally the following arguments:
```
-d, --data: Input file/directory
-o, --out: Output file/directory. Default: Same as input file/directory.
-m, --minsize: Minimum size of a file to compress (in bytes). Type = int, Default = 0.
-rec, --recursive: Recursively process subdirectories if input is a directory.
-v, --verbose: Increase verbosity.
```

Note that the tool only processes image files. All other unsupported files are copied over directly. Any file smaller than `--minsize` is copied over directly. If `-rec` is not specified, all subdirectories are copied directly to the output directory.