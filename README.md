Man kann die App direkt als Python standalone ausführen, indem man im Terminal im entsprechenden Ordner einfach den Command

python ./zeitraum.py

oder

python3 ./zeitraum.py

ausführt.
Die fertig kompilierte .app die sowohl auf Intel, als auch auf Apple Silicon Macs läuft, ist im Unterordner "dist" zu finden.
Eventuell besteht das Problem, dass der Gatekeeper den Fehler bringt, dass er nicht sicherstellen konnte, dass die App keinen Schaden anrichtet.

Um dies zu umgehen, einfach beim Ordner, in welchem die .app liegt

xattr -d com.apple.quarantine /.Nebenkosten\ Rechner.app

ausführen. (Oder wo auch immer die App bei euch liegt…)
Dadurch sollte sich die .app Problemlos öffnen lassen.


Das App-Icon kann ganz einfach angepasst werden, indem die icon.icns Datei, die in der .app verpackt ist, entsprechend überschrieben wird. Die voreingestellte .icns ist auch hier im Projekt-Root zu finden unter dem Namen "icon.icns".
