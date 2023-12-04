#!/bin/bash

# import imghdr

################### Help message ###################

help ()
{
    echo "Compress Pics tool"
    echo "Usage: compress_pics [-i | --in] INPATH
               [-o | --out] OUTPATH
               [-m | --minsize] MINSIZE
               [-r | --recursive]
               [-v | --verbose]
               [-resize | --resize] SIZE_PERCENT
               [-quality | --quality] QUALITY_PERCENT
               [-h | --help]"
}

################### Start ###################

# Start time
t_start=$(date +%s)

################### Parse cmd-line args ###################

out=""
minsize=0
recursive=0
verbose=0
resize='100%'
quality='100%'

while [[ "$1" != "" ]]; do
    case "$1" in
        -i | --in)
            in="$2"
            shift 2
            ;;
        -o | --out)
            out="$2"
            shift 2
            ;;
        -m | --minsize)
            minsize="$2"
            shift 2
            ;;
        -r | --recursive)
            recursive=1
            shift 1
            ;;
        -v | --verbose)
            verbose=1
            shift 1
            ;;
        -resize | --resize)
            resize="$2"
            shift 2
            ;;
        -quality | --quality)
            quality="$2"
            shift 2
            ;;
        -h | --help)
            help
            exit 0
            ;;
        *)
            echo "Unexpected option: $1"
            echo ""
            help
            exit 1
            ;;
    esac
done


################### Methods ###################

log ()
{
    if [[ $verbose -eq 1 ]]; then
        echo "$@"
    fi
}

compress_file ()
{
    local size=$(stat "$1" | cut -d " " -f 8)
    if [[ $size -le $minsize ]]; then
        log "Skipping $1: Size $size less than minsize $minsize"
        cp "$1" "$2"
    else
        if [[ "$1" == *.jpg || "$1" == *.png || "$1" == *.gif || "$1" == *.tiff ]]; then
            convert "$1" -resize $resize -quality $quality "$2"
            log "Compressed $1 into $2"
        else
            cp "$1" "$2"
            log "Directly copied $1: Not an image file"
        fi
    fi
}

compress_dir ()
{
    # Create the output directory
    mkdir -p "$2"

    for fpath in $(ls "$1"); do
        local inpath="$1/$fpath"
        local outpath="$2/$fpath"
        if [[ -f "$inpath" ]]; then
            compress_file "$inpath" "$outpath"
        elif [[ $recursive -eq 1 ]]; then
            compress_dir "$inpath" "$outpath"
        else
            cp -r "$inpath" "$outpath"
        fi
    done
    log "Compressed directory $1 into $2"
}

################### Program ###################

# If output path not specified, override input path
if [[ $out = "" ]]; then
    out=$in
fi

# Save and change IFS to ignore spaces in filenames while looping later
OLDIFS=$IFS
IFS=$'\n'

# Compress files
if [[ -f "$in" ]]; then
    compress_file "$in" "$out"
elif [[ -d "$in" ]]; then
    compress_dir "$in" "$out"
else
    echo "Input path: $in is neither a file nor a directory"
    exit 1
fi

# Restore IFS
IFS=$OLDIFS

################### End ###################

# End time
t_end=$(date +%s)

log "Program finished in $(($t_end - $t_start)) secs."
exit 0
