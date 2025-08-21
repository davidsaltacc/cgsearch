:: this script can manually be run to generate a good ico file with multiple resolutions if imagemagick is installed

@echo off

where magick
if %errorlevel% neq 0 goto exit

magick big_icon.png -define icon:auto-resize=16,18,24,32,48,64,128,256,512 -filter Lanczos -quality 100 icon.ico

:exit