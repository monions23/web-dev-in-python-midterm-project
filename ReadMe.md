## Meredith Onions Midterm Project

**_Note: update for database integration and user authorization is viewable below._**

### TVTracker: An Application To Track Your TV Watching Habits

My idea for this app stemmed from the realization that there are many apps and websites where one can track the movies they watch. However, this type of feature does not tend to include ways to track television shows. With the prevalence of streaming services today - and the sheer abundance of show options that are available to us - it can be difficult to keep track of everything one is watching. I created this prototype to help solve this problem: maybe a streamlined app that can track in-progress shows across streaming services would help users be more organized and knowledgeable about their watch activity.

### Set Up

After cloning this repository, create a virtual environment in your local project folder. Enter the following terminal command:

```
python -m venv venv
```

To activate the venv, run the following command on MacOS:

```
source venv/bin/activate
```

Or, on Windows, run:

```
.\venv\Scripts\activate
```

Next, it should be noted project uses FastAPI and Uvicorn. All necessary libraries are listed in `requirements.txt`. To install them, run the following command:

```
pip install -r requirements.txt
```

### Notes About Project

This project, called TV Tracker, is similar to the To-Do App that we completed in class, with a few small exceptions. First, I renamed the Todo class to Show, and I added season and episode as class attributes:

```
# In tv_show.py:

class Show(BaseModel):
    id: int
    title: str
    desc: str
    season: int
    episode: int


class ShowRequest(BaseModel):
    title: str
    desc: str
    season: int
    episode: int

```

Then, I changed the back-end by renaming to-do related items (making them more semantically accurate in the context of a TV Show Tracker) and implementing the capability to take in a season and integer value. For example, the following is the updated POST request that adds a new show:

```
@show_router.post("", status_code=201)
async def create_new_show(tv_show: ShowRequest) -> Show:
    global global_id  # important, so that this variable will have value and tracked for every request
    global_id += 1
    new_show = Show(id=global_id, title=tv_show.title, desc=tv_show.desc, season = tv_show.season, episode = tv_show.episode)
    show_list.append(new_show)
    return new_show
```

Next, I modified the class names in `index.html` to be more semantically accurate. I added extra inputs to the edit and add modals for season and episode.

I also changed the JavaScript so it could take in a season and episode from the back-end and accurately render it. For example, upon adding a new show, I changed it so that any empty value (including season and episode) will render an error.

Finally, I added some styling to make it more individualized. This included changing the button colors and adding a hover effect to such buttons for better usability.

## Update: Database Integration and User Authentication

Note that any necessary installations for your venv can be viewed in requirements.txt.

### Database Integration

First, I wrote the Python script necessary to connect to a local MongoDB database in a new file called `database.py`.

I placed my database URL into .env as an environment variable. Note that the .env files is ignored by default when pushing to Git, so you will not see .env in my repository.

I ensured that the database URL matched a database I had created in MongoDB Compass (a GUI external to VSCode).

Then, I changed my Show class to inherit from Beanie's Document instead of Pydantic's BaseModel. This allowed it to handle database interactions instead of just basic data validation. I also ensured the id attribute of Show was a Beanie-defined id, not my own auto-incremented id. Finally, I defined the class as "show" in my class settings so it could correctly connect to the collection I created.

```
from typing import Optional

from pydantic import BaseModel, Field
from beanie import Document, PydanticObjectId

class Show(Document):
    id: Optional[PydanticObjectId] = Field(default=None, alias="_id")
    title: str
    desc: str
    season: int
    episode: int

    class Settings:
        name = "show"  # The exact name in MongoDB

```

After this, I changed `tv_show_routes.py` to account for the updated Document class. I added necessary Python script to insert, delete, and retrieve items from the database.

I also updated my front-end JavaScript file, `main.js`, so that it searched for \_id in its API requests instead of id, and I got rid of the data array that stored all of the Show instances locally. This allowed me to rely solely on API requests and the database for rendering the shows in the front-end.

Once all of this was complete, I had effectively connected my app to a MongoDB database.

## User Authentication

To begin, I created a folder entitled `auth` with three files: `authenticate.py`, `hash_password.py`, and `jwt_handler.py`. The `jwt_handler.py` file includes functions that can create and verify an access token, the `hash_password.py` file includes code that effectively hashes a user's password, and the `authenticate.py` file includes code that validates a token and allows users to access certain routes.

I used the professor's Github and my own final project for reference for the front-end html (seen in `login.html`), the user model (seen in `users.py`), and the user routes (seen in `user_routes.py`).

I created a users collection in MongoDB Compass to reflect where the user data would go.

Then, I created an `auth_routes.py` file to handle API requests for routes related to JWT authentication (signing up, signing in, and getting the current user through "\me"). Note that the current rendition of my app does not have a sign-in page; to create a new user, go to the "/docs" route to access all available FastAPI requests, and use the signup function to input your own email and password.

I created my own user using the signup request in FastAPI Docs, and then I tested out my login function. After some debugging, it worked! All that was left was to make it so the user was redirected to `index.html` when they successfully logged in (rather than just staying on `login.html`). To do this, I added the following code in `login.js` under the authentication API call:

```
localStorage.setItem("access_token", data.access_token); // this was here before - to save the token to local storage

window.location.href = "/index.html"; // NEW LINE - IMPORTANT FOR PAGE REDIRECT

msg.textContent = "Logged in!"; // this was here before - to update the msg
```

Finally, I added my own styling for the log-in page. That was added to `style.css`.
