import document from "document";
import * as messaging from "messaging";
import { vibration } from "haptics";

let ALERT_STATUS={
  'wrong_direction': false,
  "blink_too_slow": false,
  "blur_sight": false,
  "usage_too_long": false};
let ALERT_SHOW=false;
let ALERT_QUEUE = [];
let icon_element = document.getElementById("alert_icon");

// Listen for the onopen event
messaging.peerSocket.onopen = function() {
  //ui.updateUI("loading");
  messaging.peerSocket.send("FETCH");
  console.log('on open app');
}

// Listen for the onmessage event
messaging.peerSocket.onmessage = function(evt) {
  console.log('on message app');
  let alerts = evt.data;
  console.log("new alerts:"+alerts);
  if(ALERT_QUEUE.length == 0 && ALERT_SHOW == false) {
    for (var i = 0; i < alerts.length+1; ++i){
      if (ALERT_STATUS[alerts[i]] == false){
        ALERT_QUEUE.push(alerts[i]);
      }
    }
    console.log("QUEUE:", ALERT_QUEUE);
    if (ALERT_QUEUE.length>0){
      updateUI();
    }
  }
}

// Listen for the onerror event
messaging.peerSocket.onerror = function(err) {
  // Handle any errors
  icon_element.href="Easy_Eye.jpg";
}

// Function to update the UI given the alert type. Alert types: wrong_direction, blink_too_slow, blur_sight, usage_too_long.
function updateUI(){
  console.log("updateUI", ALERT_QUEUE)
  
  //ALERT_SHOW = false;
  let alert = ALERT_QUEUE[0]
  switch(alert) {
    case 'wrong_direction':
      if (ALERT_STATUS['wrong_direction'] == false){
        icon_element.href="wrong_direction.jpg";
        console.log("photo changed 1")
        vibration.start("alert");
        console.log("Vibration 1");
        setTimeout(vibration.stop, 500);
        setTimeout(function(){ALERT_STATUS['wrong_direction']=false}, 5*60*1000);
        ALERT_SHOW=true;
        console.log("ALERT_SHOW set to true 1");
      }
      
    break;
    case 'blink_too_slow':
      if (ALERT_STATUS['blink_too_slow'] == false){
        icon_element.href="blink.jpg";
        vibration.start("alert");
        console.log("Vibration 2");
        setTimeout(vibration.stop, 500);
        setTimeout(function(){ALERT_STATUS['blink_too_slow']=false}, 10*1000);
        ALERT_SHOW=true;
        console.log("ALERT_SHOW set to true 2");
      }
    break;
    case 'blur_sight':
      if (ALERT_STATUS['blur_sight'] == false){
        icon_element.href="blur_sight.jpg";
        vibration.start("alert");
        console.log("Vibration 3");
        setTimeout(vibration.stop, 500);
        setTimeout(function(){ALERT_STATUS['wrong_direction']=false}, 30*1000);
        ALERT_SHOW=true;
        console.log("ALERT_SHOW set to true 3");
      }
    break;
    case 'usage_too_long':
      if (ALERT_STATUS['usage_too_long'] == false){
        icon_element.href="usage_too_long.jpg";
        vibration.start("alert");
        console.log("Vibration 4");
        setTimeout(vibration.stop, 1000);
        setTimeout(function(){ALERT_STATUS['usage_too_long']=false}, 15*60*1000);
        ALERT_SHOW=true;
        console.log("ALERT_SHOW set to true 4");
      }
      break;
    default:
      icon_element.href="Easy_Eye.jpg";
      ALERT_SHOW=false;
      console.log("ALERT_SHOW set to false 1");
  };
  ALERT_STATUS[alert] = true;
  ALERT_QUEUE.shift();
  if (ALERT_QUEUE.length != 0){
    setTimeout(updateUI, 3000);
  }else{
    setTimeout(function(){ALERT_SHOW=false;
                          console.log("ALERT_SHOW set to false 2");
                         icon_element.href="Easy_Eye.jpg";}, 3000);
  }
  
};
function fetch_alert(){
  if (ALERT_SHOW == false){
    messaging.peerSocket.send("FETCH");
    console.log("A FETCH is sent.")
  }
  setTimeout(function(){fetch_alert();}, 1000);
}

setTimeout(function(){fetch_alert();}, 2000);