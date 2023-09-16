from lyricsgenius import Genius

genius = Genius("ZI8bJmhp-URBvInIRXIEN1tkR0trUmb-3acnZgZcOlqUaPG3XEBVbUrg9BtfLA5F")

# Im Gegensatz zum Code in "Webscraping_Billboard2010", versuchte ich hier die Titel ohne zugehörige Künstler
# zu suchen, was in diesem Fall bessere Ergebnisse lieferte:

titel = ["California Gurls", "Airplanes", "Telephone", "Cooler Than Me (Single Mix)", "Imma Be", "Sexy Bitch", "I Gotta Feeling", "Meet Me Halfway", "Rock That Body"]
for t in titel:
    song = genius.search_song(t)
    ly = song.lyrics
    print(ly, "\n\n")



