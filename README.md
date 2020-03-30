# gallery_sorter

Will sort photos and videos with the format `IMG_YYYYmmDD` or `VID_YYYYmmDD` into pre-determined directories.

## Requirements
• >= python 3.7

## Usage

Put `gallery_sort.py` adjacent to the `sort` directory.  Put all photos and videos you wish to sort in `sort`, then run `python gallery_sort.py`

Default directory structure is:
```
gallery_sort.py
sort/
  files.jpg
  to.mp4
  sort.jpeg
  IMG_20200109_180332.jpg
  IMG_20200122_194152_790.jpg
  VID_20200123.mp4

2020/
  01 January/
    Photos/
      IMG_20200109_180332.jpg
      IMG_20200122_194152_790.jpg
    Videos/
      VID_20200123.mp4
```


## Default Configuration
```
# The Directory to sort from
sorting_dir = "sort"

# Whether to separate videos from images
separate_filetypes = True

# The directory to put images and videos
images_dir = "Photos"
videos_dir = "Videos"

# The directory structure to sort into (supports strftime format codes)
# https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
path_format = ["%Y", "%m %B"]

# Whether to copy the files, or move them
copy_files = True

# Overwrite files if they exist
overwrite = False
```
