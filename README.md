# What is this project

It is a little crawler created with Scrapy (http://scrapy.org/)

It is used for some specific tasks:
- find invalid urls on pages
- detect and report invalid or undesired words on pages
- as a side effect, forces the caching of pages on a server (like WordPress sites using cache plugins)

# How to install

Install Scrapy and them download and run this script like the example below.

# How to run

Put one forbidden words per line in the file you use with -a forbidden_words_file="forb-words.txt". 
Some words that are interesting to detect in a PHP and MySQL base website.

###########################################
Parse error
Fatal error
PHP Warning
Missing argument
Error establishing a database connection
foreach
Invalid argument
###########################################

This a command line you can use:

scrapy crawl cpages -a start_url=http://www.example.com/ -a output_html_filename=/tmp/report-check-pages.html -a forbidden_words_file=/tmp/forb-words.txt
