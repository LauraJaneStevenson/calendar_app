
// function to handle notification responses
const handleApprove = (approved,id) => {

    // object to pass to server.py
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
                >
                    Approve
                </button>
                <button 
                    type="button" 
                    class="approved" 
                    id="deny-${id}"
                    onclick="handleApprove(${false},${id})"
                >
                    Deny
                </button>
            </li>`);
        
    };
   
});



// request access to calendar
$('button.request_access').on('click',(evt) => {

    // get value for cal_id to pass through with ajax
    const button = $(evt.target);
    const cal_id = button.attr('id');
    alert("ID:" + cal_id);
    // console.log(cal_id)

    // make ajax request
    $.post('/request_access_to_cal',{ 'cal_id': cal_id },(res) => {
        //alers user that request has been sent
        alert(res);
    });

});

// invite user to calendar
$('button.invite').on('click',(evt) => {

    // get value of invited user's user_id to pass through with ajax
    const button = $(evt.target);
    const user_id = button.attr('id');
    console.log(user_id);
    // make ajax request
    $.post('/invite',{ 'user_id': user_id },(res) => {
        //alers user that they have invited user to calendar
        alert(res);
    });
});



