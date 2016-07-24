# UltimateStatisticsAnalysis

Small program I threw together to analyze statistics from intramural ultimate games at UofT.

Players are stored in a 'master roster' as a text file One player per line with three items per line - (name, number, sex)

Games are stored as a text file.
Each line outlines a possession by the team in question. 
Points are made up of multiple possession (until a point is scored). 
First line/possession in a point is just the players on the field.
Points are separated by lines contains a single '#'.
Players are noted within a single possession as three letter acronyms.
Players are separated within a possession by a dash.
  - Example: Rub-Chr-Tif 
    - Indicates Rub threw to Chr who attempted to throw to Tif (incomplete)

Last pair of acronyms indicate players who were involved in turning the disc over.
If a point is scored then the possession ends in '-p'.
If a point ends a game then the possession ends in '-g'.

Versions:
(Python 2.7.5)
(xlrd 0.9.2)
(xlwt 0.7.5)

Enjoy!
