# WCA Data Analyzer
One day I was wondering - What is the overall average of all solves in the WCA database? Sadly, I wasn't able to find this information anywhere on the internet, so I made this. It's a simple command line program, which fetches data from [the Unofficial WCA Public API]("https://wca-rest-api.robiningelbrecht.be") and calculates the average. It also allows simple filtering of the results.

# Installation
Installation is as simple as cloning the repository and installing the requirements from `requirements.txt`.

# Usage
To launch the program just execute the `cli.py` file, for example `py cli.py`. This is the most minimal way of running it. It calculates the average of all solves, no matter when or what event. You can also add additional arguments to filter the data.

- `--competition-parameters`, `-c` - Parameters for fetching competition data from the API. This is where you want to narrow your results the most, since it has a big effect on run time. You can set set things like the year of when the competitions took place (example: `py cli.py -c 2023`) or what event (example: `py cli.py -c 333`). You can read what exactly you can put here in [the Unofficial WCA Public API]("https://wca-rest-api.robiningelbrecht.be")'s documentation.

- `--solve-parameters`, `-s` - Parameters for fetching solve data from competitions. Allows for specifing events (example: `py cli.py -s 444`). What exactly can be put be here is explained in [the docs]("https://wca-rest-api.robiningelbrecht.be").

The program may throw errors when fetching data from some competitions. <b>This is not a problem.</b> It's most often caused by competitions which don't have a certain event or haven't happened yet. If you see a 404 error, it's most likely this specific competition didn't have the event you're looking for.

### Examples:
- `py cli.py -c 2023 -s 333` - Fetches all competitions from 2023 and calculates the average of all 3x3x3 solves.
- `py cli.py -c 2023/01 -s 333` - Fetches all competitions from january 2023 and calculates the average of all 3x3x3 solves.
- `py cli.py -c 333` - Fetches all competitions which had a 3x3x3 event and calculates the average of all events.
- `py cli.py -c 333 -s 444` - Fetches all competitions which had a 3x3x3 event and calculates the average of all 4x4x4 solves.