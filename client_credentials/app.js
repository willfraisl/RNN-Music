/**
 * This is an example of a basic node.js script that performs
 * the Client Credentials oAuth2 flow to authenticate against
 * the Spotify Accounts.
 *
 * For more information, read
 * https://developer.spotify.com/web-api/authorization-guide/#client_credentials_flow
 */
var express = require('express'); // Express web server framework
var request = require('request'); // "Request" library
//var SecretData = require('./SecretData.js');
//let secretData = new SecretData();

var client_id = getClientId(); // Your client id
var client_secret = getClientSecret(); // Your secret

// your application requests authorization
var authOptions = {
  url: 'https://accounts.spotify.com/api/token',
  headers: {
    'Authorization': 'Basic ' + (new Buffer(client_id + ':' + client_secret).toString('base64'))
  },
  form: {
    grant_type: 'client_credentials'
  },
  json: true
};

request.post(authOptions, function(error, response, body) {
  if (!error && response.statusCode === 200) {

    // use the access token to access the Spotify Web API
    var token = body.access_token;
    var options = {
      url: 'https://api.spotify.com/v1/users/124632828/playlists/6X2OFVuHppo7uZHPjfJitd/tracks',
      headers: {
        'Authorization': 'Bearer ' + token
      },
      json: true
    };
    //gets list of track ids
    request.get(options, function(error, response, body) {
      for(var i=0; i<body.total; i++){
        console.log(body.items[i].track.id);
      }
    });
  }
});

var app = express();
app.use(express.static(__dirname));
console.log('Listening on 8888');
app.listen(8888);
