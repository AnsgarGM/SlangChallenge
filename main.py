import requests
import datetime
import keys

if __name__ == '__main__':

    res = requests.get( "https://api.slangapp.com/challenges/v1/activities", headers = { "Authorization": keys.auth_header } )
    if res.status_code == 200:
        print( res.json() )
