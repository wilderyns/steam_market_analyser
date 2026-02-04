run.py
Just acts as a simple runner so the user can neatly run the application with python3 run.py

main.py
The root of the application. Attempts to set terminal size then verifies the dataset exists and is as expected. If the dataset doesn't exist the application can attempt to download it.
Main then continues to instaniate the main loop of the application and display the main menu whilst also handling main menu input 

dataset.py
Contains functions to check whether the dataset exists, check dataset integrity, and fetch the dataset from Kaggle

banner.py
A banner to make the application look nice and build an identity reminiscent of CLI apps of old

features.py
Informs the application about what libraries are available so available features can be presented. This was chosen so that users who may not have the required libraries can still utilise core application functionality

helpers.py
Miscallenous functions such as atempting to clear the terminal window, resizing the terminal, etc

models.py
Houses overarching data structures such as app state and dataset expected structure, as well as storing applied filters

user_input.py
Functions to handle user input constraints and sanitisation