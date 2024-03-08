import little_mallet_wrapper as m
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE

# Pfade als Variablen speichern
path_mallet = "/Applications/mallet-2.0.8/bin/mallet"
path_output = "/Users/estern/Documents/Korpus_MeDa"
path_training_data = "/Users/estern/Documents/Korpus_MeDa/Billboard2010_Geschlechteraufgeteilt.xlsx"

# Als Trainingsdaten alle Songtexte des Jahres 2020 verwenden
train = pd.read_excel(path_training_data, sheet_name="Blatt 1 - Billboard2010_Tabelle", header=1)
print(train["Songtext"])
Geschlecht = train["Geschlecht"]

# Die Dokument IDs der Geschlechter in Listen speichern
f_IDs = list(Geschlecht[Geschlecht == "f"].index)
m_IDs = list(Geschlecht[Geschlecht == "m"].index)

# Die IDs mit zugehörigem "f" und "m" in einem Dictionary speichern
docs_f_m = {"f": f_IDs, "m": m_IDs}

# Die Songtexte als strings in einer Liste speichern, dafür Liste "stringslist" erstellen
stringslist = []

# Songtexte "f/m" ausschließen für Trainingsdaten, sonstige Songtexte zu "stringslist" hinzufügen (zuerst alle "f", dann "m")
for x in docs_f_m.get("f"):
    stringslist.append(train["Songtext"][x])

for x in docs_f_m.get("m"):
    stringslist.append(train["Songtext"][x])

# Grundsätzliche Informationen zur Liste der Strings anzeigen, z.B. Anzahl der Dokumente, Wörter pro Dokument etc.
m.print_dataset_stats(stringslist)

# Stoppwörter festlegen (aus AntConc Frequenzlisten und Probedurchläufen des Topic Modelling erstellt)
sw = ["eh", "ooh", "na", "doo", "la", "the", "it", "oh", "chorus", "verse", "intro", "eh", "yeah", "and", "NUM"]

# Die Songtexte in der "stringslist" für den Trainingsprozess vorbereiten (Stoppwörter entfernen, alles in Kleinbuchstaben umwandeln, etc.)
training_data = [m.process_string(t, lowercase=True, remove_short_words=False, remove_stop_words=True, stop_words=sw)
                 for t in stringslist]
training_data = [d for d in training_data if d.strip()]

# Anfang der Trainingsdaten anzeigen
print(training_data[0])

# Noch einmal Informationen zum Datenset anzeigen lassen.
# Durch das Entfernen der Stoppwörter ist die Wortzahl kleiner.
m.print_dataset_stats(training_data)

# Ein Topic Model auf die Songtexte trainieren
topic_keys, topic_distributions = m.quick_train_topic_model(path_to_mallet=path_mallet,
                                                            output_directory_path=path_output, num_topics=10,
                                                            training_data=training_data)

# Pfade zu Mallet Files (Topic Keys, Topic Distribution, Word Weights)
tk = "/Users/estern/Documents/Korpus_MeDa/mallet.topic_keys.10"
td = "/Users/estern/Documents/Korpus_MeDa/mallet.topic_distributions.10"
ww = "/Users/estern/Documents/Korpus_MeDa/mallet.word_weights.10"

print("Training IDs:")
tid = m.load_training_ids(td)

# Dokument IDs, Dominantes Topic des Dokuments und Wahrscheinlichkeit zu einer Liste hinzufügen
t =[]
for ID, topic in zip(tid, topic_distributions):
    maxt = max(topic)
    t.append((topic_distributions.index(topic), topic.index(maxt), max(topic)))

# Geschlecht als Liste, erste Dokumente "f", Rest "m"
ge = []
ge += "f"*len(f_IDs)
ge += "m"*(len(training_data)-(len(f_IDs)))

# DataFrame mit Spalten Document ID, Dominant Topic ID, Probability und Geschlecht erstellen (aus "t" und "ge")
arr = pd.DataFrame(t, columns=["Document ID", "Dominant Topic ID", "Probability"])
arr["Geschlecht"] = ge
print(arr)

# Topic Distributions laden
topic_weights = m.load_topic_distributions(td)

# Dataframe der Topic Weights/Distributions
df = pd.DataFrame(topic_weights)

# Dominantes Topic in jedem Dokument
topic_num = np.argmax(df, axis=1)

# tSNE Dimension Reduction
tsne_model = TSNE(n_components=2, verbose=0, random_state=0, angle=0.5)
tsne_lda = tsne_model.fit_transform(df)

# Topic Cluster mit einem Scatterplot darstellen und die Geschlechter in zwei verschiedenen Farben anzeigen lassen (hue=ge)
sns.scatterplot(tsne_model, x=tsne_lda[:,0], y=tsne_lda[:,1], hue=ge)
plt.show()

# Subset des Dataframes erstellen nur mit Dominant Topic ID und Geschlecht, um zu sehen, welche Topics bei welchem Geschlecht auftreten
arr_ds = arr[["Dominant Topic ID", "Geschlecht"]]
arr_ds = arr_ds.sort_values(by="Dominant Topic ID")

# Häufigstes Topic für Geschlechter herausfinden
print(arr_ds.where(arr_ds["Geschlecht"] == "f").dropna())
print(arr_ds.where(arr_ds["Geschlecht"] == "f").dropna().mode())
print(arr_ds.where(arr_ds["Geschlecht"] == "m").dropna().mode())


# Topic Keys (Wörter eines Topic) und deren Wahrscheinlichkeit:
topic_tw = m.load_topic_word_distributions(ww)
for _topic, _word_probability_dict in topic_tw.items():
    print('Topic', _topic)
    for _word, _probability in sorted(_word_probability_dict.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(round(_probability, 4), '\t', _word)
    print()