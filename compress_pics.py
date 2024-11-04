import os
import errno
import argparse
import filetype
import time
import subprocess
import shutil


# ############################# Methods ###############################


def create_directory(directory):
    ''' Creates a directory if it does not already exist.
    '''
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def vprint(verbose, *args, **kwargs):
    ''' Prints only if verbose is True.
    '''
    if verbose:
        print(*args, **kwargs)


def args2str(arglist, delimiter=' '):
    ''' Converts a list of parsed arguments to string.
    '''
    return delimiter.join(arglist)


def compress_file(infile, outfile, minsize, cvt_args, verbose=False):
    ''' Parses and compresses known image format files above a specified
        minimum size.

    Args:
        infile: Input file path.
        outfile: Output file path (including name).
        minsize: Minimum file size to compress (in bytes). Files below
            minimum size are copied directly.
        cvt_args: Arguments for convert tool.
        verbose: Verbosity. Default = False.
    '''
    insize = os.path.getsize(infile)
    if insize <= minsize:
        vprint(verbose, f"Skipping {infile}: Size {insize} <= {minsize}")
        shutil.copy2(src=infile, dst=outfile)
    else:
        if filetype.is_image(infile):
            subprocess.call(f'convert "{infile}" {args2str(cvt_args)} "{outfile}"',
                            shell=True)
            vprint(verbose, f"Compressed {infile} into {outfile}")
        else:
            shutil.copy2(src=infile, dst=outfile)
            vprint(verbose, f"Directly copied non-image file: {infile}")


def compress_dir(indir, outdir, minsize, recursive, cvt_args, verbose=False):
    ''' Parses and compresses all image format files above a specified
        minimum size in a directory.

    Args:
        indir: Input directory.
        outdir: Output directory.
        minsize: Minimum file size to compress (in bytes). Files below
            minimum size are copied directly.
        recursive: If True, subdirectories are parsed recursively, else
            they are copied.
        cvt_args: Arguments for convert tool.
        verbose: Verbosity. Default = False.
    '''
    create_directory(outdir)
    for name in os.listdir(indir):
        inpath = os.path.join(indir, name)
        outpath = os.path.join(outdir, name)
        if os.path.isfile(inpath):
            compress_file(inpath, outpath, minsize, cvt_args, verbose)
        elif recursive:
            compress_dir(inpath, outpath, minsize, recursive,
                         cvt_args, verbose)
        else:
            shutil.copytree(src=inpath, dst=outpath, symlinks=True,
                            ignore_dangling_symlinks=True)
    vprint(verbose, f"Compressed directory {indir} into {outdir}")


def main(args, cvt_args):
    ''' Runs the main logic of the tool.

    Args:
        args: Known argparse arguments added by this script.
        cvt_args: Arguments for the convert tool.

    '''
    # Process output path
    if args.out is None:
        args.out = args.data

    # Compress files
    if os.path.isfile(args.data):
        compress_file(args.data, args.out, args.minsize, cvt_args,
                      args.verbose)
    else:
        compress_dir(args.data, args.out, args.minsize, args.recursive,
                     cvt_args, args.verbose)


# ############################# Entry Point ###############################


if __name__ == '__main__':
    # Initial time
    t_init = time.time()

    # Parse arguments
    parser = argparse.ArgumentParser(description='Compress pics using \
        the convert tool. Excess args are passed to convert.')
    parser.add_argument('-d', '--data',
                        help='Input file/directory.')
    parser.add_argument('-o', '--out',
                        help='Output file/directory. Default: Same as \
                            input file/directory.',
                        default=None)
    parser.add_argument('-m', '--minsize',
                        help='Minimum size of a file to compress (in bytes). \
                            Default = 0.',
                        type=int, default=0)
    parser.add_argument('-rec', '--recursive',
                        help='Recursively process subdirectories if input \
                            is a directory.',
                        action='store_true')
    parser.add_argument('-v', '--verbose',
                        help='Increase verbosity.',
                        action='store_true')
    args, cvt_args = parser.parse_known_args()

    # Call main method
    main(args, cvt_args)

    # Final time
    t_final = time.time()
    print(f"Progam finished in {t_final - t_init} secs.")
