# fundatascraper

A web scraper that that grabs details of Canadian mutual funds from fundata.com.

The scrape_fund_details.py script will get a list of all mutual fund pages on fundata.com, scrape the details from each one, and save those details as pandas dataframes in pickle files.

(I probably won't contribute much more to this for some time as the use case I had for it didn't work out)


## TODO

* Add a setup script.
* Allow user to configure wait time in beteen page reads.
* Add a feature that will save scraping progress when script is stopped before finishing. The scraping could resume from the same point when the script is started again.
* Add some test cases.