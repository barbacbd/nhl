# NHL Core

[![Build](https://github.com/barbacbd/nhl/workflows/Build/badge.svg?branch=main&event=push)](https://github.com/barbacbd/nhl/actions/workflows/python-app.yml)
[![GitHub latest commit](https://img.shields.io/github/last-commit/barbacbd/nhl)](https://github.com/barbacbd/nhl/commit/)

The National Hockey League (NHL) was kind enough to provide all of the historical data on a free web interface. This library was created to parse the data that is retrieved from the api. After json data is retrieved it can be parsed by passing it to an `NHLData` python object. The documentation can be found [here](https://barbacbd.github.io/nhl/).

# Example 

In the following example, the data for a single team is retrieved.

```python
from nhl import NHLData, API_TEAM_ENDPOINT
from requests import get

json_data = get(API_TEAM_ENDPOINT).json()
if 'teams' in json_data:
    print(NHLData(json_data['teams'][0]))
```

The result is the following:

```
{
    "id": 1,
    "name": "New Jersey Devils",
    "link": "/api/v1/teams/1",
    "venue": {
        "name": "Prudential Center",
        "link": "/api/v1/venues/null",
        "city": "Newark",
        "timeZone": {
            "id": "America/New_York",
            "offset": -4,
            "tz": "EDT"
        }
    },
    "abbreviation": "NJD",
    "teamName": "Devils",
    "locationName": "New Jersey",
    "firstYearOfPlay": "1982",
    "division": {
        "id": 18,
        "name": "Metropolitan",
        "nameShort": "Metro",
        "link": "/api/v1/divisions/18",
        "abbreviation": "M"
    },
    "conference": {
        "id": 6,
        "name": "Eastern",
        "link": "/api/v1/conferences/6"
    },
    "franchise": {
        "franchiseId": 23,
        "teamName": "Devils",
        "link": "/api/v1/franchises/23"
    },
    "shortName": "New Jersey",
    "officialSiteUrl": "http://www.newjerseydevils.com/",
    "franchiseId": 23,
    "active": true
}
```

The user could also access the values directly. For instance getting the `teamName` would require:

```python
print(NHLData(json_data['teams'][0].teamName))
```

The user can also access nested values:

```python
print(NHLData(json_data['teams'][0].franchise.franchiseId))
```

# Copyright

All data is owned by the NHL. The result of each query will contain a copyright that should be included in all work. An example is shown below:

```
NHL and the NHL Shield are registered trademarks of the National Hockey League. NHL and NHL team marks are the property of the NHL and its teams. © NHL 2023. All Rights Reserved.
```