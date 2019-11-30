//functions to parse event start/end times
const getTime = (timeStr) => {

    // console.log("inside get time")
    // let time = timeStr.slice(11, 16);
    let hour = parseInt(timeStr.slice(11,13));

    if( hour > 12){
        hour = (hour - 12);
        hour = String(hour)
        return hour + timeStr.slice(13,16) + 'P.M.';
        
    };

    return timeStr.slice(11,16) + 'A.M.';   
    
};

const setDateTime = (timeStr,info) => {
    //sets times back to iso format
    console.log('we inside setDateTime')
    let hour = timeStr.slice(0,1);
    console.log(hour);
    if(timeStr.slice(4,9) == 'P.M.'){
        hour = parseInt(hour) + 12;
        console.log(timeStr.slice(1,4))
        timeStr = String(hour) + timeStr.slice(1,4);

    }else{

        timeStr = 'O' + String(hour) + timeStr.slice(2,6);
    }


    let newStr = info.slice(0,11) + timeStr + info.slice(16,info.length);
    console.log(newStr)
    return newStr

};