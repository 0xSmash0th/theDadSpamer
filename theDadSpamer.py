'''
Created on Aug 18, 2016

@author: smashoth and rando stackOverflow contributers
'''
import feedparser
import smtplib
import random
from HTMLParser import HTMLParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
    
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

if __name__ == '__main__':
    rss = feedparser.parse('https://www.google.com/alerts/feeds/yourFeedGoesHere')
    random.seed()
    luckyArticleNum = random.randint(0, len(rss.entries)-1)
    
    # me == my email address used to log into your account, so yes they will know its from you...
    # you == recipient's email address 
    me = "###@gmail.com"
    you = "###@gmail.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = strip_tags(rss.entries[luckyArticleNum].title)
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "use the awesome html version!"
    #"Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
    html =  """\
    <html>
      <head></head>
      <body>
        <p>""" + strip_tags(rss.entries[luckyArticleNum].description) + """<br>
           <br>
           Here is the <a href=""" + rss.entries[luckyArticleNum].link + """>link</a>.
        </p>
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.login("yourEmailUsername", "emailPword")
    s.sendmail(me, you, msg.as_string())
    s.quit()
