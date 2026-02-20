import sys
from PIL import Image
from PIL.ExifTags import TAGS

if __name__=="__main__":

    if len(sys.argv) == 1:
        pass

    if len(sys.argv) == 2:
        img = Image.open(sys.argv[1])
        exif_data = img._getexif()

        if exif_data:
            for id, value in exif_data.items():
                print(TAGS.get(id), value)