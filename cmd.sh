#!/bin/bash

export SOUNDFILE=../green_day.mp3

# the python creates a folder named $user_id and calls this script with
# that user id as a param
cd $1

# resize, center and fill images
# for img in *.jpg
#   do convert $img -resize 720x480 -background black -gravity center -extent 720x480 $img
# done

# even easier than mencoder, just use dvd-slideshow!
dir2slideshow -notitle -a ${SOUNDFILE} -n slideshow -t 3.5 -c .3 .
dvd-slideshow -f slideshow.txt
exit

#deprecated code below
ls *.jpg | sort -n > files.txt

mencoder mf://@files.txt \
-mf w=720:h=480:fps=.4:type=jpeg \
-audiofile ${SOUNDFILE} \
-ovc lavc \
-oac lavc \
-lavcopts vcodec=mpeg4:vbitrate=5000 \
-ofps 30000/1001 \
-o $1.mpeg
