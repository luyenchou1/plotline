# Any Given Tuesday

Are NFL injuries really rising, or does it only feel that way? Every team's weekly injury report and reserve list since 2009.

## How it builds

```
src/fetch.sh        downloads the nflverse weekly injury reports (injuries_{season}.csv) and weekly rosters
                    (roster_weekly_{season}.csv) for 2009 to the current year, plus teams_colors_logos.csv, into src/raw/ (git-ignored)
src/assemble.py     -> src/data.json: per season and team, player-weeks Out on the report, on a reserve list, lost (union),
                       players who missed a game; league averages; Out listings by body part and position; the latest week's Out list
src/milestones.json rule changes and events (gold ticks)
build.py            -> index.html (data embedded), meta.json, card.json
```

Counting rule: a player-week is lost when a player is listed Out on that week's injury report, or is on a reserve list (status RES in the roster file) that week; a player on both is counted once. Non-injury listings (illness, personal) are excluded, as is the COVID reserve list where the roster data marks it (code R59, 2021 on). Regular season only. Historical team codes are mapped to current franchises (STL/SL to LA, SD to LAC, OAK to LV).

Known limits: the roster file's reserve listings are thin before 2016, so the page fades those years and reads the long-run trend from the Out series. Team identity is shown as abbreviation on a team-colour disc; logos and helmets are trademarks and are not used.

Runs from `.github/workflows/refresh.yml` on Mondays, Thursdays and Saturdays.

## Sources

- nflverse-data, injuries and weekly rosters. https://github.com/nflverse/nflverse-data (CC BY 4.0)
- Team names and colours: nflverse teams_colors_logos.csv
- League-published injury figures (not machine-readable, cited in the notes): https://www.nfl.com/playerhealthandsafety/health-and-wellness/injury-data/injury-data
