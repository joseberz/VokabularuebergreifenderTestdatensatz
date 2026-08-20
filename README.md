## Vokabularübergreifender Testdatensatz

### Funktion

Dieser Datensatz dient dem Testen des Vocabulary-Retrieval-Mechanismus auf unbekannten Klassen. Er enthält für ausgewählte Bilder aus drei Datensätzen zusätzliche Klassenannotationen, die im jeweiligen Originaldatensatz nicht vorkommen. Damit soll sich untersuchen lassen, wie das Verfahren reagiert, wenn im Eingabebild Objekte sichtbar sind, deren Klassen außerhalb des ursprünglich bekannten Klassenvokabulars liegen.

Die neuen Klassen basieren auf einer Teilmenge von Bildern aus:

- **PASCAL-Context 59 (PC59)**
- **IDD (India Driving Dataset)**
- **NYU Depth Dataset V2 (NYU)**

### Ordnerstruktur

**Hinweis:** Die `image/`-Ordner enthalten in diesem Repository keine Originalbilder (siehe Abschnitt "Lizenzhinweis"). Dort liegt pro Klasse eine `filelist.txt` mit den Namen der benötigten Original-Bilddateien.

```
PC59_novel/
  image/
    <Klasse_1>/
      filelist.txt   -> namen der bilder die man braucht
    <Klasse_2>/
      filelist.txt
    ...
  new_masks/
    <Klasse_1>/
    <Klasse_2>/
    ...
  pc59_novel.json

IDD_novel/
  image/
    <Klassenordner>/
      filelist.txt
  new_masks/
    <Klassenordner>/
  idd30_novel.json

NYU_novel/
  image/
    <Klassenordner>/
      filelist.txt
  new_masks/
    <Klassenordner>/
  nyu40.json
```

Für jeden der drei Datensätze (`PC59_novel`, `IDD_novel`, `NYU_novel`) gilt derselbe Aufbau:

- **`image/<Klassenordner>/filelist.txt`**: listet die Namen der Original-Bilder auf, auf denen die neue Klasse annotiert wurde. Jeder Unterordner entspricht einer neuen Klasse. Die Bilddateien selbst sind nicht enthalten (siehe Abschnitt "Originalbilder beschaffen").
- **`new_masks/<Klassenordner>`**: enthält die zugehörigen Segmentierungsmasken für die Klasse, mit identischem Dateinamen wie das zugehörige Bild in `filelist.txt`.
- **JSON-Dateien** (eine je Datensatz): enthalten alle für diesen Datensatz annotierten Masken-IDs. Die IDs im JSON-Array entsprechen den Pixelwerten in den Masken.

### Originalbilder beschaffen

Da die Originalbilder aus Lizenzgründen nicht mitgeliefert werden (siehe unten), müssen sie vor der Nutzung selbst besorgt werden:

1. **PC59 (PASCAL-Context)**: Bilder über die offizielle PASCAL-VOC-2010-/PASCAL-Context-Distribution beziehen.
2. **IDD**: Account unter [idd.insaan.iiit.ac.in](https://idd.insaan.iiit.ac.in/) registrieren, Lizenzbedingungen akzeptieren, Segmentation-Dataset herunterladen.
3. **NYU Depth V2**: Bilder über die offizielle Projektseite ([cs.nyu.edu/~silberman/datasets/nyu_depth_v2.html](https://cs.nyu.edu/~silberman/datasets/nyu_depth_v2.html)) beziehen.

Der Ablagepfad der Originalbilder sollte der von detectron2 festgelegte Datensatz-Ordner sein.

### Originalbilder ins Repository kopieren

Mit dem Skript `fetch_images.py` (im Wurzelverzeichnis dieses Repos) lassen sich die zuvor beschafften Originalbilder automatisch in die passenden `image/<Klasse>/`-Ordner kopieren. Es sucht anhand der `filelist.txt`-Dateien nach den Bildern.
Es muss aus dem Wurzelverzeichnis des Repos heraus aufgerufen werden:

```bash
python3 fetch_images.py \
  --pc59 /pfad/zu/pascal-context/JPEGImages \
  --idd /pfad/zu/idd \
  --nyu /pfad/zu/nyu
```

Es müssen nicht alle drei Optionen angegeben werden. Es genügen die Pfade für die Datensätze, für die bereits Originalbilder vorliegen.

### Quellen der Originaldatensätze

Die Basisbilder und die zugrundeliegende Datensatzstruktur stammen aus diesen Originaldatensätzen:

- Mottaghi, R., Chen, X., Liu, X., Cho, N.-G., Lee, S.-W., Fidler, S., Urtasun, R., & Yuille, A. (2014). *The Role of Context for Object Recognition and Segmentation in the Wild*. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR).
- Varma, G., Subramanian, A., Namboodiri, A., Chandraker, M., & Jawahar, C. V. (2019). *IDD: A Dataset for Exploring Problems of Autonomous Navigation in Unconstrained Environments*. In IEEE Winter Conference on Applications of Computer Vision (WACV).
- Silberman, N., Hoiem, D., Kohli, P., & Fergus, R. (2012). *Indoor Segmentation and Support Inference from RGBD Images*. In European Conference on Computer Vision (ECCV).

Die neuen Klassenannotationen sind eigenständige Ergänzungen zu diesen Originaldatensätzen und nicht Teil der offiziellen Annotationen.

### Lizenzhinweis

Die Originalbilder werden in diesem Repository nicht mitgeliefert. Für alle drei Quelldatensätze gelten die Lizenz-/Nutzungsbedingungen der jeweiligen Anbieter. Die IDD-Lizenz schließt bspw. eine Weitergabe der Originalbilkder explizit aus.

- `image/`-Ordner enthalten nur `filelist.txt` statt der Originalbilder.
- `new_masks/` und die JSON-Dateien werden veröffentlicht.
- Nutzung ausschließlich nicht-kommerziell (Forschung).