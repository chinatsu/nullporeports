nullporeports
=============

gathering NullpoMino reports into one thing


## dependencies
* [Python 3](https://www.python.org/downloads/)
* [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/)
* [Jinja2](http://jinja.pocoo.org/)

If you installed pip with Python 3, you can do `pip install beautifulsoup4` and `pip install jinja2`.

## things to consider
* Change the `REPORTS_DIR` and `YOUR_NAME` variables in the script. 
* There are a few comments here and there, which may be useful for both me and you.
* There's no error handling so so, but given that you've set the right path to the directory with NullpoMino report html files, it should be fairly painless.
* I've not done much testing in Windows.
* The `res` folder in this repository is optional, it's just there for css in the output html. By default, the script will output a html file in the same directory as the script.
* Change stuff as you please!


## todo
* Graphs
* things
