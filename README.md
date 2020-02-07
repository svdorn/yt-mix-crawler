# yt-mix-crawler
Crawls for mixes on YT.

## Usage
Run the run_crawl.py script. It takes two arguments - input_filename (required) and output_filename (required).
```
python3 run_crawl.py [input_filename] [output_filename]
```
The input_filename is a CSV and should be located in the /input folder. The output_filename is the filename you want for the output and will be put in the /output folder upon succeful completion of the script.

Example:
```
python3 run_crawl.py input_playlists output_playlists
```

## Built With
-   [Python](https://www.python.org/)
-   [Pandas](https://pandas.pydata.org/)
-   [Beautiful Soup](https://pypi.org/project/beautifulsoup4/)
