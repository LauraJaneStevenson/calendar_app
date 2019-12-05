//functions to parse event start/end times
const getTime = (timeStr) => {

    // console.log("inside get time")
    // let time = timeStr.slice(11, 16);
    let hour = parseInt(timeStr.slice(11,13));

    if(hour > 12){
        hour = (hour - 12);
        hour = String(hour)
        return hour + timeStr.slice(13,16) + 'P.M.';
        
    }else if(hour == 12){

        return timeStr.slice(11,16) + 'P.M.'

    }else if( hour == 11 || hour == 10) {

        return timeStr.slice(11,16) + 'A.M.'
    }else if(hour == 0){

        return "12" + timeStr.slice(13,16) + 'A.M.'
    };


    return timeStr.slice(12,16) + 'A.M.';   
    
};

const setDateTime = (timeStr,info) =>  {
    //sets times back to iso format
    // console.log('we inside setDateTime')
    let hour;

    if(timeStr.slice(0,2).includes(':')){

        hour = timeStr[0];

    } else {

        hour = timeStr.slice(0,2);
    }
    

    console.log("hour:"+ hour);
    console.log(timeStr)


    if(timeStr.slice(-4) == 'P.M.' && parseInt(hour) < 10){
        //times 1 pm-9pm
        //done
        // console.log('inside first conditional')
        hour = parseInt(hour) + 12;
        timeStr = String(hour) + timeStr.slice(1,4);
      

    }else if(timeStr.slice(-4) == 'P.M.' && parseInt(hour) > 9 && parseInt(hour) < 12){
        //time 10pm-11pm
        //done
        hour = parseInt(hour) + 12;
        timeStr = String(hour) + timeStr.slice(2,5);

    }else if(hour == '12' && timeStr.slice(-4) == 'A.M.'){
        //times 12am
       
        timeStr = '00' + timeStr.slice(2,timeStr.length-4);
        

    } else if(hour == '12' && timeStr.slice(-4) == 'P.M.'){
        //times 12pm
        //done
         timeStr = timeStr.slice(0,timeStr.length-4)
        

    } else if(parseInt(hour) > 9 && parseInt(hour) < 12 && timeStr.slice(-4) == 'A.M.'){
        //times 10am-11am

        
        timeStr = timeStr.slice(0,timeStr.length -4);
        

    } else {
        //times 1am-9am
    
        timeStr = '0' + timeStr.slice(0,timeStr.length -4);

    };

    

    let newStr = info.slice(0,11) + timeStr + info.slice(16,info.length);
    // console.log(newStr)
    return newStr

};
