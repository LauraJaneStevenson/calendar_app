let evt_showing = false;
let hm_evt = false;

document.addEventListener('DOMContentLoaded', function() {

  var calendarEl = document.getElementById('calendar');

  const eventList = $.get('/approved_events.json', (res) =>{

  console.log("Event List: " + eventList);

  window.calendar = new FullCalendar.Calendar(calendarEl, {
    plugins: [ 'interaction', 'dayGrid', 'timeGrid' ],
    defaultView: 'dayGridMonth',
    defaultDate: '2019-12-05',
   
    //moment().format('YYYY MM Do')
    // moment().format();
    header: {
      left: 'prev,next today',
      center: 'title, addEventButton',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    eventRender: function(info) {
   
      let tooltip = new Tooltip(info.el, {
        title: 'Created by: ' + info.event.extendedProps.author,
        placement: 'top',
        trigger: 'hover',
        container: 'body'
        
      });
    },
    eventClick: function(info){
   
    },
    selectable: true,
    events: res,
    select: function(info) {
      console.log('info: '+ info.startStr)
      let startT = prompt('Enter Start Time: ', getTime(info.startStr));
      let endT = prompt('Enter End Time: ', getTime(info.endStr));
      let partyTitle;
      let description;
      // let url;
      startT = setDateTime(startT,info.startStr);
      endT = setDateTime(endT,info.endStr);
      
      let eventType = prompt('Enter Event Type(quiet hours, shower, party): ');
      if(eventType == 'party'){
        partyTitle = prompt('Enter Party Name: ');
        description = prompt('Enter a description:');
      }

      // }else if(eventType == 'quiet hours'){

      //   description = prompt('Enter a description:');
      // }
      const eventDetails = {
        'start': startT,
        'end': endT,
        'eventType': eventType,
        'title': partyTitle,
        'description':description
      };

      $.post('/add_event',eventDetails,(response) =>{
        if(eventType != 'shower'){
          alert("An event request has been sent to your housemates!");
        };
        let url = response.url
        let author = response.author
     

        calendar.addEvent({
                title: eventType,
                start: startT,
                endTime: endT,
                backgroundColor: '#286DA8', 
                url: url,
                author: author

        });
      });         
    },
    customButtons: {
      addEventButton: {
        text: 'requested events',
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
                    end: event.end,
                    author: event.author,
                    backgroundColor: '#286DA8',
                    url: event.url 

                  });
                  console.log(event.url);

                };

             

              evt_showing = true;

            }
          });
        console.log(evt_showing); 

        }
      }
     },
     // customButtons: {
     //  addEventButton: {
     //    text: "See hm event requests",
     //    click: function() {
     //      // evt_showing.toggle();
     //      //AJAX request to get unapproved events
     //      $.get("/hm_evt_req.json",(res) =>{

     //        // if statement to toggle between displaying user's unapproved events 
     //        if(hm_evt){

     //          // get all events on calendar
     //          const allEvents = calendar.getEvents();

     //          // create empty set
     //          const eventIds = new Set();

     //          // for all the events from the response
     //          for(const event of res){
     //            // add event ids to set
     //            eventIds.add(event.id);

     //          }
     //          // loop over all events on calendar 
     //          for(const event of allEvents){
     //            // see if each event's id is in the id set
     //            if(eventIds.has(parseInt(event.id))){
     //              // if so, remove it from the calendar
     //              event.remove();
     //            }
     //          }

     //          hm_evt = false;

     //        }else{
  
     //            for(const event of res){

     //              calendar.addEvent({

     //                title: event.title,
     //                id: event.id,
     //                start: event.start,
     //                endTime: event.end,
     //                author: event.author,
     //                backgroundColor: '#90ee90', 

     //              });

     //            };

     //          hm_evt = true;

     //        }
     //      });
     //    console.log(hm_evt); 

     //    }
     //  }
     // },
  });

    calendar.render();
});

 });
// console.log(evt_showing);


