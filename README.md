# SATIN

SATIN stands for the `Set of Audio Tags and Identifiers Normalized` and was proposed in [this article](https://www.researchgate.net/project/Toward-better-playlists-from-bigger-musical-databases-use-case-in-singing-voice-detection-at-track-scale).
SATIN is a Music Information Retrieval (MIR) database for reproducible research.
SATIN is shipped along SOFT1, the first Set Of FeaTures extracted by musical pieces referenced by SATIN.

## Aim of SATIN

- Guarantee long-term reproducible research in MIR
- Enable precise identification and reuse of musical pieces
- Foster research in multiple MIR tasks such as Cover Song Identification and Singer Gender Classification.

## Description of SATIN

SATIN is a csv file containing on each line:
- the [ISRC](http://isrc.ifpi.org/en) of the musical pieces as given by the [IFPI](http://www.ifpi.org/)
- the genre tag provided by [Musixmatch](https://www.musixmatch.com/fr) and [Simbals](http://www.simbals.com)

## Description of SOFT1

### Softwares used to extract audio features of the files referenced in SATIN:

- [YAAFE](https://github.com/Yaafe/Yaafe)
- [Marsyas](http://marsyas.info/)
- [Essentia](https://github.com/MTG/essentia/)

We plan to add:
- [Vamp](http://www.vamp-plugins.org)
- [harmony-analyser](http://www.harmony-analyser.org)

### Commands used for extracting features
- [YAAFE](https://github.com/Yaafe/Yaafe): `yaafe -r 22050 -f "mfcc: MFCC blockSize=2048 stepSize=1024" --resample -b  output_dir_features input_filename`
- [Essentia](https://github.com/MTG/essentia/): `essentia-extractors-v2.1_beta2/streaming_extractor_music input_filename output_filename`
- [bextract](http://marsyas.info/doc/manual/marsyas-user/bextract.html#bextract): `bextract -mfcc -zcrs -ctd -rlf -flx -ws 1024 -as 898 -sv -fe`

The commands that we will use for extracting new features are:
- [Vamp](http://www.vamp-plugins.org) extracted via [harmony-analyser](http://www.harmony-analyser.org) using JNI wrapper:
    - `java -jar ha-script.jar -a nnls-chroma:nnls-chroma -s .wav -t 0.07`
    - `java -jar ha-script.jar -a nnls-chroma:chordino-tones -s .wav -t 0.07`
    - `java -jar ha-script.jar -a nnls-chroma:chordino-labels -s .wav -t 0.07`
    - `java -jar ha-script.jar -a qm-vamp-plugins:qm-keydetector -s _wav -t 0.07`
- [harmony-analyser](http://www.harmony-analyser.org) with the following commands (note that Vamp plugin analysis was first performed to extract low-level features):
    - `java -jar ha-script.jar -a chord_analyser:chord_complexity_distance -s .wav -t 0.07`
    - `java -jar ha-script.jar -a chroma_analyser:complexity_difference -s .wav -t 0.07`
    - `java -jar ha-script.jar -a chord_analyser:average_chord_complexity_distance -s .wav -t 0.07`
    - `java -jar ha-script.jar -a chord_analyser:tps_distance -s .wav -t 0.07`
    - `java -jar ha-script.jar -a filters:chord_vectors -s .wav -t 0.07`
    - `java -jar ha-script.jar -a filters:key_vectors -s .wav -t 0.07`

If you would like to see more features, please contact us.
As the features in SOFT1 are too large to be shared on a GitHub repository, please [click here](http://yannbayle.fr/english/index.php) to download them.

## Installation & Getting started

You can either in your linux terminal `pip install bayle` and 
```
from bayle import satin
satin.main()
```

or you can fork the repo and `python satin.py`

## Requirements/Dependencies

- [Python 3](https://www.python.org/download/releases/3.0/)
- [Cartopy](https://github.com/SciTools/cartopy)
- [word_cloud](https://github.com/amueller/word_cloud)

## Contributing

Any sort of participation is encouraged.
We will closely analyze each fork, pull request and consider new contributors.
Please contact us if you use this database, we would love to know what you used it for!
We hope that SATIN and SOFT1, in their current state, will be helpful in your research and we will continue to improve them, so stay tuned!

## Documentation

In progress.

## License

- If you use SATIN and/or SOFT1, please [cite us accordingly](https://github.com/ybayle/SATIN/blob/master/citation.bib) (our related research paper can be found [here](https://www.researchgate.net/project/Toward-better-playlists-from-bigger-musical-databases-use-case-in-singing-voice-detection-at-track-scale)).
- We are grateful to [Musixmatch](https://www.musixmatch.com/fr), [Deezer](http://www.deezer.com) and [Simbals](http://www.simbals.com) who made this study possible.
- SATIN, SOFT1 and the code in this repository is licensed under the terms of the [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png"/>

## Contact
For more information please contact bayle.yann@live.fr or visit [yannbayle.fr](http://yannbayle.fr/english/index.php)
