Pokebot _(poh-kay-bot)_
=======================
A friend of mine asked me to write him a bot that would automatically poke back anyone who poked him on Facebook, so that's what I did.

This bot doesn't make use of any of the actual Facebook APIs, but instead performs all of its actions by mimicking the behavior of an actual web browser.  I designed it this way for three reasons.

1. I was bored and enjoy a challenge.
2. It takes me back to my days as a freelance spam bot developer.
3. Working with official APIs can be messy when you have to deal with getting access tokens, and the possibility of having your access revoked if your actions are deemed excessive.  So while it's not nearly as straight forward as working with the official API, mimicking a web browser does have its perks.

Requirements
------------

* Python 2.7 - [http://python.org](http://python.org)
* Requests - [http://docs.python-requests.org/en/latest/index.html](http://docs.python-requests.org/en/latest/index.html()
* BeautifulSoup - [http://www.crummy.com/software/BeautifulSoup/](http://www.crummy.com/software/BeautifulSoup/)
* py2exe (If you want to create an executable) - [http://www.py2exe.org/](http://www.py2exe.org/)

Usage
-----
Assuming you meet all the requirements listed above, all you need to do is run __main.py__  Pokebot will ask for your Facebook email and password, as well as an amount of time to wait between checking for pokes.  Once all of that information is squared away, Pokebot will run on a continuous loop until you tell it to stop.