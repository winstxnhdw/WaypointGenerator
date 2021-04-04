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
Optional arguments:
-h, --help      show this help message and exit
-r, --random    generates a user-selected amount of random waypoints
-c, --click     generates user-selected waypoint positions   
```
> Press `Z` to undo a selected waypoint or revert to a previously generated set of waypoints. <br>
Press `X` to clear selected waypoints or to generate a new set of randomly generated waypoints. <br>
Press `C` to connect the last and first waypoints. <br>
Generated waypoints are **only exported at exit**.
>
## User Selected Waypoints
```bash
$ python main.py -c
```
<div align="center">
	<img src="resources/clickgen.gif" />
</div>

## Randomly Generated Waypoints
>The generated waypoints are passed piecewise through an algorithm that ensures that each line segment never intersects with each other.
>
```bash
$ python main.py -r <number-of-waypoints>
```
<div align="center">
	<img src="resources/randgen.gif" />
</div>

## Circular Generated Waypoints
circle_wp_gen.py is primarily used to generate waypoints of a certain radius and smoothness. The user is given two different smoothness modes which can be configured via the command-line interface.
```bash
$ cd circle
$ python circle_wp_gen.py -a <x-radius> -b <y-radius>
```
> The `numpy` library is required to run this script.
>
<div align="center">
	<img src="resources/circlegen.gif" />
</div>

```yaml
Optional arguments:
-h, --help       show this help message and exit
-a, --xradius    radius of an ellipse on the x-axis
-b, --yradius    radius of an ellipse on the y-axis 
```

## Additional Information
Exported waypoints can be imported using the `pandas` library with the following block.
```python
import pandas as pd

dir_path = 'waypoints.csv'
df = pd.read_csv(dir_path)
x = df['X-axis'].values.tolist()
y = df['Y-axis'].values.tolist()
```
