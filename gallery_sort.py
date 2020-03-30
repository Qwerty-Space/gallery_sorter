import re
import os
import os.path as osp
from datetime import datetime
from shutil import copy2


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

# Overwrite files if they exist
overwrite = False


def main():
    sort = os.listdir(sorting_dir)
    for f in sort: 
        floc = osp.join(sorting_dir, f) # set the original file location

        # if the file doesn't match the format, ignore it
        m = re.match("(IMG|VID)_\d{8}(_\d{6})?(_\d{1,3})?\.(jpe?g|mp(eg)?4)", f)
        if not m:
            continue

        # split the name by _ and extract required information
        namelist = f.split("_")
        ftype = namelist[0]
        if ftype == "IMG":
            fpath = images_dir
        elif ftype == "VID":
            fpath = videos_dir

        fyear = namelist[1][:4]
        fmonth = namelist[1][4:6]
        fday = namelist[1][6:8]

        # create a datetime object from the file name info
        fdate = datetime(int(fyear), int(fmonth), int(fday))

        # this variable will be an empty string if separate_files is False, else it's equal to fpath
        basename = fpath if separate_filetypes else ""

        # use a splat operator to join every element of the path_format list
        pre_formatted_path = osp.join(*path_format)
        path = osp.join(fdate.strftime(pre_formatted_path), basename)

        os.makedirs(path, exist_ok=True) # make directories, unless they already exist

        new_path = osp.join(path, f) # the path of the file after being copied

        # check if the file exists if overwrite is False
        if not overwrite and osp.isfile(new_path):
            # overwrite if prompted
            ans = input(f"File exists:  {new_path}\noverwrite? (y/n)  ")
            if ans[0] == "n":
                print("Ignoring:  " + f)
                continue

        copy2(floc, path) # copy2() preserves metadata
        print(f"Copying file:  {f} → {new_path}")

        if not copy_files: # delete old files?
            os.remove(floc)


if __name__ == "__main__":
    if not osp.isdir(sorting_dir): # make sort dir if it doesn't exist
        os.mkdir(sorting_dir)

    main()
