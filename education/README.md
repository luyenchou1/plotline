# The Report Card

American school results since 1990 against what the country spends per pupil, and against the rest of the world.

## How it builds

```
src/fetch.sh        pulls the raw sources into src/raw/ (git-ignored), then runs assemble.py
                    - PISA, all rounds through 2025, three subjects: OECD PISA 2025 Results Vol. I, Annex B1 tables I.B1.2a.36-38
                      (StatLink xlsx https://stat.link/files/73451bc5-en/mrq53f.xlsx); primary where present
                    - PISA math and reading fallback: Our World in Data grapher CSVs (OECD data)
                    - PISA science fallback: World Bank API, indicator LO.PISA.SCI (through 2018)
                    - NAEP: nationsreportcard.gov data service, one request per assessment year
                      (the API rejects year lists; years before 1996 need the R2 sample suffix)
                      mean (MN:MN), share at/above Proficient (ALC:AP), and from 2013 the percentiles (PC:P1..P9),
                      parents' education (variable PARED, grade 8) and lunch eligibility (SLUNCH3, served through 2022)
                    - Spending per pupil: NCES Digest table 236.55, HTML (newest edition that exists)
                    - Spending per student, OECD countries: OECD SDMX API, DF_UOE_INDIC_FIN_PERSTUD
src/assemble.py     -> src/data.json
src/milestones.json the gold ticks (id, date, name, title, text, url)
build.py            -> index.html (data embedded), meta.json, card.json
```

Every fetch keeps the previous file if the new download fails or is empty, so a source outage does not blank the page. Runs weekly from `.github/workflows/refresh.yml`.

## Sources

- NAEP, National Center for Education Statistics. https://www.nationsreportcard.gov/ (public domain)
- PISA, OECD (CC BY 4.0), with Our World in Data (CC BY) and the World Bank (CC BY 4.0) as fallbacks
- NCES Digest of Education Statistics, table 236.55 (public domain)
- OECD Education at a Glance, expenditure per student (OECD terms of use)

When the next PISA round is published (2028 results, due 2029), point `fetch.sh` at the new volume's Annex B1 StatLink; the sheet names and layout have been stable across editions.
