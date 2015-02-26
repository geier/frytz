# frytz
making calls from command line (via your FritzBox)


## Usage

* enable the *dial helper* (*Wählhilfe*) in the FritzBox
* set the FritzBox's password at the top of frytz.py (look for `PASSWORD`)
* put frytz.py to somewhere in your *$PATH* (I have it symlinked to `dial`)
* enter `fritz.py +492219876543210` to make a call to *+492219876543210*
* pick up the default telephone configured in the FritzBox and listen to ringing phone
* eventually talk to the person you are calling

## Tips

This script works nicely with [pycarddav](https://github.com/geier/pycarddav) and [choose](https://github.com/geier/choose).
I use this shell script (called `call`) to make calls from my address book:

    #!/bin/sh
    number=`pc_query -t $1 | choose | cut -f 2`;  frytz.py $number

Usage:

    call Hanz

will present a list of phone numbers matching to *Hanz*. Once one is selected in choose (arrows to navigate, *enter* to select), the number will be called.

## Caveats

* you need at least FritzOS 5.5 on your FritzBox for this script to work
* you need [requests](http://docs.python-requests.org/en/latest/) installed (old versions as in Debian stable should work)
