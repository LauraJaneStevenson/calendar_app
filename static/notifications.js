


$('button.request_access').on('click',(evt) => {

    const button = $(evt.target);
    const cal_id = button.attr('id');
    alert("ID:" + cal_id);
    console.log(cal_id)


    $.post('/request_access_to_cal',{ 'cal_id': cal_id },(res) => {
        //alers user that request has been sent
        alert(res);
    });

});

// // request access to calendar
// $('#request_access').on('click',() => {
    
//     // get value for cal_id to pass through with ajax
//     let cal_id = $('#request_access').attr('value');
//     console.log(cal_id)
//     // make ajax request
//     $.post('/request_access_to_cal',{ cal_id: cal_id },(res) => {
//         //alers user that request has been sent
//         alert(res);
//     });
// });

// invite user to calendar
$('#invite').on('click',() => {
    
     // get value of invited user's user_id to pass through with ajax
    let user_id = $('#invite').attr('value');
    console.log(user_id)
    // make ajax request
    $.post('/invite',{ user_id: user_id },(res) => {
        //alers user that they have invited user to calendar
        alert(res);
    });
});

//list all notifications

// $.get('/get_notifications.json',(response) => {
    
//     // get length of json object so we can loop through it
//     jsonSize = Object.keys(response).length;

//      for (let i = 0; i < jsonSize;i++){
       
//         let id = response[i].id;
//         console.log(id);
//         $('#notifications').append(`<li>$${id}</li>`);
    
//     };
       
//  });