//functions to parse event start/end times
const getTime = (timeStr) => {

    let time = timeStr.slice(11, 16);
    return time;
    
};

const setDateTime = (timeStr,info) => {

    let newStr = info.slice(0,11) + timeStr + info.slice(16,info.length);
    return newStr

};