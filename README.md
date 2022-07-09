# NHL 

[![Build](https://github.com/barbacbd/nhl/workflows/Build/badge.svg?branch=main&event=push)](https://github.com/barbacbd/nhl/actions/workflows/python-app.yml)
[![GitHub latest commit](https://img.shields.io/github/last-commit/barbacbd/nhl)](https://github.com/barbacbd/nhl/commit/)

The National Hockey League (NHL) was kind enough to provide all of the historical data on a free web interface. This project was created
to pull the data and analyze the data. The data is all loaded into python objects from the json encoded data that was pulled from the
NHL database. The documentation can be found [here](https://barbacbd.github.io/nhl/).


# References

The reader may find resources in [references](./refs). The references may include information that can be used after obtaining
information from this library.

# Pulling NHL Historical Data

The executable is called `NHLAPIPuller`:

The following are parameters,

```
usage: Pull NHL data from the web API based on the following parameters: 
       [-h] [-g GAMES [GAMES ...]] [-s {PRESEASON,REGULAR,PLAYOFFS,ALLSTAR}]
       [-y YEARS [YEARS ...]] [--dir DIR]

optional arguments:
  -h, --help            show this help message and exit
  -g GAMES [GAMES ...], --games GAMES [GAMES ...]
                        Type game for the years that are selected.
  -s {PRESEASON,REGULAR,PLAYOFFS,ALLSTAR}, --season {PRESEASON,REGULAR,PLAYOFFS,ALLSTAR}
                        Type of seasonal games for which the data should be
                        gathered.
  -y YEARS [YEARS ...], --years YEARS [YEARS ...]
                        The years of data that is requested.
  --dir DIR             Output directory.
```

**Notes:**
- _When no games are provided to the executable, all games for the valid years are pulled._
- _When no years are provided, all years from the start of the NHL to the current year are selected._


# Creating Python objects

Read in a file that contains the NHL data obtained from the api

```
from nhl import ParseFromFile

nhlData = ParseFromFile("/path/to/nhl_data.json")
```

# Utilizing NHL Data

Now the user can inspect the object with functions such as `tree`, `json` property, or the `__str__` override.

Tree will show information like:

```
example
  |
  -- child_1
  -- child_2
    |
    -- grandchild_1
example_2
  |
  -- child_1 

```

Json will provide a dictionary the same as the original data read in.

```
{
    "example": {
        "child_1": "data",
	"child_2": {
	    "grandchild_1": "data"
	}
    },
    "example_2": {
        "child_1": "data"
    }
}
```

The string override will provide the json output with a pretty format.

The user may also query for values from within the `NHLData` object.

```
result = nhlData.query("example.child_1")
```

The user may provide a string delimited by periods, or a list of string name of the variables.