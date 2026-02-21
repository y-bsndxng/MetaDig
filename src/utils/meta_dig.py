import os
import piexif
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def get_metadig(file_path: Path):
    ret = "{}\t{}\n".format("File Path", file_path)
    img = Image.open(file_path)
    exif_data = img._getexif()

    if exif_data:
        strings = ["{}\t{}".format(TAGS.get(id), value) for id, value in exif_data.items()]
        ret += "\n".join(strings)

    return ret

if __name__=="__main__":
    # 1. テスト画像を作成（グラデーション）
    img = Image.new("RGB", (800, 600), color=(100, 149, 237))

    # 2. EXIF データを構築
    exif_dict = {
        "0th": {
            piexif.ImageIFD.Make: b"TestCamera",
            piexif.ImageIFD.Model: b"TestModel X1",
            piexif.ImageIFD.Software: b"Python piexif",
            piexif.ImageIFD.DateTime: datetime.now().strftime("%Y:%m:%d %H:%M:%S").encode(),
            piexif.ImageIFD.XResolution: (72, 1),
            piexif.ImageIFD.YResolution: (72, 1),
        },
        "Exif": {
            piexif.ExifIFD.ExposureTime: (1, 100),        # 1/100秒
            piexif.ExifIFD.FNumber: (28, 10),             # F2.8
            piexif.ExifIFD.ISOSpeedRatings: 400,
            piexif.ExifIFD.DateTimeOriginal: b"2024:06:01 12:00:00",
            piexif.ExifIFD.FocalLength: (50, 1),          # 50mm
            piexif.ExifIFD.Flash: 0,
        },
        "GPS": {
            piexif.GPSIFD.GPSLatitudeRef: b"N",
            piexif.GPSIFD.GPSLatitude: ((35, 1), (41, 1), (22, 1)),   # 東京付近
            piexif.GPSIFD.GPSLongitudeRef: b"E",
            piexif.GPSIFD.GPSLongitude: ((139, 1), (41, 1), (30, 1)),
            piexif.GPSIFD.GPSAltitude: (10, 1),
        },
        "1st": {},
        "thumbnail": None,
    }

    # 3. EXIF をバイト列に変換して保存
    exif_bytes = piexif.dump(exif_dict)
    img.save("test.jpeg", "JPEG", exif=exif_bytes, quality=95)
    ret = get_metadig(Path("test.jpeg"))
    print(ret)