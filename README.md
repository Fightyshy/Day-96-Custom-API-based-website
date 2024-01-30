# FFXIV Adventurer's guild card thing 

A dynamically generated one-page interactive "business"/"calling" card style website whcih gathers information from multiple community-made APIs and website-scrapped data to present a condensed summary of a player's character and their achievements and activities, including
- Basic character information (Class levels, Free Company (Guild), Character's home Data-center and Server, etc)
- Endgame raiding performance (Savage/Ultimate raids)
- Collectables status (Achievements/Mounts/Minions)

Done as part of the 100 Days of Code: The Complete Python Pro Bootcamp for 2023 course, [link here](https://www.udemy.com/course/100-days-of-code/), but further refined into it's current state. The main branch has been updated with the current minimally viable build, however, any further refinements will be made on the 'full-implementation' branch before being merged with the main branch.

This project currently uses the following technologies:
- Frontend: HTML/CSS/Bootstrap, Javascript and jQuery for functionality/Request/Respsonse
- Backend: Python - Flask
- External API:
    - FFLogs (Uses GraphQL, documentation link below)
    - FFXIV-Collect (REST API, documentation link below)
**Disclaimer:** The frontend of the card was developed with assistance from AI (Using ChatGPT), with the basic structure and components being established, but fine-tuning and getting the exactly-desired functionality and appearence was personally done. The AI did **not** assist in the development of the backend and database components.

All Python modules used are included in the requirements.txt, while relevant static files are contained in a static/assets folder. At this stage, a database (and as a result, no SQLAlchemy) is not implemented yet. Character portraits are uploaded to a folder local to the project, and the editable character summary is rather a proof-of-concept and storing the data is not yet implemented. 

In addition, the following resources were used:
- [FFLogs API documentation](https://www.archon.gg/ffxiv/articles/help/api-documentation), where we used the Authorization, Token, and Public URIs provided were used.
- [CSS Lodestone selectors](https://github.com/xivapi/lodestone-css-selectors) for help in scraping the relevant data off the Lodestone website, used both to fill the API query and provide content in lieu of XIVApi's own character GET endpoints not working at the time of repository creation.
- [Class Job icons](https://github.com/xivapi/classjob-icons/tree/master/icons) for well, class and job icons used in the website.
- [FFXIV-Collect API](https://documenter.getpostman.com/view/1779678/TzXzDHM1) for collectable data requests and tracked character requests.
