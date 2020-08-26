# Official World Golf Ranking Scraper
***

**Introduction:**

Web scraping program to obtain data from Official World Golf Ranking.
***

**Context:**

The Official World Golf Ranking is a system for rating the performance level of male professional golfers. It was started in 1986. [[1]](https://en.wikipedia.org/wiki/Official_World_Golf_Ranking)

The rankings are based on a player's position in individual tournaments (i.e. not pairs or team events) over a "rolling" two-year period. New rankings are produced each week. During 2018, nearly 400 tournaments on 20 tours were covered by the ranking system. All players competing in these tournaments are included in the rankings. In 2019, 23 tours will factor into the world rankings. [[1]](https://en.wikipedia.org/wiki/Official_World_Golf_Ranking)

The World Ranking Points for each player are accumulated over a two year “rolling” period with the points awarded for each tournament maintained for a 13-week period to place additional emphasis on recent performances. [[2]](http://www.owgr.com/about)

Ranking points are then reduced in equal decrements for the remaining 91 weeks of the two year Ranking period. Each player is then ranked according to his average points per tournament, which is determined by dividing his total number of points by the tournaments he has played over that two-year period. [[2]](http://www.owgr.com/about)

There is a minimum divisor of 40 tournaments over the two year ranking period and a maximum divisor of a player’s last 52 tournaments. [[2]](http://www.owgr.com/about)

Simply put, a golfer's World Ranking is obtained by dividing their points total by the number of events they have played, which gives their average. Players are then ranked; a higher average yields a higher rank. [[1]](https://en.wikipedia.org/wiki/Official_World_Golf_Ranking)
***

**Tours Included in the Rankings:**

- PGA Tour

- European Tour

- Asian Tour (not a charter member of the Federation)

- PGA Tour of Australasia

- Japan Golf Tour

- Sunshine Tour

- Korn Ferry Tour

- Challenge Tour

- PGA Tour Canada

- Golf Tour

- Korean Tour

- PGA Tour Latinoamérica

- Asian Development Tour

- PGA Tour China

- Alps Tour

- Nordic Golf League

- PGA EuroPro Tour

- ProGolf Tour

- MENA Golf Tour

- Big Easy Tour

- China Tour

- All Thailand Golf Tour

- Professional Golf Tour of India

- Abema TV Tour
***

**Scraping Programs:**

- OWGR_Player.py

   - Tournament performance of every player that has been ranked by the Official World Golf Ranking.
***

**Data:**

- The data was acquired from the [Official World Golf Ranking](http://www.owgr.com/ranking) website.

- Stored in a long data format.

***

**Collection Method:**

- Acquired the data using the Python library BeautifulSoup. Manipulated data using the Pandas & NumPy libraries.
***

**Acknowledgements:**

- Data scraped from: [Official World Golf Ranking](http://www.owgr.com/ranking)
***

**Inspirations:**

- Can this data be used to predict who will win upcoming tournaments?

- Can we predict the players that will make the tournament cuts?
***

**Disclaimer:**

The Official World Golf Ranking website contains plenty of messy data in the 'Name' column. There are still records where there is not enough information for me to infer the proper name of the athlete. If the name contains a date within brackets it is because there are two players with the same name. The date is the birth date of the athlete and is used to uniquely identify athletes with the same name.
***

**Questions, Concerns & Suggestions:**

- Feel free to email me for questions, concerns or suggestions, bradklassen@outlook.com
***

**Resources**

[1] https://en.wikipedia.org/wiki/Official_World_Golf_Ranking


[2] http://www.owgr.com/about
