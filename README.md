# WODatHome

My first full-stack capstone project for the Springboard Software Engineering Career Track.

This app is now [deployed on heroku](https://wod-at-home.herokuapp.com/).

Live Link: https://wod-at-home.herokuapp.com/

Wireframes (created by drawIO) can be found [here](https://drive.google.com/file/d/1yAY6GoaadWmxEO3Tsi-nS69-XsKmUaJ0/view?usp=sharing).

---

### **Tools Used**

This app will make use of the [wger REST API](https://wger.de/en/software/api) for access to workout information and images. The local PostgerSQL database has been seeded with data from this API.

Styling was achieved using [Bootstrap](https://getbootstrap.com/) and the [Bootswatch Flatly Template](https://bootswatch.com/).

Other Tools

- Flask
- SQL/PostgreSQL
- SQLAlchemy
- bcrypt
- WTForms
- jQuery
- axios (using CSRF protection from WTForms)

---

### **User Flow**

_Before registering_, a user is able to browse different exercises based on different criteria including, but not limited to, available equipment. Users will be required to register before they are able to create/save workouts and log the results of any workouts.

Once registered, users are able will have access to all of their saved workouts as well as their workout history of logged workouts.

New users should begin their experience by creating their first workout. After choosing between creating an AMRAP, EMOM, or RFT they will be taken to a page where they can select exercises from a list of exercises from the WGER API that have been filtered to their needs/specifications. Once an exercise has been added to the workout, users can specify how many reps or seconds are required for that particular exercise. During this stage, Local Storage will be utilized so that if a user checks on the details of an exercise or adjusts their search filters the specifics of their workout list will be unaffected.

Once the workout is saved, it will be added to the user's homepage and will remain available until it is deleted by the user.

Users have the option to execute any of their saved workouts. For the execution of the workouts, users will be taken to a window with a timer that is created specifically for this workout. Once the timer is started, the window will display instructions for the current round/stage of the workout, including what exercises should be done.

From this window users are able (and encouraged) to log their results. The date and workout will be stored automatically, but the user will need to include a note if they want record of their actual results for that day. All logged results can be accessed from the "Your History" tab. This is a great way to track your growth, or to just look back and admire your previous accomplishments!

---

### **Running the App Locally (python3 and PostgreSQL required)**

Setting up your Secret file

1. You will need need an API key to fill the database. Visit the [wger REST API](https://wger.de/en/software/api) website and create an account. When you are signed in you can generate an API KEY.
2. Create a file named <i>secret.py</i> on the same level as _app.py_.
3. In _secret.py_ define a variable called **API_SECRET_KEY** and set it equal to your API KEY as a string.

Next, type the following into the Terminal

1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `createdb WODatHome_db`
5. `python3 run fetch.py`

The last step may take up to five minutes to run. Once complete, the database will be filled and a sample user will already be registered. This user has a username of 'Test1' and a password set to 'Password5'. This user will already have one stored workout.
