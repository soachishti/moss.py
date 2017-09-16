import os
import socket
import glob

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
    userid = None
    options = {
        "l": "c",
        "m": 10,
        "d": 0,
        "x": 0,
        "c": "",
        "n": 250
    }
    basefiles = []
    files = []

    def __init__(self, userid, language = "c"):
        self.userid = userid

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

    def addBaseFile(self, file):
        self.basefiles.append(file)

    def addFile(self, file):
        if os.path.isfile(file):
            self.files.append(file)
        else:
            raise Exception("addFile({}) => File Not Found".format(file))

    def addFilesByWildcard(self, wildcard):
        for file in glob.glob(wildcard):
            self.files.append(file)

    def getLanguages(self):
        return languages

    def uploadFile(self, s, file, id):
        size = os.path.getsize(file)
        filename_fixed = os.path.basename(file).replace(" ", "_")
        message = "file {0} {1} {2} {3}\n".format(
            id,
            self.options['l'],
            size,
            filename_fixed
        )
        s.send(message.encode())
        content = open(file,"rb").read(size)
        s.send(content)

    def send(self):
        s = socket.socket() 
        s.connect((self.server, self.port))

        s.send("moss {}\n".format(self.userid).encode())
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

        for file in self.basefiles:
            self.uploadFile(s, file, 0)

        index = 1
        for file in self.files:
            self.uploadFile(s, file, index)

        s.send("query 0 {}\n".format(self.options['c']).encode())

        response = s.recv(1024)

        s.send(b"end\n")
        s.close()

        return response.decode().replace("\n","")

    def saveWebPage(self, url, path):
        response = urlopen(url)
        content = response.read()

        f = open(path, 'w')
        f.write(content.decode())
        f.close
