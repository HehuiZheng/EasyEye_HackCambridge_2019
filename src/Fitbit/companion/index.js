/*
 * Entry point for the companion app
 */

console.log("Companion code started");

import { me } from "companion";
import * as messaging from "messaging";

let last_timestamp = null;

// Listen for the onopen event
messaging.peerSocket.onopen = function() {
  console.log('on open campanion')
}

// Listen for the onmessage event
messaging.peerSocket.onmessage = function(evt) {
  // Output the message to the console
  console.log('on message companion')
  if (evt.data=='FETCH'){
    fetch_data();
    //let test_alerts=['wrong_direction','blink_too_slow','usage_too_long', 'blur_sight'];
    //messaging.peerSocket.send(test_alerts);
  }
}

// Function to fetch data and send it back to app.
function fetch_data(){
  fetch('https://zhilingmail.pythonanywhere.com/api/get_alert')
  .then(response => response.json())
  .then(data => {
    console.log(data['alert']);
    console.log("timestamp:", data['timestamp'])
    if (last_timestamp != null){
      console.log("last_timestamp:", last_timestamp);
      if (last_timestamp !=data['timestamp']) {
         last_timestamp = data['timestamp'];
         let alerts = data['alert'];
         messaging.peerSocket.send(alerts);
      } 
    } else {
      last_timestamp = data['timestamp'];
      fetch_data();
    }
  })
  .catch(error => console.error(error));
}