To install:
python setup.py install

For more information on Python distutils install:
http://docs.python.org/inst/



This is the README.txt file that comes with the "PyFeed" family of
Python library modules.  These modules are useful for making syndication
feeds.

I have released these modules under the BSD license.  Please see the
comments at the beginning of each source file for the full text of the
license.

I would like to donate these modules to the Python Software Foundation.
(Of course it's up to the PSF to decide whether they want them or not.)


Here is a list of the modules, with notes on each.


xe

xe (short for "XML elements") is a Python library module that defines
classes to work with XML elements in a Pythonic way.  PyFeed depends
heavily on xe; you must have xe installed to use PyFeed.  xe is packaged
separately and has its own installer.



feed.date.tools

This is a Python library module that defines some utility functions for
working with Python time float values.



feed.date.rfc3339

This is a Python library module with functions for converting timestamp
strings in RFC 3339 format to Python time float values, and vice versa.
RFC 3339 is the timestamp format used by the Atom feed syndication
format.



feed.date.rfc822

This is a Python library module with functions for converting timestamp
strings in extended RFC 822 format to Python time float values, and vice
versa.  "Extended RFC 822" means the flavor of RFC 822 that is supported
by RSS 2.0; the key extension is that years can be four digits (and this
module defaults to writing four-digit years).



feed.atom

This is a Python library module designed to make it very easy to
work with an Atom syndication feed.

http://atomenabled.org/developers/syndication/

feed.atom is built on top of xe.  It automatically manages the XML tree
structure for you; you can just focus on the content you want to
syndicate and let the module take care of the formatting.

Take a look at the test cases at the end of the module, for example code
showing how to set up an Atom feed with an entry.  Also, here are a few
short examples:

To create an XML document with a feed in it, you do this:

xmldoc = XMLDoc()
feed = Feed()
xmldoc.root_element = feed


The above lines are so common I added a convenience function to make
them into a one-liner:

xmldoc, feed = new_xmldoc_feed()


To assign an entry to a feed, you just do this:

entry = Entry()
# set up entry by assigning to its properties
feed.entries.append(entry)

This adds "entry" to the internal list that keeps track of entries.
"entry" is now nested inside "feed", which is nested inside "xmldoc".

When you want to save the XML in a file, you can just do this:

f = open("file.xml", "w")
s = str(xmldoc)
f.write(s)
f.write("\n")  # write() doesn't add a newline on its own



feed.rss

This is a Python library module designed to make it very easy to
work with an RSS 2.0 syndication feed.

http://blogs.law.harvard.edu/tech/rss

feed.rss is built on top of xe.  It automatically manages the XML tree
structure for you; you can just focus on the content you want to
syndicate and let the module take care of the formatting.

Take a look at the test cases at the end of the module, for example code
showing how to set up an RSS feed with an item.  Also, here are a few
short examples:

To create an XML document with a feed in it, you do this:

xmldoc = XMLDoc()
xmldoc.root_element = RSS()

channel = Channel()
xmldoc.root_element.channel = channel


The above lines are so common I added a convenience function to make
them into a one-liner:

xmldoc, channel = new_xmldoc_channel()


To assign an item to a channel, you just do this:

item = Item()
# set up item by assigning to its properties
channel.items.append(item)

This adds "item" to the internal list that keeps track of items.
"item" is now nested inside "channel", which is nested inside "xmldoc".

When you want to save the XML in a file, you can just do this:

f = open("file.xml", "w")
s = str(xmldoc)
f.write(s)
f.write("\n")  # write() doesn't add a newline on its own



feed.opml1 / feed.opml

These are Python library modules designed to make it very easy to work
with OPML data.  opml1.py creates OPML 1.0 XML data; opml.py is intended
to create the latest version of OPML (currently, 2.0).

See the examples with feed.atom and feed.rss, above, to get an idea
how to use these.  As with those, there is a convenience function for
the common case of:

xmldoc, opml = new_xmldoc_opml()



feed.tools

This is a Python library module that defines some utility functions that
are handy when you are generating a syndication feed.  These functions
are not specific to any particular syndication format.



If you have any questions, comments, or bug reports about any of these
modules, please contact me using this email address:

pyfeed@langri.com



I hope you will find these modules useful!

Steve R. Hastings
steve@hastings.org
