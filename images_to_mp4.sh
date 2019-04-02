../../../ffmpeg -r 20 -f image2 -s 1000x1000 -i 20190402_090155_parc_pie_626_%04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p test.mp4
