## Meredith Onions Midterm Project

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
