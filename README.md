# FFXIV Adventurer's guild card thing 

A simple one-page (currently proof of concept) interactive "business"/"calling" card style website using multiple community-made APIs and Lodestone scraped data to present a summary of a character and the activities they've done, including
- Basic character information (Class levels, FC, DC and server, etc)
- Savage/Ultimate raids
- Mounts/Minions/Achievements owned
- Housing/Roleplaying activiets (really selling that business card vibe)
- Probably more as I make it up
Currently, only the first three have had any progress. With planning on how to do Housing/Roleplay still being worked on.

Originally done as part of day 96 of the 100 Days of Code: The Complete Python Pro Bootcamp for 2023 course, [link here]([https://www.udemy.com/course/100-days-of-code/learn/practice/1251204#overview](https://www.udemy.com/course/100-days-of-code/)), which this is currently a branch of.
All Python modules used are included in the requirements.txt, while relevant static files are contained in a static/assets folder.

In addition, the following resources were used:
- [FFLogs API documentation](https://www.archon.gg/ffxiv/articles/help/api-documentation), where we used the Authorization, Token, and Public URIs provided were used.
- [CSS Lodestone selectors](https://github.com/xivapi/lodestone-css-selectors) for help in scraping the relevant data off the Lodestone website, used both to fill the API query and provide content in lieu of XIVApi's own character GET endpoints not working at the time of repository creation.
- [Class Job icons](https://github.com/xivapi/classjob-icons/tree/master/icons) for well, class and job icons used in the website.
- [FFXIV-Collect API](https://documenter.getpostman.com/view/1779678/TzXzDHM1) for collectable data requests and tracked character requests.
