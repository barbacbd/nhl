# NHL

The National Hockey League (NHL) was kind enough to provide all of the historical data on a free web interface. This project was created
to pull the data and analyze the data. The data is all loaded into python objects from the json encoded data that was pulled from the
NHL database.


# References

The reader may find resources in [references](./refs). The references may include information that can be used after obtaining
information from this library.

# Pulling NHL Historical Data


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