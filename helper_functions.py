

from model import connect_to_db, db, User, Calendar, Event, EventRequest, AccessRequest, Invitation, Notification

from twilio.rest import Client

from twilio.twiml.messaging_response import MessagingResponse

import os

def get_user(user_id):
    """Retuns user onject"""

    return User.query.filter_by(user_id=user_id).one()

def get_event(event_id):
    """Retuns event object"""

    return Event.query.filter_by(event_id=event_id).one()

def get_event_request(request_id):
    """Retuns EventRequest object"""

    return EventRequest.query.filter_by(request_id=request_id).one()

def get_invitation(invite_id):
    """Retuns EventRequest object"""

    return Invitation.query.filter_by(invite_id=invite_id).one()

def get_calendar(cal_id):
    """Returns calendar object"""
    
    return Calendar.query.filter_by(cal_id=cal_id).one()

def get_notifications(user_id):
    """Returns list of notifications for specific user"""
    
    print("\n\n\n\n\n\n\n")
    print('The user is',get_user(user_id).name)
    # print(Notification.query.filter_by(to_user_id=user_id).all())
    # print("get_notifications in helper functions")
    print("\n\n\n\n\n\n\n")
    return Notification.query.filter_by(to_user_id=user_id).all()

def get_access_request(request_id):
    """Retuns AccessRequest object"""

    return AccessRequest.query.filter_by(request_id=request_id).one()

def check_consensus(event_id):
    """Checks to see if all housemates approve 
    an event and set event.approved accordingly"""

    # create a list of requests for specific event
    requests = EventRequest.query.filter_by(event_id=event_id).all()
    event = get_event(event_id)

    # if any of the requests .approve = false pop out of function
    for request in requests: 
        if request.approved != True:
            return None

    # else set event approved to true and commit to the DB
    event.approved = True
    db.session.commit()


def get_approved_events(cal_id):
    """Returns a list of all approved events on given calendar"""

    # get list of all currently unapproved events for this calendar 
    events = Event.query.filter_by(cal_id=cal_id,approved=False).all()

    # loop through list and change consensus on event if need be
    for event in events:
        check_consensus(event.event_id)
        
    # return list of all approved events
    return Event.query.filter_by(cal_id=cal_id,approved=True).all()
    
def map_event_colors():
    """Returns a dictionary that links event types to colors"""

    colorDict = {
        'party': '#FF0000',
        'quiet hours': '#800080',
        'shower': '#add8e6'
    }

    return colorDict

def send_init_sms(request_id,user_id):
    """Taked in notification id and uses twilio api to send text to user's housemates"""

    # get the event request object
    event_request = get_event_request(request_id)
    # get the event object 
    event = get_event(event_request.event_id)
    # get the user's name
    from_user = get_user(event.user_id).name
    # get user_id to send text to
    to_user = get_user(user_id)

    message = f"""Your housemate {from_user} has requested the event number 
    {request_id}, {event.event_type} from {event.start_time} to {event.end_time}. 
    Reply 'Y' to accept or 'N' to deny."""

    account_sid = os.environ.get('ACCOUNT_SID')
    auth_token = os.environ.get('AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=message,
                         from_=os.environ.get('SMS_NUMBER'),
                         to=to_user.phone_number
                     )

    print(message.sid)





















