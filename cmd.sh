#!/bin/bash

export VBITRATE=5000
export SOUNDFILE=../green_day.mp3

cd $1

# resize the images
for img in *.jpg
  do convert $img -resize 720x480 -background black -gravity center -extent 720x480 $img
done

ls *.jpg | sort -n > files.txt

mencoder mf://@files.txt \
-mf w=720:h=480:fps=.4:type=jpeg \
-audiofile ${SOUNDFILE} \
-ovc lavc \
-oac lavc \
-lavcopts vcodec=mpeg4 \
-ofps 30000/1001 \
-o $1.mpeg

# mencoder -ovc lavc -oac lavc -lavcopts \
#   vcodec=mpeg2video:vrc_buf_size=1835:vrc_maxrate=9800:vbitrate=${VBITRATE}:keyint=18:acodec=ac3:abitrate=192:aspect=4/3:trell:mbd=2:dia=4:cmp=3:precmp=3:ildctcmp=3:subcmp=3:mbcmp=3:cbp:mv0:dc=10 \
#   -of mpeg -mpegopts format=dvd -vf expand=720:480,harddup \
#   -srate 48000 -af lavcresample=48000 -ofps 30000/1001 -o ${MPG_2} ${MPG_1}
