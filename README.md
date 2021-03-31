# WaypointGenerator
A simple python script that uses the `pandas` library to export generated waypoints into a CSV file. Waypoints can either be user-selected or randomly selected.

## Installation
```bash
# Install dependencies
$ pip install -r requirements.txt
```
## Usage
```bash
# Run the script
$ python main.py <flag> <value>
```

```yaml
Required arguments:
-h, --help      show this help message and exit
-r , --random   generates a user-selected amount of random waypoints
-c, --click     generates user-selected waypoint positions   
```
> Press `X` to clear selected waypoints or to generate a new set of randomly generated waypoints. <br>
Press `C` to connect the last and first waypoints.
>
## User-selected Waypoints
```bash
$ python main.py -c
```
<div align="center">
	<img src="resources/clickgen.gif" />
</div>

## Random Generated Waypoints
```bash
$ python main.py -r <number-of-waypoints>
```
<div align="center">
	<img src="resources/randgen.gif" />
</div>

## Additional Information
Exported waypoints can be imported using pandas
```python
import pandas as pd

dir_path = 'waypoints.csv'
df = pd.read_csv(dir_path)
x = df['X-axis'].values.tolist()
y = df['Y-axis'].values.tolist()
```