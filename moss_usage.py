import moss_py

userid = 987654321

m = moss_py.Moss(userid, "python")

#m.addBaseFile("submission/a01.py")
#m.addBaseFile("submission/test_student.py")

# Submission Files
m.addFile("submission/a01-sample.py")

m.addFilesByWildcard("submission/a01-*.py")

url = m.send()

m.saveWebPage(url, "submission/report.html")