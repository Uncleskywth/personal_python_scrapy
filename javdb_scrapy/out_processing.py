import re
f = open("searched_urls.txt","r")
contents = f.readlines()
clean_contents = []
for content in contents:
	clean_contents.append(re.match("(https.*)(\n)",content).group(1))
f.close()

