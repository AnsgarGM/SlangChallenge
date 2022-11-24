import requests
import datetime
import keys

def get_activity_by_user( data ):
    final = {}
    for activity in data:
        obj = {}
        if not activity["user_id"] in final.keys():
            final[activity["user_id"]] = []
        obj["id"] = activity["id"]
        obj["answered_at"] = activity["answered_at"]
        obj["first_seen_at"] = activity["first_seen_at"]
        final[activity["user_id"]].append( obj )
    return final

def make_user_sessions( data ):
    # Sorting activities cronologically
    sorted_act = sorted( data["activities"], key = lambda i : i ["first_seen_at"] )
    # Getting activities divided by user
    by_user = get_activity_by_user( sorted_act )
    # print( by_user )

    for user, activities in by_user.items():
        session = {
            "started_at": activities[0]["first_seen_at"],
            "ended_at": activities[0]["answered_at"],
            "activity_ids": [activities[0]["id"]]
        }
        for activity in activities:
            if not activity["id"] in session["activity_ids"]:
                if datetime.datetime.fromisoformat( activity["first_seen_at"] ) - datetime.datetime.fromisoformat( session["ended_at"] ) > datetime.timedelta( seconds = 300 ):
                    session = {
                        "started_at": activity["first_seen_at"],
                        "ended_at": activity["answered_at"],
                        "activity_ids": [activity["id"]]
                    }
                else:
                    # Add to "activity_ids"
                    session["activity_ids"].append( activity["id"] )
                    # Update "ended_at" key
                    session["ended_at"] = activity["answered_at"]
            print( user, session )

if __name__ == '__main__':

    res = requests.get( "https://api.slangapp.com/challenges/v1/activities", headers = { "Authorization": keys.auth_header } )
    if res.status_code == 200:
        print( "Yei", end = "\n" )
        make_user_sessions( res.json() )
