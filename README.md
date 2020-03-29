# gallery_sorter

Will sort photos and videos with the format `IMG_YYYYMMDD` or `VID_YYYYMMDD` into pre-determined directories.

## Usage

`python sort.py`

Default directory structure is:
```
sort/
  files.jpg
  to.mp4
  sort.jpeg
  IMG_20200109_180332.jpg
  IMG_20200122_194152_790.jpg
  VID_20200123.mp4

YYYY/
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
