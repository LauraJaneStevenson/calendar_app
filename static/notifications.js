
// function to handle notification responses
const handleApprove = (approved,id) => {

    // object to pass to server.py
    console.log('approved in js: ' + approved)
    const notifDetails = {
        'id': id,
        'approved': approved

    };

    // AJAX post request 
    $.post('/handle_notif_response',notifDetails,(res) => {
        alert(res)
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
            <li>
                ${type} from ${from} 
                <button
                    type="button"
                    class="approved"
                    id="approve-${id}"
                    onclick="handleApprove(${true},${id})"
                    onmouseover="handleApprove(${false},${id})"
                >
                    Approve
                </button>
                <button 
                    type="button" 
                    class="approved" 
                    id="deny-${id}"
                    onclick="handleApprove(${false},${id})"
                    onmouseover="handleApprove(${false},${id})"
                >
                    Deny
                </button>
            </li>`);
        
    };
   
});




