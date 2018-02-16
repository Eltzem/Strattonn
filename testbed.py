import csvreader
filename = open("ANG.csv","r")
test = csvreader.csvreader(filename)
print(test)
print('[%s]' % "".join(map(str, test.aList)))


