import sys
import os

def rename_file(src):
    for filename in os.listdir(src):
        origin = filename
        filename = filename.replace('-', '_')
        filename = filename.replace('+', '_')
        os.rename(os.path.join(src, origin), os.path.join(src, filename))

if __name__ == "__main__":
    src = "D:\\ai2020_prprc\\rgb_vid\\swoop_02"
    rename_file(src)

