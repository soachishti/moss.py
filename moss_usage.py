from moss import moss

m = moss.Moss("userid", "python")

m.addBaseFile("a01.py")
m.addBaseFile("a01_other_file.py")

# Submission Files
m.addFile("submission/abc.py")

m.addFilesByWildcard("submission/a01-p17*.py")

m.send()
