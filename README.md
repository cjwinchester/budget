# home budgeting app

:fire: :moneybag: :fire:

caveat emptor, this is a 

  __                       .__        _____.__                
_/  |_____________    _____|  |__   _/ ____\__|______   ____  
\   __\_  __ \__  \  /  ___/  |  \  \   __\|  \_  __ \_/ __ \ 
 |  |  |  | \// __ \_\___ \|   Y  \  |  |  |  ||  | \/\  ___/ 
 |__|  |__|  (____  /____  >___|  /  |__|  |__||__|    \___  >
                  \/     \/     \/                         \/ 

not intended to be used in production, ever, for any reason

### Requirements
* python
* virtualenv
* npm


### Environmental variables
* `DJANGO_SECRET_KEY`: what it says on the tin
* `DEBUG`: 'on' resolves to True


### Credentials file
If you want to use the jank "dump data to json and push to google drive" management command, which uses the Google Drive API, you'll need a `client_secret.json` file in `budget/management/commands/`. The auth-ing process for Google Drive is outlined [here](https://developers.google.com/drive/v3/web/quickstart/python#step_1_turn_on_the_api_name).

Once that's set up, `make backup` will create a backup.