

from model import connect_to_db, db, User, Calendar, Event, EventRequest

from twilio.rest import Client

from twilio.twiml.messaging_response import MessagingResponse

import os

def get_user(user_id):
    """Retuns user onject"""

    return User.query.filter_by(user_id=user_id).one()

def get_event(event_id):
    """Retuns user onject"""

    return Event.query.filter_by(event_id=event_id).one()

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

def send_init_sms(event_id,user_id):
    """Taked in notification id and uses twilio api to send text to user's housemates"""

    event = get_event(event_id)
    from_user = get_user(event.user_id).name
    to_user = get_user(user_id)

    message = f"""Your housemate {from_user} has requested the event,
    {event.event_type} from {event.start_time} to {event.end_time}. 
    Reply 'Y' to accept or 'N' to deny."""

    account_sid = os.environ.get('ACCOUNT_SID')
    auth_token = os.environ.get('AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=message,
                         from_=os.environ.get('SMS_NUMBER'),
                         to=os.environ.get('SMS_TO')
                     )

    print(message.sid)





















