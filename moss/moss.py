import os
import socket
import glob


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

    def __init__(self, userid, language):
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
        s.send(
            "file {} {} {} {}\n".format(
                id,
                self.options['l'],
                size,
                file.replace(
                    " ",
                    "_")))
        s.send(open(filename).read(size))

    def send(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server, self.port))

            s.send("moss {}\n".format(self.userid))
            s.send("directory {}\n".format(self.options['d']))
            s.send("X {}\n".format(self.options['x']))
            s.send("maxmatches {}\n".format(self.options['m']))
            s.send("show {}\n".format(self.options['n']))

            s.send("language {}\n".format(self.options['l']))
            recv = s.recv(1024).trim()
            if recv == "no":
                s.send("end\n")
                s.close()
                raise Exception("send() => Language not accepted by server")

            for file in self.basefiles:
                self.uploadFile(s, file, 0)

            index = 1
            for file in self.files:
                self.uploadFile(s, file, index)

            s.send("query 0 {}\n".format(self.options['c']))

            response = s.recv(1024)

            s.send("end\n")
            s.close()

            return response
