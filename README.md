# conll-viewer
Turning coNLL 2009 formatted files to a visual format, with support for files resulting from [open-sesame](https://github.com/swabhs/open-sesame)
Currently, the only format supported is the one that been through argument identification stage of open-sesame.

---
### Installation
Conll-viewer can be installed from PyPi using PIP
```sh
$ pip install conllviewer
```
----
### Examples

```python
import conllviewer
file=conllviewer.reader("predicted-args.conll")
sentences=file.get_sentences()
im=sentences[0].draw()
im.save("sentence.png")
```