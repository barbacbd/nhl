# NHL Core

[![Build](https://github.com/barbacbd/nhl/workflows/Build/badge.svg?branch=main&event=push)](https://github.com/barbacbd/nhl/actions/workflows/python-app.yml)
[![GitHub latest commit](https://img.shields.io/github/last-commit/barbacbd/nhl)](https://github.com/barbacbd/nhl/commit/)

The National Hockey League (NHL) was kind enough to provide all of the historical data on a free web interface. This library was created to parse the data that is retrieved from the api. After json data is retrieved it can be parsed by passing it to an `NHLData` python object. The documentation can be found [here](https://barbacbd.github.io/nhl/).

# Endpoints

The enpoints can be found in the package [endpoints](https://github.com/barbacbd/nhl/blob/main/src/nhl_core/endpoints.py) file. All endpoints that are public can be accessed without a required [modifier](#modifiers). For example, the endpoint `API_TEAM_ENDPOINT` does not require additional information, so the user can perform a lookup immediately. 

Dynamic endpoints are the [endpoints](https://github.com/barbacbd/nhl/blob/main/src/nhl_core/endpoints.py) where modifiers are added to alter the functionality and returned information. Even though the `API_TEAM_ENDPOINT` does NOT require additional information, a user can provide more information using `_TEAM_MODIFIERS` and the function `create_team_endpoint` to create a more [descriptive url](#using-modifiers)

# Modifiers

Modifiers are content added to the end of a URL that will modify what is executed on the server. This information changes the returned value(s). 

## Get Modifier information

The user can either look up the modifier information [here](https://github.com/barbacbd/nhl/blob/main/src/nhl_core/endpoints.py), or they can access the function associated with the endpoint in which they are intending to modify. For example, the `API_TEAM_ENDPOINT` endpoint has a set of modifiers that can be accessed by `describe_team_endpoint()`. The returned value is a dictionary where the name the modifier is paired with details about the modifier.

## Using Modifiers

The endpoints that can be modified will have a function to create the new/modified endpoint. For example, `create_team_endpoint` will modify the `API_TEAM_ENDPOINT` when provided with a `team_id` and a dictionary of modifiers. 

```python
endpoint = create_team_endpoint(team_id="1", modifiers={"roster": "", "season": "20212022"})
```

The above example can be used to lookup the roster for the team with id = `1` during the 2021-2022 season. 

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