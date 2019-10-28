# must install mediawiki on command prompt
# pip instiall pymediawiki
from mediawiki import MediaWiki

wikipedia = MediaWiki()
wiki = wikipedia.page("Wikipedia")
print(wiki.title)
print(wiki.pageid)
