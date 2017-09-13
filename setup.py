from setuptools import setup

try:
  import pypandoc
  long_description = pypandoc.convert('README.md', 'rst')
  long_description = long_description.replace("\r","")  
except(IOError, ImportError):
  long_description = open('README.md').read()

setup(
  name = 'moss.py',
  packages = ['moss'], # this must be the same as the name above
  version = '1.0.1',
  description = 'A Python client for Moss: A System for Detecting Software Similarity',
  long_description=long_description,
  author = 'soachishti',
  author_email = 'soachishti@outlook.com',
  url = 'https://github.com/soachishti/moss.py', # use the URL to the github repo
  download_url = 'https://github.com/soachishti/moss.py/archive/v1.0.0.tar.gz', # I'll explain this in a second
  keywords = ['moss', 'similarity', 'detecting', 'plagiarism'], # arbitrary keywords
  classifiers = [],
)