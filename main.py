import requests
import datetime
import keys

def get_activity_by_user( data ):
    act_user = {}
    ids = []
    for activity in data:
        ids.append( activity["id"] )
        if not activity["user_id"] in act_user.keys():
            act_user[activity["user_id"]] = []
        act_user[activity["user_id"]].append( activity["id"] )
            
    return act_user

def make_user_sessions( data ):
    # Sorting activities cronologically
    sorted_act = sorted( data["activities"], key = lambda i : i ["first_seen_at"] )
    # Getting activities divided by user
    by_user = get_activity_by_user( sorted_act )
    print( by_user )

if __name__ == '__main__':

    res = requests.get( "https://api.slangapp.com/challenges/v1/activities", headers = { "Authorization": keys.auth_header } )
    if res.status_code == 200:
        print( "Yei", end = "\n" )
        make_user_sessions( res.json() )
