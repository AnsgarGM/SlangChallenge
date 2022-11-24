import requests
import datetime
import keys
import json

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

def make_session( activity ):
    session = {
        "started_at": activity["first_seen_at"],
        "ended_at": activity["answered_at"],
        "activity_ids": [activity["id"]]
    }
    return session

def make_user_sessions( data ):
    MAX_TIME = datetime.timedelta( seconds = 300 )
    # Sorting activities cronologically
    sorted_act = sorted( data["activities"], key = lambda i : i ["first_seen_at"] )
    # Getting activities divided by user
    by_user = get_activity_by_user( sorted_act )
    # print( by_user )

    user_sessions = {}
    for user, activities in by_user.items():
        sessions = []
        session = make_session( activities[0] )
        # Finding activities with more than 5 minutes diference
        for activity in activities:
            if not activity["id"] in session["activity_ids"]:
                if datetime.datetime.fromisoformat( activity["first_seen_at"] ) - datetime.datetime.fromisoformat( session["ended_at"] ) > MAX_TIME:
                    session["duration_seconds"] = ( datetime.datetime.fromisoformat( session["ended_at"] ) - datetime.datetime.fromisoformat( session["started_at"] ) ).seconds
                    sessions.append( session.copy() )
                    session = make_session( activity )
                else:
                    # Add to "activity_ids"
                    session["activity_ids"].append( activity["id"] )
                    # Update "ended_at" key
                    session["ended_at"] = activity["answered_at"]
        # Adding last session to sessions list
        session["duration_seconds"] = ( datetime.datetime.fromisoformat( session["ended_at"] ) - datetime.datetime.fromisoformat( session["started_at"] ) ).seconds
        sessions.append( session.copy() )
        user_sessions[user] = sessions.copy()

    return user_sessions

if __name__ == '__main__':

    res = requests.get( "https://api.slangapp.com/challenges/v1/activities", headers = { "Authorization": keys.auth_header } )
    if res.status_code == 200:
        user_sessions = { "user_sessions": make_user_sessions( res.json() ) }

        print( json.dumps( user_sessions, indent=4 ) )

        res = requests.post( "https://api.slangapp.com/challenges/v1/activities/sessions",
                        headers = { "Authorization": keys.auth_header },
                        json = user_sessions )
        print( res.status_code )
        if res.status_code == 204:
            print( "Data sent c:" )
            print( "Have a nice day!" )
