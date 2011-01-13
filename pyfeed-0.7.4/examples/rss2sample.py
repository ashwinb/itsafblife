# rss2sample.py -- generate the rss2sample.xml file with rssfeed.py
#
# This will write a file called rss2sample.tmp, which should be
# identical to the included rss2sample.xml file.
#
# This example is taken from here:
# http://media-cyber.law.harvard.edu/blogs/gems/tech/rss2sample.xml
#
# The differences are only:
#     a) I changed the indenting from 3 spaces to 1 tab per indent.
#     b) I changed the order in which a few lines appear, to match what
#         rssfeed.py does by default.
#
# Steve R. Hastings
# pyfeed@langri.com



from feed.rss import *
from feed.tools import escape_html

set_default_time_offset("GMT")

xmldoc, channel = new_xmldoc_channel()

xmldoc.xml_decl.attrs["encoding"] = ""

channel.title = "Liftoff News"
channel.link = "http://liftoff.msfc.nasa.gov/"
channel.description = "Liftoff to Space Exploration."
channel.language = "en-us"
channel.pub_date = "Tue, 10 Jun 2003 04:00:00 GMT"
channel.last_build_date = "Tue, 10 Jun 2003 09:41:01 GMT"
channel.generator = "Weblog Editor 2.0"
channel.managing_editor = "editor@example.com"
channel.web_master = "webmaster@example.com"

item = Item()
s = """Sky watchers in Europe, Asia, and parts of Alaska and Canada will experience a <a href="http://science.nasa.gov/headlines/y2003/30may_solareclipse.htm">partial eclipse of the Sun</a> on Saturday, May 31st."""
item.description = escape_html(s)
item.pub_date = "Fri, 30 May 2003 11:06:42 GMT"
item.guid = "http://liftoff.msfc.nasa.gov/2003/05/30.html#item572"
channel.items.append(item)

item = Item()
item.title = "The Engine That Does More"
item.link = "http://liftoff.msfc.nasa.gov/news/2003/news-VASIMR.asp"
s = """Before man travels to Mars, NASA hopes to design new engines that will let us fly through the Solar System more quickly.  The proposed VASIMR engine would do that."""
item.description = escape_html(s)
item.pub_date = "Tue, 27 May 2003 08:37:32 GMT"
item.guid = "http://liftoff.msfc.nasa.gov/2003/05/27.html#item571"
channel.items.append(item)

item = Item()
item.title = "Astronauts' Dirty Laundry"
item.link = "http://liftoff.msfc.nasa.gov/news/2003/news-laundry.asp"
s = """Compared to earlier spacecraft, the International Space Station has many luxuries, but laundry facilities are not one of them.  Instead, astronauts have other options."""
item.description = escape_html(s)
item.pub_date = "Tue, 20 May 2003 08:56:02 GMT"
item.guid = "http://liftoff.msfc.nasa.gov/2003/05/20.html#item570"
channel.items.append(item)

item = Item()
item.title = "Star City"
item.link = "http://liftoff.msfc.nasa.gov/news/2003/news-starcity.asp"
s = """How do Americans get ready to work with Russians aboard the International Space Station? They take a crash course in culture, language and protocol at Russia's <a href="http://howe.iki.rssi.ru/GCTC/gctc_e.htm">Star City</a>."""
item.description = escape_html(s)
item.pub_date = "Tue, 03 Jun 2003 09:39:21 GMT"
item.guid = "http://liftoff.msfc.nasa.gov/2003/06/03.html#item573"
channel.items.insert(0, item)

f = open("rss2sample.tmp", "w")
s = str(xmldoc)
f.write(s)
f.write("\n")
f.close()
