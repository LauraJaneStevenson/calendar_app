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
      let startT = prompt('Enter Start Time: ', info.startStr);
      let endT = prompt('Enter End Time: ', info.endStr);
      console.log('endT: ' + endT)
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

            if(evt_showing){

              

              for(const event of res){

                // $('#calendar').fullCalendar( ‘removeEvents’);

              }
              evt_showing = false;

            }else{

              
                
                for(const event of res){

                  calendar.addEvent({

                    title: event.title,
                    id: event.id,
                    start: event.start,
                    endTime: event.end,
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


