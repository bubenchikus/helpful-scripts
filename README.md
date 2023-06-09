# helpful-scripts

Python scripts needed for managing my apps and files.

## image-processing scripts:

- **img-downscaling.py** - script for downscaling picture or all pictures in given folder. arguments: _--image_name (-n)_ - path to image; _--image_directory (-d)_ - will be used if image name not provided, default is current directory; _--max-megapixels (-m)_ - target resolution, pictures smaller than that will not be changed.

```
python3 img-downscaling.py -d ~/Desktop/pictures -m 2
```

- **img-to-webp.py** - script for converting images to .webp format or compressing existent .webp pictures. _--image_name (-n)_ and _--image_directory (-d)_ arguments are same as in img-downscaling.py. _--remove-originals (-r)_ - self-explanatory, but initially .webp pictures will be re-written anyway. _--min_size (-m)_ - pictures smaller than that (in kBs) will not be targeted. _--quality (-q)_ - compression level used while saving picture, value from 0 to 100, default 80.

```
python3 img-to-webp.py -d ~/Desktop/pictures -r True -m 30 -q 90
```

## apps scripts:

- **bubengogh-art-statistics.py** - collects and visualizes art statistics from bubengogh.com. result - monthly plot (with spline approximation) and yearly plot of works count by art categories.

```
python3 bubengogh-art-statistics.py
```

- **food-data-fetching.py** - fetches data from USDA database, than processes it and inserts into local mongodb collection. _--types (-t)_ argument defines which data types will be fetched (https://fdc.nal.usda.gov/data-documentation.html).

```
python3 food-data-fetching.py -t 'Foundation' 'Branded' 'Survey (FNDDS)' 'SR Legacy'
```
