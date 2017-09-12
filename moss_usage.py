from moss import moss

userid = int(open("userid.txt").read(80))

m = moss.Moss(userid, "python")

#m.addBaseFile("submission/a01.py")
#m.addBaseFile("submission/test_student.py")

# Submission Files
m.addFile("submission/a01-sample.py")

m.addFilesByWildcard("submission/a01-*.py")

url = m.send().decode().replace("\n","")

m.saveWebPage(url, "submission/report.html")
