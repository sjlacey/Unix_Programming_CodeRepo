"""
Sean Lacey, 18902826, sean.lacey@ucdconnect.ie

This script takes two arguments, a source file/directory and a destination file/
directory. The script duplicates the source directory to the destination
directory, however it converts any .png files to .jpg, and does not preserve any
other files.
"""

#! /bin/bash

if [ ! $# -eq 2 ]; then
    echo -e "\nError: Script needs 2 arguments: a source directory and a destination directory\n"
    exit
fi

function recursiveCopy {
    for file in `ls $1`; do
        if [ -d $1/$file ] && [ ! -d $2/$file ]; then
            mkdir $2/$file
            recursiveCopy $1/$file $2/$file
        elif [[ $1/$file == *.png ]]; then
            convert $1/$file $2/$file
            mogrify -format jpg -background white -flatten $2/$file
            rm -f $2/$file
        fi
    done
}

if [ ! -d $1 ]; then
    echo -e "\nError: $1 does not exist\n"
    exit
elif [ ! -d $2 ]; then
    echo -e "\nSuccess: $2 has been created"
    mkdir $2
elif [ -d $2 ] && [ ! -w $2 ]; then
    echo -e "\nError: You do not have permission to write to $2\n"
    exit
fi

recursiveCopy $1 $2
