# Selenium 

We have seen how to use Python programs to scrape data from websites, but there are three scenarios that make it more challenging

1. Accessing data behind login screens
2.  Having to click through a bunch of stuff to dig into the middle of a website somewhere without a clear URL to jump to
3. Accessing data that is the result of executing JavaScript

[Selenium](http://www.seleniumhq.org/) is a tool that lets us automate actions within a browser as if we were clicking or typing as a human. This lets us login and do anything else a human can do when using the browser. Perhaps most importantly, it allows us to scrape data from webpages that generate HTML using JavaScript executing within the browser; i.e., there are some webpages that are pure JavaScript and no HTML.

## Installation

```bash
pip install -U selenium
pip install chromedriver # if you plan on automating chrome usage
```

Download [Chrome driver binary](https://sites.google.com/a/chromium.org/chromedriver/downloads) as well and/or [FireFox's gecko driver](https://github.com/mozilla/geckodriver/releases). Get `geckodriver-v0.9.0` not v0.10. The pip stuff just makes the python packages but the real meat is in the binary download. I stored the executable binaries in a standard place:

```bash
mv ~/Downloads/chromedriver /usr/local/bin
mv ~/Downloads/geckodriver /usr/local/bin
```

Oh wait. ok, a serious bug prevents firefox usage for 0.9 but 0.10 didn't work either. Ok, Chrome it is. 

## Launching a Chrome Browser

Here is the boilerplate code that launches a chrome browser to the Google search page, waits 5 seconds, and then closes the browser.

```python
import time
from selenium import webdriver

driver = webdriver.Chrome('/usr/local/bin/chromedriver')  # Optional argument, if not specified will search path.
driver.get('http://www.google.com')

# here is where some useful work would typically happen

raw_input("Press Enter to quit")
driver.quit() # close browser
```

Notice that this is creating an entirely new instance of the browser (You'll see more a new chrome icon appear).

## Puppeteering with Chrome Browser

Let's start by asking chrome to perform a search for `USF Analytics`. The
[Selenium python API doc](http://selenium-python.readthedocs.io/locating-elements.html#locating-elements) shows us that we can find elements by name. Conveniently the name of the search entry box is `q`, determined by using `inspect` functionality in the chrome browser itself:

<img src=figures/google-searchbox.png width=500>

Using the boilerplate code from the previous section, we would add the following functionality.

```python
search_box = driver.find_element_by_name('q')
search_box.send_keys('USF Analytics')
search_box.submit()
```

## Support code for logging in

We don't ever want to store a username and password in our source code. Also, if we hardcoded info like that, we could not use software for different users. Instead, I built a little dialog box that asks for a username and password from the user. The `login()` returns when the user clicks on the `Login` button:

```python
from Tkinter import *

def login():
    master = Tk()
    Label(master, text="Username").grid(row=0)
    Label(master, text="Password").grid(row=1)
    user = Entry(master)
    password = Entry(master, show="*")
    user.grid(row=0, column=1)
    password.grid(row=1, column=1)
    Button(master, text='Login', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
    
    mainloop()
    return user.get(), password.get()

if __name__ == '__main__':
    print login()
```

**Exercise**: Run that program and verify that it prints out a sample (meaningless) username and password.
 
## Log in to twitter, pull a following list

 In order to login to twitter, we can go directly to `https://twitter.com/login`, where we see `form` fields:

```html
<input class="js-username-field email-input js-initial-focus"
 type="text"
 name="session[username_or_email]"
 autocomplete="on" value="" placeholder="Phone, email or username">
```

and

```html
<input class="js-password-field"
 type="password" name="session[password]"
 placeholder="Password">
```

That is where the user should enter their username and password. We need to launch a chrome browser at that URL and then inject characters into those two fields.  I tried selecting the input fields by `name` but it didn't work so I had to use the CSS `class` selector.

**Exercise**:  Write a script to login to twitter and view the list of accounts followed by our data Institute. You can get this information here `https://twitter.com/DataInstituteSF/following` but only if you are logged in. You need these statements to select the input fields:

```python
userfield = driver.find_element_by_css_selector('.js-username-field.email-input.js-initial-focus')
passwordfield = driver.find_element_by_css_selector('.js-password-field')
```

**Exercise**:  Alter the script so that it (i) pages down twice using: `driver.execute_script("window.scrollTo(0, 10000);")` and (ii) collects all of the `following` `a` tags into a list of tuples with (*link*,*link text*). I get:

```
[(u'https://twitter.com/DataInstituteSF', u''), 
(u'https://twitter.com/Vungle', u'Vungle'),
(u'https://twitter.com/fueledbytri', u'Kimberly Shenk'),
(u'https://twitter.com/decodyng', u'Cody Wild'),
(u'https://twitter.com/samswey', u'Samuel Sinyangwe'),
(u'https://twitter.com/CRASEusf', u'CRASE'),
(u'https://twitter.com/oaklandmuseumca', u'Oakland Museum of CA'),
(u'https://twitter.com/Tate', u'Tate'), 
(u'https://twitter.com/deyoungmuseum', u'de Young Museum'),
(u'https://twitter.com/SFMOMA', u'SFMOMA'),
(u'https://twitter.com/interian', u'Yannet Interian'),
(u'https://twitter.com/jeremyphoward', u'Jeremy Howard'),
(u'https://twitter.com/the_antlr_guy', u'The ANTLR Guy'),
(u'https://twitter.com/usfcs', u'USF CS'),
(u'https://twitter.com/kaggle', u'Kaggle'),
(u'https://twitter.com/HamrickJeff', u'Jeff Hamrick'),
(u'https://twitter.com/sjengle', u'Sophie Engle'),
(u'https://twitter.com/bayesimpact', u'Bayes Impact'),
(u'https://twitter.com/kdnuggets', u'Gregory Piatetsky')]
```

The links are of the form:
 
```html
<a class="ProfileNameTruncated-link u-textInheritColor js-nav js-action-profile-name"
 href="/Vungle"
 data-aria-label-part="">
 Vungle
</a>
...
<a class="ProfileNameTruncated-link u-textInheritColor js-nav js-action-profile-name"
 href="/decodyng"
 data-aria-label-part="">
 Cody Wild
</a>
```    

and you can select them by using:
 
```python
links = driver.find_elements_by_css_selector('a.ProfileNameTruncated-link')
```
