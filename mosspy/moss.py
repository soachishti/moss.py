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
        "verilog",
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
        if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
            self.base_files.append((file_path, display_name))
        else:
            raise Exception("addBaseFile({}) => File not found or is empty.".format(file_path))

    def addFile(self, file_path, display_name=None):
        if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
            self.files.append((file_path, display_name))
        else:
            raise Exception("addFile({}) => File not found or is empty.".format(file_path))

    def addFilesByWildcard(self, wildcard):
        for file in glob.glob(wildcard, recursive=True):
            self.files.append((file, None))

    def getLanguages(self):
        return self.languages

    def uploadFile(self, s, file_path, display_name, file_id, on_send):
        if display_name is None:
            # If no display name added by user, default to file path
            # Display name cannot accept \, replacing it with /
            display_name = file_path.replace(" ", "_").replace("\\", "/")

        size = os.path.getsize(file_path)
        message = "file {0} {1} {2} {3}\n".format(
            file_id,
            self.options['l'],
            size,
            display_name
        )
        s.send(message.encode())
        with open(file_path, "rb") as f:
            s.send(f.read(size))
        on_send(file_path, display_name)

    def send(self, on_send=lambda file_path, display_name: None):
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
            self.uploadFile(s, file_path, display_name, 0, on_send)

        index = 1
        for file_path, display_name in self.files:
            self.uploadFile(s, file_path, display_name, index, on_send)
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
        charset = response.headers.get_content_charset()
        content = response.read().decode(charset)

        f = open(path, 'w', encoding='utf-8')
        f.write(content)
        f.close()
