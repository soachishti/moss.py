# moss.py

A Python client for [Moss](http://theory.stanford.edu/~aiken/moss/): A System for Detecting Software Similarity

## Introduction

It is a Python interface for [Moss](http://theory.stanford.edu/~aiken/moss/) client. It was written for [AutoGrader](https://github.com/BilalZaib/AutoGrader) for handling similarity in Python assignment submission. 

It was written using the [original bash script/documentation](http://moss.stanford.edu/general/scripts.html) and its [PHP](https://github.com/Phhere/MOSS-PHP) dialect.

### Installation
 
```shell
pip install mosspy
```

### Usage

```python
import mosspy

userid = 987654321

m = mosspy.Moss(userid, "python")

m.addBaseFile("submission/a01.py")
m.addBaseFile("submission/test_student.py")

# Submission Files
m.addFile("submission/a01-sample.py")
m.addFilesByWildcard("submission/a01-*.py")

# progress function optional, run on every file uploaded
# result is submission URL
url = m.send(lambda file_path, display_name: print('*', end='', flush=True))
print()

print ("Report Url: " + url)

# Save report file
m.saveWebPage(url, "submission/report.html")

# Download whole report locally including code diff links
mosspy.download_report(url, "submission/report/", connections=8, log_level=10, on_read=lambda url: print('*', end='', flush=True)) 
# log_level=logging.DEBUG (20 to disable)
# on_read function run for every downloaded file
```

## Python Compatibility

* [Python](http://www.python.com) - v3

## Similar Project

* [ocaml-moss](https://github.com/Chris00/ocaml-moss) OCaml client 
* [cl-moss](https://github.com/wsgac/cl-moss) Common Lisp
* [moji](https://github.com/nordicway/moji) Java version
* [MOSS-PHP](https://github.com/Phhere/MOSS-PHP) PHP version
* [GUI for Windows](https://onedrive.live.com/?cid=b418048abfa842a7&id=B418048ABFA842A7%2136714&ithint=folder,.txt&authkey=!ACqFMI0kmA4L1mc) GUI for Windows

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/soachishti/moss.py/blob/master/LICENSE) file for details
