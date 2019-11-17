

// request access to calendar
$('#request_access').on('click',() => {
    
    // get value for cal_id to pass through with ajax
    let cal_id = $('#request_access').attr('value');
    console.log(cal_id)
    // make ajax request
    $.post('/request_access_to_cal',{ cal_id: cal_id },(res) => {
        //alers user that request has been sent
        alert(res);
    });
});

