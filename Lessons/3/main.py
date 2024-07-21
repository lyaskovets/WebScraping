import re
import xml.etree.ElementTree as ET
from lxml import etree

text = """Welcome to the Regex Training Center! Let's start with some dates:
01/02/2021, 12-25-2020, 2021.03.15, 2022/04/30, 2023.06.20, 12 12 2012 and 2021.07.04. You can
also find dates with words: March 14, 2022, and December 25, 2020.

Now let's move on to some phone numbers:
(123) 456-7890, +1-800-555-1234, 800.555.1234, 800-555-1234, and 123.456.7890.
Other formats include international numbers: +44 20 7946 0958, +91 98765 43210.

Here are some email addresses to find:
[john.doe@example.com](mailto:john.doe@example.com), [jane_doe123@domain.org](mailto:jane_doe123@domain.org), [support@service.net](mailto:support@service.net), [info@company.co.uk](mailto:info@company.co.uk),
and [contact.us@my-website.com](mailto:contact.us@my-website.com). You might also find these tricky: [weird.address+spam@gmail.com](mailto:weird.address+spam@gmail.com),
"quotes.included@funny.domain", and [this.one.with.periods@weird.co.in](mailto:this.one.with.periods@weird.co.in).

Need some URLs to extract? Try these:
[http://example.com](http://example.com/), [https://secure.website.org](https://secure.website.org/), [http://sub.domain.co](http://sub.domain.co/),
[www.redirect.com](http://www.redirect.com/), and [ftp://ftp.downloads.com](ftp://ftp.downloads.com/). Don't forget paths and parameters:
https://my.site.com/path/to/resource?param1=value1&param2=value2,
http://www.files.net/files.zip, https://example.co.in/api/v1/resource, and
https://another-site.org/downloads?query=search#anchor.

Hexadecimal numbers appear in various contexts:
0x1A3F, 0xBEEF, 0xDEADBEEF, 0x123456789ABCDEF, 0xA1B2C3, and 0x0. You might also find these:
#FF5733, #C70039, #900C3F, #581845, #DAF7A6, and #FFC300. RGB color codes can be tricky:
rgb(255, 99, 71), rgba(255, 99, 71, 0.7).

For those interested in Social Security numbers, here's some data:
123-45-6789, 987-65-4321, 111-22-3333, 555-66-7777, and 999-88-7777. Note that Social
Security numbers might also be written like 123 45 6789 or 123456789.

Let's throw in some random sentences for good measure:

- The quick brown fox jumps over the lazy dog.
- Lorem ipsum dolor sit amet, consectetur adipiscing elit.
- Jack and Jill went up the hill to fetch a pail of water.
- She sells seashells by the seashore.

Finally, let's include some special characters and numbers:
1234567890, !@#$%^&*()_+-=[]{}|;':",./<>?, 3.14159, 42, and -273.15.

That's it! I hope you find this useful for your regex training."""

xml = """<?xml version="1.0"?>
<data>
    <info number="1">
        <fact>When a cat drinks, its tongue - which has tiny barbs on it - scoops the liquid up backwards.</fact>
        <length>92</length>
    </info>
    <info number="2">
        <fact>Cats spend nearly 1\/3 of their waking hours cleaning themselves.</fact>
        <length>64</length>
    </info>
</data>"""


def parse_re():
    # pattern = r'(March|December)\D\d{1,2},\D(\d{4})'
    # dates = re.findall(pattern,text)
    # print(dates)

    pattern = r'rgba\((\d+,\s?\d+,\s?\d+),\s?([\d\.]+)\)'
    color = re.search(pattern, text).group(1)
    print('color is: ', color)
    prozorist = re.search(pattern, text).group(2)
    print('prozorist: ', prozorist)


def parsexpathxml():
    root = ET.fromstring(xml)
    facts = root.findall('.//fact')
    facts = [fact.text for fact in facts]
    # print(facts)

    facts = root.findall('.//info[@number="2"]/fact')
    facts = [fact.text for fact in facts]
    # print(facts)

    length = root.findall('.//info[2]/length')
    length = [length.text for length in length]
    print(length)


html = """<html>
    <head>
        <title>My page</title>
    </head>
    <body>
        <h2>Welcome to my <a href="#">page</a></h2>
        <p>This is the first paragraph</p>.
        <p>This is the second paragraph</p>.
        <!-- this is the end -->
    </body>
</html>"""


def parse_html_xpath():
    tree = etree.HTML(html)
    p = tree.xpath('//p[2]')
    p = [elementttt.text for elementttt in p]
    print(p)


if __name__ == '__main__':
    # parse_re()
    # parsexpathxml()
    parse_html_xpath()
