# Sky High
**Sky High** is a web application designed to help individuals with their mental well being. This application is mainly purposed to allow users to generate images based on information from their day. This application also allows the user to search for the nearest therapists near the user with their given location. Additionally, the platform also provides daily inspirational quotes. 

## *Why?*
The generated images are saved and lets the user come back and review on past happiness that can allow them to reminisce with their current selves and be happy again. The therapist finders can help the user know that help is always around the corner if they need it. The daily quotes can mean a lot to anyone, even a couple positive words can change a persons outlook on life. 

## **Features**
Whiteboard: Generates images based on a daily occurrences given by the user.

Therapist Finder: Locate therapists nearby by entering your current location (City, State or ZIP).

Daily Inspirational Quote: Start your day with uplifting words to encourage mindfulness and positivity.

User-Friendly Interface: A positive and clean user-interface where all tools are readily available and visible to the user.

Gallery: Work in progress, and should be finished soon. <!-- Not gonna pull a GTA 6-->

## Tech Stack
Frontend: HTML, CSS, Bootstrap, and JavaScript for a clean and responsive user interface.

Backend: Flask and Python with AI-powered functionalities to enhance image generation.

Database: SQL for managing user interactions and login information.

Geolocation: Yelp Geolocation API for accurate location-based therapist searches.

Inspirational Quotes: ZenQuotes API for delivering daily inspirational quotes.

## Authors
* Oluwajembola Orioke (Frontend/Backend Developer) <!-- Might be the goat -->
* eefward (Frontend Developer) <!-- Decent at best (and might not be straight) -->
* GuestyTheBesty (Backend Developer) <!-- Completely Straight -->

## How to run
1. Install the required libaries (You need Python): $pip install -r requirements
<br></br>
2. Create a "secret.py" file with your own keys

* Azure OpenAI: https://learn.microsoft.com/en-us/azure/api-management/api-management-authenticate-authorize-azure-openai

* Yelp Geolocation: https://docs.developer.yelp.com/reference/v3_business_search

* ImgBB: https://api.imgbb.com/
<br></br>
3. Run: $python app.py