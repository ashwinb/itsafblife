from feed.rss import *

xmldoc, channel = new_xmldoc_channel()


set_indent_str("  ")

lst_errors = []

channel.import_xml("rss2sample.xml", lst_errors)

if len(lst_errors) == 0:
    print "Import result: No errors!\n"
else:
    print "Import result: Errors:\n" + "\n".join(lst_errors) + "\n"

print "And here is some info from the channel:"

print "    title:", channel.title.text
print "    description:", channel.description.text
print "    item 0 title:", channel.items[0].title.text
print "    item 3 title:", channel.items[3].title.text

title = Title()
title.import_xml("""<title keanu="Whoa">This is the second item</title>""")

channel.items[1].title = title
print "    item 1 title:", channel.items[1].title.text
print channel.items[1]
