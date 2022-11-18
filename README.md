# fotoco.py
Photo copy wizard written in Python

Usage:
python3 photoco.py

Developed and tested on Python 3.9

I wrote this because I really missed good old photo import wizard, that arranges imported photos in a subdirectory structure like {year}/{year.4d}-{month.2d}. 

This kind of arrangement is very nice, if you use old-fashioned physical media like CDs, DVDs or small USB drives, which cannot contain the photo collection in one unit.
Also, if you want make a USB stick to browse photos on your smart TV, in practise it may become clumsy to find last summer's photos in a flat collection of 9000 photos.
Instead, keeping yearly and monthly order, which I started already in 2004, I still consider nice. 

There are of course more sophisticated photo management apps, this is just a script that copies photos to folders by date.
By which date? Excellent question!!! The answer is not that simple. I decided (you can read it in the code)

1. EXIF DateTimeOriginal
2. EXIF DateTime (any other DateTime, if the above wasn't available
3. A date implied by file name, as detected by dateutil.parser
4. Filesystem date that is given by os.path.getctime, that is sort of creation time.

The Script throws you a few windows, made with _easygui_

In the future, I hope to extend this to support some other directory structures and schemes, and a possibility to intelligently rename files.

I hope this will provide a less irritating alternative to these wizards that come in system software.

The first version is made and tested on Windows 10, and shall be developed and tested to works with Ubuntu-class linux as well.
