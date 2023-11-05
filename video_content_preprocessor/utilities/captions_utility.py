import json

# Hier sind Ihre Transkript-Daten
transcripts = [
    # Ihre JSON-Daten hier einfügen
]

# Sortieren Sie die Transkripte nach Startzeit
transcripts.sort(key=lambda x: x["start"])


# Eine Funktion, um zu überprüfen, ob zwei Teile überlappen
def do_overlap(a, b):
    return a["start"] + a["duration"] > b["start"]


# Die Funktion, um zusammengehörige Transkripte zu vereinigen
def _merge_transcripts(transcripts):
    merged = []
    current = None

    for transcript in transcripts:
        if current is None:
            # Wenn es der erste Transkript ist
            current = transcript
        elif do_overlap(current, transcript):
            # Wenn der aktuelle Transkript mit dem nächsten überlappt
            combined_text = current["text"] + " " + transcript["text"].strip()
            current_end = current["start"] + current["duration"]
            overlap_end = transcript["start"] + transcript["duration"]
            current["duration"] = max(current_end, overlap_end) - current["start"]
            current["text"] = combined_text
        else:
            # Keine Überlappung; Füge den aktuellen zur Liste hinzu und setze mit dem nächsten fort
            merged.append(current)
            current = transcript

    # Vergiss nicht, das letzte Element hinzuzufügen
    if current is not None:
        merged.append(current)

    return merged


# Die Transkripte zusammenführen
merged_transcripts = _merge_transcripts(transcripts)

# Das Ergebnis in JSON umwandeln
merged_json = json.dumps(merged_transcripts, indent=4)
print(merged_json)
