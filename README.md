# stresser
Simple python script for sending a plenty amount of HTTP-requests to an specified address

## How to run the script
1. Clone the repository and enter its directory:
```
> git clone git@github.com:kapturoff/stresser.git
> cd stresser
```
2. Install dependencies:
```
> pip install -r requirements.txt
```
3. Run the script:
```
> python script.py --address=http://your_server_to_test/ --threads=8 --duration=30
```

The address and threads count parameters must be set in the script arguments. Duration parameter is not required (default: 10) and it's responsible for the duration of running the script. It's specified in _seconds_.
