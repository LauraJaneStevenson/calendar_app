let evt_showing = false;

document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');

  const eventList = $.get('/approved_events.json', (res) =>{

  console.log("Event List: " + eventList);
  var calendar = new FullCalendar.Calendar(calendarEl, {
    plugins: [ 'interaction', 'dayGrid', 'timeGrid' ],
    defaultView: 'timeGridWeek',
    defaultDate: '2019-11-11',
    header: {
      left: 'prev,next today',
      center: 'title, addEventButton',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    eventRender: function(info) {
      //AJAX request 
      var tooltip = new Tooltip(info.el, {
        title: 'Created by: ' + info.event.extendedProps.author,
        placement: 'top',
        trigger: 'hover',
        container: 'body'
      });
    },
    selectable: true,
    events: res,
    select: function(info) {
      console.log('info: '+ info.startStr)
      let startT = prompt('Enter Start Time: ', getTime(info.startStr));
      let endT = prompt('Enter End Time: ', getTime(info.endStr));

      startT = setDateTime(startT,info.startStr);
      endT = setDateTime(endT,info.endStr);
      
      let eventType = prompt('Enter Event Type(Quiet hours, Bathroom, Party): ');
      const eventDetails = {
        'start': startT,
        'end': endT,
      'eventType': eventType
      };

      $.post('/add_event',eventDetails,(response) =>{
        alert(response);
      });
      calendar.addEvent({
              title: eventType,
              start: startT,
              endTime: endT,
              backgroundColor: '#90ee90',    
      });         
    },
    customButtons: {
      addEventButton: {
        text: 'show my requested events',
        click: function() {
          // evt_showing.toggle();
          //AJAX request to get unapproved events
          $.get('unapproved_events.json',(res) =>{

            // if statement to toggle between displaying user's unapproved events 
            if(evt_showing){

              // get all events on calendar
              const allEvents = calendar.getEvents();

              // create empty set
              const eventIds = new Set();

              // for all the events from the response
              for(const event of res){
                // add event ids to set
                eventIds.add(event.id);

              }
              // loop over all events on calendar 
              for(const event of allEvents){
                // see if each event's id is in the id set
                if(eventIds.has(parseInt(event.id))){
                  // if so, remove it from the calendar
                  event.remove();
                }
              }

              evt_showing = false;

            }else{
  
                for(const event of res){

                  calendar.addEvent({

                    title: event.title,
                    id: event.id,
                    start: event.start,
                    endTime: event.end,
                    author: event.author,
                    backgroundColor: '#90ee90', 

                  });

                };

             

              evt_showing = true;

            }
          });
        console.log(evt_showing); 

        }
      }
     },

   


  });


  calendar.render();

});

 });
// console.log(evt_showing);


