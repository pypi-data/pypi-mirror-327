Software Developer Kit (SDK) for PVRADAR platform.

https://pvradar.com

# Installation

```sh
pip install pvradar-sdk
```

# Usage

```python
import pandas as pd
from pvradar.sdk import PvradarSite, PvradarLocation, describe

interval = pd.Interval(pd.Timestamp('2020-01-01'), pd.Timestamp('2020-12-31T23:59:59'))
location = PvradarLocation(latitude=-23, longitude=115)
site = PvradarSite(location=location, interval=interval)
ghi = site.pvradar_resource_type('global_horizontal_irradiance')
print(ghi)
print(describe(ghi))
```
