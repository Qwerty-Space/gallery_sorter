import os
import os.path as osp
from imghdr import what
from shutil import copy2
from ffmpeg import probe
from pyexiv2 import Image
from datetime import datetime


## Config ##
# The Directory to sort from
sorting_dir = "sort"

# Whether to separate videos from images
separate_filetypes = True

# The directory to put images and videos (default "Photos" and "Videos")
images_dir = "Photos"
videos_dir = "Videos"

# The directory structure to sort into (supports strftime format codes)
# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
path_format = ["%Y", "%m %B"]

# Whether to copy the files, or move them
copy_files = True


def copyfile(f, new_path, ftype):
    count = 1
    new_name = f"{new_path}{ftype}"
    while osp.isfile(new_name):
        new_name = f"{new_path}_{count:03}{ftype}"
        count += 1
    copy2(f, new_name)

    return new_name


def main():
    sort = list()
    for root, directories, filenames in os.walk(sorting_dir):  # Create a list of all files in "path"
        for filename in filenames:
            f = os.path.join(root, filename)
            if osp.splitext(f)[1].casefold() not in [".mp4", ".jpg", ".jpeg"]:
                print(f"Not handling:  {f}")
                continue
            sort.append(f)
    print(f"Sorting {len(sort)} file(s)")
    
    failed = list()
    copied = dict()

    for f in sort: 
        # split the name by _ and extract required information
        fname = osp.basename(f)
        ftype = osp.splitext(fname)[1].casefold()

        print(f"Checking: {fname}")

        try: # try to get the creation date, else add it to the failed list
            ## get jpgs and mp4 files only
            if ftype in [".jpg", ".jpeg"]:
                fpath = images_dir
                name_prefix = "IMG"

                out = probe(f, show_frames=None)
                try: # try using ffprobe
                    creation_date = out['frames'][0]['tags']['DateTimeOriginal']
                except:
                    try: # try using pyexiv 2
                        img = Image(f)
                    except: # if reading fails, it might still have the information, because it's weird
                        pass
                    creation_date = img.read_exif()["Exif.Image.DateTime"]

            elif ftype == ".mp4":
                name_prefix = "VID"
                fpath = videos_dir
                out = probe(f)
                creation_date = out['format']['tags']['creation_time']
            else:
                print("Not handling")
                continue
        except:
            failed.append(f)
            continue


        ## get the date parts from the creation_date
        fyear = creation_date[:4]
        fmonth = creation_date[5:7]
        fday = creation_date[8:10]
        fhour = creation_date[11:13]
        fminute = creation_date[14:16]
        fsecond = creation_date[17:19]


        # create a datetime object from the file name info
        fdate = datetime(int(fyear), int(fmonth), int(fday), int(fhour), int(fminute), int(fsecond))
        new_name = f"{name_prefix}_{fyear}{fmonth}{fday}_{fhour}{fminute}{fsecond}"


        # this variable will be an empty string if separate_files is False, else it's equal to fpath
        basename = fpath if separate_filetypes else ""

        # use a splat operator to join every element of the path_format list
        pre_formatted_path = osp.join(*path_format)
        path = osp.join(fdate.strftime(pre_formatted_path), basename)

        os.makedirs(path, exist_ok=True) # make directories, unless they already exist

        new_path = osp.join(path, f"{new_name}") # the path of the file after being copied without the extension

        ## check if the file already exists
        check_name = f"{new_path}{ftype}"
        if osp.isfile(check_name) and check_name not in copied:
            print(f"File already exists:  {check_name}")
            continue

        new_file = copyfile(f, new_path, ftype)
        print(f"Copyied file:  {f} → {new_file}")

        copied[new_file] = f

        if not copy_files: # delete old files?
            os.remove(floc)

    for f in failed:
        print(f)

if __name__ == "__main__":
    if not osp.isdir(sorting_dir): # make sort dir if it doesn't exist
        print("Making sort dir")
        os.mkdir(sorting_dir)
    main()
    print("Done")
