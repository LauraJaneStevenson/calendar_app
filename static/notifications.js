

// request access to calendar
$('button.request_access').on('click',(evt) => {

    // get value for cal_id to pass through with ajax
    const button = $(evt.target);
    const cal_id = button.attr('id');
    // alert("ID:" + cal_id);
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

    //list all notifications

 $.get('/get_notifications.json',(response) => {
        // get length of json object so we can loop through it

        console.log('1')
        jsonSize = Object.keys(response).length;
        console.log(jsonSize)
         for (let i = 0; i < jsonSize;i++){
           console.log('3')
            let id = response[i].id;
            console.log(id);
            $('#notifications').append(`<li>$${id}</li>`);
            console.log('4')
        };
           
     });