# WODatHome

My first full-stack capstone project for the Springboard Software Engineering Career Track.

**Status:** In development. Not ready to deploy.

**Goal:** The website will allow users to create their own HIIT (high-intensity interval training) workout from a template. They will have options for the structure of the workout (AMRAP, RFT, EMOM) and access to a database of different workouts and their descriptions. Users can search the database by type of workout or muscle group targeted. Users can perform their workout with this screen up and the website will show descriptions/pictures of the specific exercises of the workout as well as an appropriate timer. Logged-in users will be able to save their workouts to be reused and can keep track of the workout results over time.

This app will make use of the [wger REST API](https://wger.de/en/software/api) for access to workout information and images.

Wireframes (created by drawIO) can be found [here](https://drive.google.com/file/d/1yAY6GoaadWmxEO3Tsi-nS69-XsKmUaJ0/view?usp=sharing).

---
**User Flow**
*Before registering* a user is able to browse different exercises based on different criteria including, but not limited to, available equipment. Users will be required to register before they are able to create/save workouts and log the results of any workouts.



---

**Running the App (python3 and PostgreSQL required)**

Setting up your Secret file


1. You will need need an API key to fill the database. Visit the [wger REST API](https://wger.de/en/software/api) website and create an account. When you are signed in you can generate an API KEY.
2. Create a file named <i>secret.py</i> on the same level as *app.py*. 
3. In *secret.py* define a variable called **API\_SECRET\_KEY** and set it equal to your API KEY as a string.
4. In *secret.py*, also define a variable called **sample\_password** and set it equal to a string of your choosing. This will be the password for the sample user (with username - Test1). 

Next, type the following into the Terminal


1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `createdb WODatHome_db`
5. `ipython`
6. `%run app.py`
7. `fetch.execute_all()`


The last step may take up to five minutes to run. Once complete, the database will be filled and a sample user will already be registered. This user has a username of 'Test1' and a password set to whatever you picked in Step 4 of "Setting up your Secret file". This user will already have one stored workout.
