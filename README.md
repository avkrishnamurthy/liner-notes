# Liner Notes

Liner Notes is a full-stack web app that is a platform for music enthusiasts to share their musical opinions with a community. The idea for this project came from my sister. She is an avid user of the movie reviewing app Letterboxd, and wanted a way to review music and albums in the same way, and to be able to share that with her friends and other music lovers. I thought it was a great idea and would be a fun way to share my music taste with my friends and family. As a result, Liner Notes was born, and I started working every day to create it. A month later, it is online, and being used by friends and family to review albums and show off their favorite songs and albums. The main function of Liner Notes is to serve as an album reviewing app, where users can rate and review their favorite albums, sharing them with other users that they can follow. Every user has a custom feed, consisting of reviews made by other users that they follow. In addition to a user's album reviews, albums can be favorited and displayed on your profile as a way to showcase the albums that you love. Also on your profile will be your top 5 spotify tracks.

## How it works
The backend is created in Python. It utilizes Flask to create the backend logic and endpoints. The database used is PostgreSQL, a relational database, for efficient data storage and retrieval. The app employs SQLAlchemy, a powerful Object-Relational-Mapping (ORM) library, for seamless database interaction. The app integrates the Spotify Web API to enable features such as album search and user-specific top tracks. This allows users to search for albums by the artist, utilizing the Spotify API's rich music catalog. The app also implements Spotify's authorization code flow to facilitate secure access to users' Spotify data. The frontend employs JavaScript to enhance interactivity and manipulate the Document Object Model (DOM). Web templates were created Jinja2, and the styling was done with CSS.

## See it in action

[Try it for yourself](https://liner-notes-627b78c2d8e8.herokuapp.com/)


[Watch the demo](https://www.youtube.com/watch?v=BPlUprQ1PSA)

## Photos
<img width="1420" alt="profile" src="https://github.com/avkrishnamurthy/liner-notes/assets/46771241/5e231ad4-e236-47e7-8ef8-86006ff2e173">
<img width="1440" alt="linernotes" src="https://github.com/avkrishnamurthy/liner-notes/assets/46771241/0a012e72-90f3-4d5b-99ad-1e8fb8b09c89">

![feedRenamed](https://github.com/avkrishnamurthy/liner-notes/assets/46771241/ddc1562b-76f3-4fbf-9f87-d23a667edbc0)

# Technologies

<img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white">
<img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white">
<img src="https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E">
<img src="https://img.shields.io/badge/Spotify-1ED760?style=for-the-badge&logo=spotify&logoColor=white">
<img src="https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white">
<img src="https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black">
<img src="https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white">
<img src="https://custom-icon-badges.demolab.com/badge/-SQLAlchemy-aqua.svg?logo=sqlalchemy1"/>
