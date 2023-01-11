# fotofiler
**Photo filing utility written in Python**

Usage:
python3 cli.py

Developed and tested on Python 3.9+

I wrote this because I really missed the good old photo import wizard, that arranges imported photos in a subdirectory structure like {year}/{year.4d}-{month.2d}. 

This kind of arrangement is very nice, if you use old-fashioned physical media like CDs, DVDs or small USB drives, which cannot contain the photo collection in one unit.
Also, if you want make a USB stick to browse photos on your smart TV, in practise it may become clumsy to find last summer's photos in a flat collection of 9000 photos.
Instead, keeping yearly and monthly order, which I started already in 2004, I still consider relevant. 

There are of course more sophisticated photo management apps, this is just a script that copies photos to folders by date.
By which date? Excellent question!!! The answer is not that simple. I decided (you can read it in the code)

1. EXIF DateTimeOriginal
2. EXIF DateTime (any other DateTime, if the above wasn't available
3. Filesystem date that is given by os.path.getctime or os.path.getmtime, whichever is older
4. A date implied by file name, as detected by dateutil.parser (file system date rarely fails, so this is mererly theoretical)

The app in wizard mode throws you a few windows, made with _easygui_; the progress is indicated in a _tkinter_ window.

There will be command line options, to use this without GUI wizard.

I'm thinking of new features:
- Outputting the collected metadata to a table file (e.g. .csv), that can be further processed. 
- for being able to run without large memory (everyone doesn't have a i7 with 16GB)
- for being able to analyze in detail what's being done
- for being able to modify the copying task
- for finding events by timewise clustering 
- find places by clustering coordinates
- limiting output to certain dates and number of items

In the future, I hope to extend this to support some other directory structures and schemes, and a possibility to intelligently rename files.

I hope this will provide a less irritating alternative to these wizards that come in system software.

The first version is made and tested on Windows 10, and will be developed and tested to work with Ubuntu-class linux as well.

If you need a complete, stable tool that solves most of the EXIF and photo metadata related desires, please visit Phil Harvey's *exiftool* project at https://exiftool.org . I humbly give respect to that work.
