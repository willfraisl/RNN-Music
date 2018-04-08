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

function getClientId(){
  return '2153204389124b6097a0e86ca3a17f46'; // Your client id
}
function getClientSecret(){
  return '55a4e744962a4d8e97bf54cc4bc44c32'; // Your secret
}
function getRedirectURI(){
  return 'http://localhost:8888/callback'; // Redirect URI
}

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
      url: 'https://api.spotify.com/v1/users/jmperezperez',
      headers: {
        'Authorization': 'Bearer ' + token
      },
      json: true
    };
    request.get(options, function(error, response, body) {
      console.log(body);
    });
  }
});

var app = express();
app.use(express.static(__dirname));
console.log('Listening on 8888');
app.listen(8888);
