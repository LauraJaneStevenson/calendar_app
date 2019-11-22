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
      var tooltip = new Tooltip(info.el, {
        title: '<h1>hi</h1>',
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
        text: 'add event...',
        click: function() {
          var dateStr = prompt('Enter a date in YYYY-MM-DD format');
          var date = new Date(dateStr + 'T00:00:00'); // will be in local time
          if (!isNaN(date.valueOf())) { // valid?
            calendar.addEvent({
              title: 'dynamic event',
              start: date,
              allDay: true
            });
            alert('Great. Now, update your database...');
          } else {
            alert('Invalid date.');
          }
        }
      }
     }

   


  });


  calendar.render();

});

 });