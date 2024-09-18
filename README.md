# Legacy Baptist Church Fall Fair Data Pipeline

The project aimed to automate player leaderboard calculations using Google Sheets as a read/write database that could be displayed on a web server for near real-time updates. Our church used pen and paper two years ago to calculate and tally up scores. Last year, we used Google Sheets. Our annual fall fair is September 29th, 2024 where the goal is to provide near real-time updates publicly available to the church congregation. 

Tools/Technologies Used:
- Python
- HTML/CSS
- Google Sheets API/Google Cloud Platform
- Pandas
- Django
- Websockets

Data Flow Explained:
- Volunteers at each mini-game booth input player scores from their mobile devices onto the master spreadsheet
- Using the Google Sheets API, the data is extracted and transformed into a variety of point leader tables in an HTML format
- Using Django for the web framework, HTML and CSS are used to format the webserver to display leaderboard data
- Websockets are used to refresh data every 3 seconds for near real-time updates
- The local web server is then displayed on a TV in the church for participants to see

Church Website: https://legacybaptist.church/

![alt text](https://github.com/jobcabanto/Legacy-Baptist-Fall-Fair/blob/main/lbcleaderboard/static/website_sample.png)
