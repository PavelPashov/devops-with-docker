## Fasta manipulation scripts

### Requirements
Python 3.8 is required to run the scripts

Please run the below:

```
python -m pip install -r requirements.txt
```

### Instructions
Run the below in order to get more information about a script

```
 ./repacle_header.py --help
 ./replace_n.py --help
```

### Usage
`replace_header.py` will replace the header in a .fa file based on the file name
and the selected delimiter and range, it will also change any Xs to Ns inside the file

`replace_n.py` will repace all occurances of two or more Ns in a .fasta file with
a new header or a 10 000 Ns based on the user input
