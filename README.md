# gluster-BulkVolumeCreate
A tool to generate a large number of glusterfs volumes.

## Prerequisites
Python 3.x
Running gluster cluster.


## Installation
1. Download the project files from github.
```
git clone https://github.com/kshithijiyer/gluster-BulkVolumeCreate.git
```
2. Change directory to the project directory. 
```
cd gluster-BulkVolumeCreate
```
3. Now run the installation script.
```
python3 setup.py install
```
4. To check run ``` BulkVolumeCreate --help ```

## Usage
### Setting Up config file
Create a .conf file with the following structure:
```
hosts=host1,host2,host3,host4,host5
bricks=/bricks/brick1/,/bricks/brick2/,/bricks/brick3/,/bricks/brick4/,/bricks/brick5/,/bricks/brick6/,/bricks/brick7/
vol_name=test
```
Where ``` hosts ``` is the IP or hostnames of the peers in the gluster cluster, ``` bricks ``` are the paths to mount points where the bricks are mounted and ``` vol_name ``` is the base name of all the volumes. Edit the ``` example.conf ``` file available in the project folder. 
 
### Example commands
1. Creating 10 EC volumes.
```
BulkVolumeCreate -f example.conf -t ec -e 2x4+2 -n 10
```
2. Creating 100 arb volumes.
```
BulkVolumeCreate -f example.conf -t arb -e 1x2+1 -n 100
```
3. Creating 20 replica 3x3 volumes with prefix ``` hi_ ```.
```
BulkVolumeCreate -f example.conf -t rep -e 3x3 -n 20 -p hi

```


Another way of writing the same commands:
```
BulkVolumeCreate --config_file example.conf --type ec --expression 2x4+2 --number 10
BulkVolumeCreate --config_file example.conf --type arb --expression 1x2+1 --number 100
BulkVolumeCreate --config_file example.conf --type rep --expression 3x3 --number 20 --pefix hi
```
### Expression definition 
This is how you write expressions for BulkVolumeCreate which defines what will be the configuration for the volumes. 
 |  |Expression
:---:| :---: | :---:
1. |  | N
2. | rep | AxB
3. | arb | AxB+C
4. | ec  | AxD+R


No. | Type | Expression
--- | --- | ---
1 | dist | N
1 | 2 | 3
1 | 2 | 3
1 | 2 | 3

For more info do a ``` BulkVolumeCreate --help ``` or ``` BulkVolumeCreate -h ```.

## Built with 
[IDLE 3](https://www.python.org/downloads/)

## Author
[Kshithij Iyer](https://www.linkedin.com/in/kshithij-iyer/)

## Licence 
The project is released under BSD 2-Clause "Simplified" License.
