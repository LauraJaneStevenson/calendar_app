
// function to handle notification responses
const handleApprove = (approved,id) => {

    // object to pass to server.py
    console.log('approved in js: ' + approved)
    const notifDetails = {
        'id': id,
        'approved': approved

    };
    // calendar.add

    // AJAX post request 
    $.post('/handle_notif_response',notifDetails,(res) => {
        alert(res)
    }); 


    // $.get('/event_req_notif.json',{ 'id':notifDetails.id },(res) =>{
    //     console.log("In handleApprove notifications.js:" + res.title);
    //     //calendar.addevent
    //     $('#calendar').fullCalendar('renderEvent', {
    //         title: res.title,
    //         id: res.id,
    //         start: res.start,
    //         endTime: res.end,
    //         author: res.author,
    //         backgroundColor: '#90ee90', 
    //     });

    //     // $('#calendar').fullCalendar.addEvent({

    //     //     title: res.title,
    //     //     id: res.id,
    //     //     start: res.start,
    //     //     endTime: res.end,
    //     //     author: res.author,
    //     //     backgroundColor: '#90ee90', 

    //     // });
    // });   
  
};
// gives user info about the event request
function showRequested(id) {

    $.get('/event_req_notif.json',{ 'id':id }, (res) => {
        // calendar.addevent
        // alert(`${res.title} at ${res.start} until ${res.end}. Click approve at add to calendar.`);


            let tooltip = new Tooltip($('li.notifications'), {
                title: 'Event Type: ' + res.title + '\n' + 'From ' + res.start 
                + '\n' + 'To' + res.end,
                placement: 'top',
                trigger: 'hover',
                container: 'body'
            });
        

    });
};

//list all notifications
$.get('/get_notifications.json',(response) => {
    // get length of json object so we can loop through it
    // console.log('1')

    jsonSize = Object.keys(response).length;
    // console.log(jsonSize)

    for (const notification of response) {
       // console.log('3')
        const id = notification.id;
        const type = notification.type;
        const from = notification.from
        console.log(id);

        $('ul.notifications').append(`
            <li class='notifications'>
                ${type} from ${from} 
                <button
                    type="button"
                    class="approved"
                    id="approve-${id}"
                    onclick="handleApprove(${true},${id})"
                    onmouseover="showRequested(${id})"
                >
                    Approve
                </button>
                <button 
                    type="button" 
                    class="approved" 
                    id="deny-${id}"
                    onclick="handleApprove(${false},${id})"
                    onmouseover="showRequested(${id})"
                >
                    Deny
                </button>
            </li>`);
        
    };
   
});




