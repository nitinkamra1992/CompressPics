# CompressPics

This is an image compression tool built on top of imagemagick convert tool. It adds support for compressing all images in a directory (recursively), along with a minimum size constraint.

## Compatibility
The tool has been written for Ubuntu and tested on Python v3.5 and above but may be compatible with other versions of python too.

## Dependencies
The tool requires python3 (generally present by default). Also install imagemagick:

```
sudo apt update
sudo apt install imagemagick
```

## Usage

The tool can be run as a Python script, e.g.:
```
python3 compress_pics.py <data_dir> -o <out_dir> -m 1000000 -rec -v -resize 50% -quality 50%
```
It supports all arguments for the imagemagick convert tool, and additionally the following arguments:
```
-d, --data: Input file/directory
-o, --out: Output file/directory. Default: Same as input file/directory.
-m, --minsize: Minimum size of a file to compress (in bytes). Type = int, Default = 0.
-rec, --recursive: Recursively process subdirectories if input is a directory.
-v, --verbose: Increase verbosity.
```

Note that the tool only processes image files. All other unsupported files are copied over directly. Any file smaller than `--minsize` is copied over directly. If `-rec` is not specified, all subdirectories are copied directly to the output directory.