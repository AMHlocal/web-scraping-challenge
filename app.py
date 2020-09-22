#dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars
import os

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

#route to use index.html
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars=mars)

#use /scrape to scrape function
@app.route("/scrape")
def scrape():
    # Run the scrape function
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_news()
    mars_data = scrape_mars.featured_image()
    mars_data = scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.hemispheres()


    # Update the Mongo database using update and upsert=True
    mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
 