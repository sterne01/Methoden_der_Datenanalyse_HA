# Benötigte Tools wurden zuvor in PyCharm 2023.1.2 unter "Preferences" als "Python Interpreter" für das Projekt installiert
# Tools in das Python Script importieren
import requests
from bs4 import BeautifulSoup
import pandas as pd
from lyricsgenius import Genius

# Gewünschte Website als URL-Variable speichern, mit "requests" library anfragen und mit BeautifulSoup den Inhalt der Website einlesen
URL = "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2010"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

# HTML Text der auf der Website vorhandenen Tabelle (Rang, Songtitel, Künstler*innen) anzeigen lassen
wiki_table = soup.find("table")
print(wiki_table)
# Man kann erkennen, dass der HTML-Tag "td" jeweils ein Set von Rang, Songtitel, Künstler*in enthält

# Listen erstellen, in die die Chart-Platzierung (number), Songtitel (titles) und Künstler*innen (artists) später eingespeist werden
list = []
number = []
titles = []
artists = []

# alle "td" Tags finden und deren Text zunächst in eine Liste zusammenführen
titles_artists_tags = wiki_table.find_all("td")
for td in titles_artists_tags:
    list.append(td.text)

# Liste mit Platzierungen, Songtiteln, Künstler*innen
print(list)

# Die Ränge, Songtitel und Küntler*innen in einzelne Listen aufteilen
i = 0
while i < len(list):
    number.append(list[i])
    i += 3

i = 1
while i < len(list):
    titles.append(list[i])
    i += 3

i = 2
while i < len(list):
    artists.append(list[i])
    i += 3

print(number)
print(titles)
print(artists)


# mit "Access Token" Zugang zu Genius anfragen
genius = Genius("ZI8bJmhp-URBvInIRXIEN1tkR0trUmb-3acnZgZcOlqUaPG3XEBVbUrg9BtfLA5F")

lyricslist = []

# jede Kombination (Titel, Künstler*innen) mit lyricsgenius auf der Genius Website anfragen und die Songtexte zu einer Liste hinzufügen
for (t, a) in zip(titles, artists):
    song = genius.search_song(t, a)
    ly = song.lyrics
    lyricslist.append(ly)

print(lyricslist)

# mit der pandas library ein Dataframe (Tabelle) erstellen mit den Spalten "Nummer", "Songtitel", "Künstler*innen" und "Songtext"
data = {"Nummer":number, "Songtitel":titles, "Künstler*innen":artists, "Songtext":lyricslist}
df = pd.DataFrame(data)
print(df)

# den Dataframe in ein .csv Dokument umwandeln und lokal speichern
df.to_csv('/Users/estern/Documents/Uni/Uni Trier/SoSe 23/Methoden der Datenanalyse (Mo Mi)/Hausarbeit/Billboard2010_Tabelle.csv')
