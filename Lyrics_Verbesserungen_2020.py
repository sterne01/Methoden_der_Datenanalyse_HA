from lyricsgenius import Genius

genius = Genius("ZI8bJmhp-URBvInIRXIEN1tkR0trUmb-3acnZgZcOlqUaPG3XEBVbUrg9BtfLA5F")

# Bei einigen Titeln wurde der Anhang "(Remix)" hinzugefügt, da sonst die Soloversion heruntergeladen wurde.
# Bei den Namen der Künstler*innen probierte ich verschiedene Kombinationen, um am Ende die richtige Version des Songtexts zu erhalten.

titel = ["Rockstar", "Whats Poppin (Remix)", "Savage (Remix)", "Intentions", "No guidance", "High Fashion", "Laugh Now Cry Later", "Senorita", "Mood", "For the Night", "If the world was ending", "Godzilla", "Popstar", "Suicidal (Remix)", "The Woo", "Supalonely"]
artists = ["DaBaby", "Jack Harlow", "Megan Thee Stallion, Beyonce", "Justin Bieber", "Chris Brown", "Roddy Ricch", "Drake, Lil Durk", "Shawn Mendez", "24k Goldn", "Pop Smoke", "JP Saxe", "Eminem", "Dj Khaled", "YNW Melly", "Pop Smoke", "Benee"]

for t, a in zip(titel, artists):
    song = genius.search_song(t,a)
    ly = song.lyrics
    print(ly, "\n\n")

