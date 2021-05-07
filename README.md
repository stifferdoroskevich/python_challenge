# IP Validation - Geolocation and RDAP
# Summary
Program focused on retrieving and parsing RDAP data and Geolocation for IPv4 addresses.

# Features
- Parses IP from a file.
- Retrieves RDAP Data.
- Retrieves Geolocation Data. 
- Save information in a local database (SQLite) for querying.
   
## Technical Requirements
- Decouple components.
- Avoid 3rd party packages for Geoip/RDAP queries.
- Program operational through CLI.
- Add optimization to HTTP requests.
- Add caching.
   
   
# How to setup the application 
```bash
# Clone this repository
$ https://github.com/stifferdoroskevich/python_challenge.git
$ cd python_challenge

# Create Virtual enviroment
$ python3 -m venv venv
$ source venv/bin/activate

# Install dependencies
$ pip install --upgrade pip
$ pip install -r requirements.txt

# Run the main function "main.py"
$ python main.py

# Select one of the five options
1. Populate Database with small dataset
2. Populate Database with full dataset
3. Populate Database with file
4. Return All IP Rdap Information
5. Return All IP Geolocation
6. Clean All Data from Database

To pass directly a file.
Put the file inside the "test_data" folder and run:
$ python main_validator.py --file ["name_of_the_file.txt"]


``` 
