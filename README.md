# frytz
making calls from command line (via your FritzBox)


## Usage

* enable the *dial helper* (*Wählhilfe*) in the FritzBox
* set the FritzBox's password at the top of frytz.py (look for `PASSWORD`)
* put frytz.py to somewhere in your *$PATH* (I have it symlinked to `dial`)
* enter `fritz.py +492219876543210` to make a call to *+492219876543210*
* pick up the default telephone configured in the FritzBox and listen to ringing phone
* eventually talk to the person you are calling


## Caveats

* you need at least FritzOS 5.5 on your FritzBox for this script to work
* you need [requests](http://docs.python-requests.org/en/latest/) installed (old versions as in Debian stable should work)
