#!/bin/bash

export SOUNDLENGTH=1
export MPG_1=yo.mpeg
export MPG_2=yoyo.mpeg
export VBITRATE=5000

mencoder mf://*.jpg -mf w=720:h=480:fps=1/${SOUNDLENGTH}:type=jpeg -ovc lavc -oac lavc -lavcopts vcodec=mpeg4 -ofps 30000/1001 -o ${MPG_1}

mencoder -ovc lavc -oac lavc -lavcopts \
  vcodec=mpeg2video:vrc_buf_size=1835:vrc_maxrate=9800:vbitrate=${VBITRATE}:keyint=18:acodec=ac3:abitrate=192:aspect=4/3:trell:mbd=2:dia=4:cmp=3:precmp=3:ildctcmp=3:subcmp=3:mbcmp=3:cbp:mv0:dc=10 \
  -of mpeg -mpegopts format=dvd -vf expand=720:480,harddup \
  -srate 48000 -af lavcresample=48000 -ofps 30000/1001 -o ${MPG_2} ${MPG_1}
