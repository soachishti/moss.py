import os
import socket
import glob
import logging

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

class Moss:
    languages = (
        "c",
        "cc",
        "java",
        "ml",
        "pascal",
        "ada",
        "lisp",
        "scheme",
        "haskell",
        "fortran",
        "ascii",
        "vhdl",
        "perl",
        "matlab",
        "python",
        "mips",
        "prolog",
        "spice",
        "vb",
        "csharp",
        "modula2",
        "a8086",
        "javascript",
        "plsql")
    server = 'moss.stanford.edu'
    port = 7690

    def __init__(self, user_id, language="c"):
        self.user_id = user_id
        self.options = {
            "l": "c",
            "m": 10,
            "d": 0,
            "x": 0,
            "c": "",
            "n": 250
        }
        self.base_files = []
        self.files = []

        if language in self.languages:
            self.options["l"] = language

    def setIgnoreLimit(self, limit):
        self.options['m'] = limit

    def setCommentString(self, comment):
        self.options['c'] = comment

    def setNumberOfMatchingFiles(self, n):
        if n > 1:
            self.options['n'] = n

    def setDirectoryMode(self, mode):
        self.options['d'] = mode

    def setExperimentalServer(self, opt):
        self.options['x'] = opt

    def addBaseFile(self, file_path, display_name=None):
        if os.path.isfile(file_path):
            self.base_files.append((file_path, display_name))
        else:
            raise Exception("addBaseFile({}) => File Not Found".format(file_path))

    def addFile(self, file_path, display_name=None):
        if os.path.isfile(file_path):
            self.files.append((file_path, display_name))
        else:
            raise Exception("addFile({}) => File Not Found".format(file_path))

    def addFilesByWildcard(self, wildcard):
        for file in glob.glob(wildcard):
            self.files.append((file, None))

    def getLanguages(self):
        return self.languages

    def uploadFile(self, s, file_path, display_name, file_id):
        if display_name is None:
            # If no display name added by user, default to file path
            display_name = file_path.replace(" ", "_")

        size = os.path.getsize(file_path)
        message = "file {0} {1} {2} {3}\n".format(
            file_id,
            self.options['l'],
            size,
            display_name
        )
        s.send(message.encode())
        content = open(file_path, "rb").read(size)
        s.send(content)

    def send(self):
        s = socket.socket() 
        s.connect((self.server, self.port))

        s.send("moss {}\n".format(self.user_id).encode())
        s.send("directory {}\n".format(self.options['d']).encode())
        s.send("X {}\n".format(self.options['x']).encode())
        s.send("maxmatches {}\n".format(self.options['m']).encode())
        s.send("show {}\n".format(self.options['n']).encode())

        s.send("language {}\n".format(self.options['l']).encode())
        recv = s.recv(1024)
        if recv == "no":
            s.send(b"end\n")
            s.close()
            raise Exception("send() => Language not accepted by server")

        for file_path, display_name in self.base_files:
            self.uploadFile(s, file_path, display_name, 0)

        index = 1
        for file_path, display_name in self.files:
            self.uploadFile(s, file_path, display_name, index)
            index += 1

        s.send("query 0 {}\n".format(self.options['c']).encode())

        response = s.recv(1024)

        s.send(b"end\n")
        s.close()

        return response.decode().replace("\n","")

    def saveWebPage(self, url, path):
        if len(url) == 0:
            raise Exception("Empty url supplied")

        response = urlopen(url)
        content = response.read()

        f = open(path, 'w')
        f.write(content.decode())
        f.close()