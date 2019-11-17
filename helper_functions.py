

from model import connect_to_db, db, User, Calendar, Event, EventRequest

def get_user(user_id):

    return User.query.filter_by(user_id=user_id).one()

def get_calendar(cal_id):
    
    return Calendar.query.filter_by(cal_id=cal_id).one()

def get_notifications(user_id):
    """Returns list of notifications for specific user"""
    # print("\n\n\n\n\n\n\n")
    # print(EventRequest.query.filter_by(to_user_id=user_id).all())
    # print("\n\n\n\n\n\n\n")

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