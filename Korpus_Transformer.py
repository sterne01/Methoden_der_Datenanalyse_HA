import pandas as pd

# Alle Titel der einzelnen Worksheets als Variablen speichern, sodass alle einmal in den Korpus Transformer
# eingesetzt werden können:
f2010 = "Billboard2010_f - Billboard2010"
m2010 = "Billboard2010_m - Billboard2010"
fm2010 = "Billboard2010_fm - Billboard201"

f2020 = "Billboard2020_f - Billboard2020"
m2020 = "Billboard2020_m - Billboard2020"
fm2020 = "Billboard2020_fm - Billboard202"

# Dateipfade als Variablen speichern
x_path = "/Users/estern/Documents/Korpus_MeDa/Billboard2010_Geschlechteraufgeteilt.xlsx"
x_path2 = "/Users/estern/Documents/Korpus_MeDa/Billboard2020_Geschlechteraufgeteilt.xlsx"

# Kombinationen der Variablen in folgenden Code einsetzen:
x_file = pd.read_excel(x_path2, m2020)
print(x_file)

# aus dem Worksheet die Spalte mit den Songtexten ohne Überschriften oder Zusatzinformation anzeigen lassen (bei diesen Dateien
# von der 3. Position bis zur vorletzten)
print(x_file["Billboard2020_Tabelle Pivot"][3:(len(x_file)-1)])

x = x_file["Billboard2020_Tabelle Pivot"][3:(len(x_file)-1)]

# über die enthaltenen Songtexte iterieren und pro Reihe (also für jeweils ein Lied) eine .txt Datei erstellen
i = 0
for l in x:
    with open(f'{i}'+'.txt', 'x') as f:
        f.write(l)
        i += 1

# im Anschluss die einzelnen .txt Dateien eines Geschlechts jeweils einem Ordner hinzufügen