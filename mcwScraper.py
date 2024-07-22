from urllib.request import urlretrieve, Request, urlopen, FancyURLopener

class AppURLopener(FancyURLopener):
    version = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

opener = AppURLopener()

#urllib._urlopener.retrieve("http://www.foo.com/foo.jpg", "C:\\bar\\bar.jpg")

#urls = [
#	"https://www.ign.com/wikis/minecraft/Beginner%27s_Guide_-_Basics_and_Features",
#	"https://www.ign.com/wikis/minecraft/Survival_Guide:_Things_to_Do_First_in_Minecraft",
#	"https://minecraft.fandom.com/wiki/Mob",
#]

urlCounter = 3

#for url in urls:
#	urlCounter = urlCounter + 1
#	filename = str(urlCounter) + ".html"
#	urlretrieve(url, filename)
#	print ("file #{} COMPLETE!",urlCounter)

urlsThat403 = [
	"https://minecraft.wiki/w/Minecraft",
	"https://www.minecraftcrafting.info/"
]

#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}

for url in urlsThat403:
	urlCounter = urlCounter + 1
	filename = str(urlCounter) + ".html"
#	req = Request(url, headers=headers)
#	page = urlopen(req).read()

	file = open(filename,"w")
#	print(page, file=file)

	opener.retrieve(url, file)

	print ("file #{} COMPLETE!",urlCounter)

