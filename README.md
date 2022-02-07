# WODatHome

My first full-stack capstone project for the Springboard Career Track.

**Status:** In development. Not ready to deploy.

**Goal:** The website will allow users to create their own HIIT (high-intensity interval training) workout from a template. They will have options for the structure of the workout (AMRAP, RFT, EMOM) and access to a database of different workouts and their descriptions. Users can search the database by type of workout or muscle group targeted. Users can perform their workout with this screen up and the website will show descriptions/pictures of the specific exercises of the workout as well as an appropriate timer. Logged-in users will be able to save their workouts to be reused and can keep track of the workout results over time.

This app will make use of the [wger REST API](https://wger.de/en/software/api) for access to workout information and images.

Wireframes (created by drawIO) can be found [here](https://drive.google.com/file/d/1yAY6GoaadWmxEO3Tsi-nS69-XsKmUaJ0/view?usp=sharing).

**Running the App (python3 and PostgreSQL required)**

---

<u>Setting up your Secret file</u>

<ol>
<li>You will need need an API key to fill the database. Visit the [wger REST API](https://wger.de/en/software/api) website and create an account. When you are signed in you can generate an API KEY.</li>
<li>Create a file named <i>secret.py</i> on the same level as *app.py*. </li>
<li>In *secret.py* define a variable called **API\_SECRET\_KEY** and set it equal to your API KEY as a string.</li>
<li>In *secret.py*, also define a variable called **sample\_password** and set it equal to a string of your choosing. This will be the password for the sample user (with username - Test1). 
</ol>

<u>Next, type the following into the Terminal</u>

<ol>
<li>`python3 -m venv venv`</li>
<li>`source venv/bin/activate`</li>
<li>`pip install -r requirements.txt`</li>
<li>`createdb WODatHome_db`</li>
<li>`ipython`</li>
<li>`%run app.py`</li>
<li>`fetch.execute_all()`</li>
</ol>
The last step may take up to five minutes to run. Once complete, the database will be filled and a sample user will already be registered. This user has a username of 'Test1' and a password set to whatever you picked in Step 4 of "Setting up your Secret file". This user will already have one stored workout.
