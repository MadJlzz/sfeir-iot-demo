/**
 * Triggered from a message on a Cloud Pub/Sub topic.
 *
 * @param {!Object} event Event payload and metadata.
 * @param {!Function} callback Callback function to signal completion.
 */

const request = require('request');

exports.helloPubSub = (event, callback) => {
  console.log("Event data", event.data);
  
  var realData = JSON.parse(Buffer.from(event.data.data, 'base64').toString());
  console.log("Real data", realData)
  
  const params = {
    "name": "open",
    "parameters": []
  };
  
  if (realData.humidity > 60) {
    
    console.log("Trigger because humidity");
    
    // DO THE HTTP POST
    request({
      url: 'https://api.somfy.com/api/v1/device/880fca4b-2e119632-6781e3b7-f6e1140e/exec',
      method: "POST",
      json: true,
      body: params,
      headers: { 
        'Authorization': '<REPLACE WITH TOKEN>',
        'Content-Type': 'application/json'
      }
    }, (err, resp, body) => {
      console.log("Error", err);
      console.log("Response", resp);
      console.log("Body", body);
      callback();
    });
  }
};
