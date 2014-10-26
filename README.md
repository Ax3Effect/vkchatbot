python-vkbot
============

VK Chat bot written on Python.

You need:

* Python 3 (doesn't work on Python 2)
* vk (pip install vk)
* requests (pip install requests)
* configobj (pip install configobj)

Secondary modules (not necessary):
* termcolor - for making names bold in terminal (pip install termcolor)
* dataset - for logging message count (pip install dataset)
* ReddiWrap - for reddit things - download ReddiWrap.py from https://github.com/derv82/reddiwrap/ and put it in the root folder
* Wand - http://docs.wand-py.org/en/0.3.8/

Also you need to provide access_token (you can find out more at https://vk.com/dev/auth_mobile )
And you need to provide "settings.ini" file with "vk_token" on it, like:
vk_token = "123asd".
You may also add Forecast.io API key:
forecastio = "321dsa"

Don't forget to customize your IDs in the script.
