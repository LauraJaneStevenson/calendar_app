

from model import connect_to_db, db, User, Calendar, Event, EventRequest

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
    """Retuns user object"""

    return EventRequest.query.filter_by(request_id=request_id).one()

def get_calendar(cal_id):
    """Returns calendar object"""
    
    return Calendar.query.filter_by(cal_id=cal_id).one()

def get_notifications(user_id):
    """Returns list of notifications for specific user"""

    return EventRequest.query.filter_by(to_user_id=user_id).all()


def get_approved_events(cal_id):
    """Returns a list of all approved events on given calendar"""

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





















