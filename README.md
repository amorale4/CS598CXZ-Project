CS598CXZ-Project
================

This project has several dependencies. You need to install flask, as well as pyLucene.

First you need to generate a file-corpus of the data this is done by running the python file file-corpus.py. The data input are the datafiles from the Amazon SNAP dataset.

Once you have generated the data now we need to index the files. We do this by running the IndexFiles.py file. providing the local path to the file-corpus and an output path where you want the index to be saved.

Finally we can use the run.py to run our program.
