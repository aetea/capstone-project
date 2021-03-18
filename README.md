# Overview 

**Wander-Vision** allows users to research major cities they'd like to live in. Get 
a sense of what life looks like there through various quality-of-life 
scores, and find out what travel restrictions are present during COVID-19. 

# Features 

**Search** 🔍 for cities and see how it scores on safety, cost of living, tolerance, 
healthcare, internet access and leisure & culture. 10/10 is best! 

City information and scores are shown at the urban area level. For example: San Francisco, 
Berkeley and San Jose all belong to the urban area "San Francisco Bay Area".

**Check** 📋 must-know COVID travel advisories for that city. Click the shortcut 
in the banner below the city name to jump there directly. 

Travel info is provided at the country level, and restrictions/procedures can 
differ depending on the traveller's place of origin. Refer to the sources 
linked in each item to see more details.

*Restrictions* indicate policies that prevent certain groups from entering the country.  
*Procedures* indicate medical, health or safety processes imposed on people 
entering the country.


Look forward to... 
- special map pins for places you've lived in
- get passport stamps for places you've lived in
- q&a time: get answers and advice from locals (past/present) of the 
places you're interested in

# Installation 

## Tech Stack

Wander-Vision runs on: 
* Python, PostgreSQL, Flask, Jinja - on the backend
* Javascript, jQuery, Bootstrap - on the frontend

*Additional libraries and tools are listed in requirements.txt*

## API Keys

The following APIs are also required:
* Teleport (for city scores)
* Sherpa (for travel advisories)
* Google Maps (for... maps) 

### 🔑 Prep
Obtain API keys:
* Sherpa: [apply here](https://www.joinsherpa.com/api/request-access)
* Google Maps (Javascript API): [see documentation here](https://developers.google.com/maps/documentation/javascript/get-api-key)

    *make sure to restrict your API key to avoid quota theft*

## Setup Instructions

1. Fork/clone this repository 
2. Create and activate a virtual environment 
    ```
    $ virtualenv env
    $ source env/bin/activate
    ```

3. Install dependencies 

    ```$ pip3 install -r requirements.txt```

4. Create a database

    ```$ createdb looksee```

5. (if you have prior data) Seed your database 

    ```$ python3 -i seed.py```

    *run interactively to check that data looks good after*

6. Run the app 

    ```$ python3 server.py```

7. Go to localhost:5000 in your browser and enjoy!
