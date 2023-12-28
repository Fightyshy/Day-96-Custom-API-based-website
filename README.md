# day96-custom-api-based-website

A simple one-page interactive "Business Card" Style website using a API and some website scraping to present a summary of a character for a certain MMORPG. Character Summary and Raid Performance "pages" are complete, while the remaining pages are left as a template of what could be.
Done as part of the 100 Days of Code: The Complete Python Pro Bootcamp for 2023 course, [link here]([https://www.udemy.com/course/100-days-of-code/learn/practice/1251204#overview](https://www.udemy.com/course/100-days-of-code/))

All modules used are included in the requirements.txt, while relevant static files are contained in a static/assets folder. No database is used for this project, though there is a potential brainstorm to use one in a fork of this project.

In addition, the following resources were used:
- [FFLogs API documentation](https://www.archon.gg/ffxiv/articles/help/api-documentation), where we used the Authorization, Token, and Public URIs provided were used.
- [CSS Lodestone selectors](https://github.com/xivapi/lodestone-css-selectors) for help in scraping the relevant data off the Lodestone website, used both to fill the API query and provide content in lieu of XIVApi's own character GET endpoints not working at the time of repository creation.
- [Class Job icons](https://github.com/xivapi/classjob-icons/tree/master/icons) for well, class and job icons used in the website.
