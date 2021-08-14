# lo2ta
## Project Motivation
Lo2ta is a car ad recommendation enigne deployed on django web app. It recommends the best deals from all the ads available on OLX for any model that you choose. 

## How To Use
First you should clone this repo into your local machine, then if change directory to `mysite`. After that run `python manage.py runserver`. If everything is okay you should see `Starting development server at http://127.0.0.1:8000/` somewhere in the output, and then you can access the web app using the link.

In the homepage you'll see two forms:
1. One is for searching all models that have ads falling in a price range that you specifiy
2. The other one is for searching for specific car models

Either way, when you finally select a model from the models shown in the price results, or select a model from the second form, you will get a list of recommendations ranked from top to bottom with the link of each ad so you can check it out in the website.


