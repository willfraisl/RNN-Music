/**
 * RNN-Music
 * app.js
 * Will Fraisl
 * Erik Fox
 */

var request = require('request'); // "Request" library

var client_id = 'c0f7fcc3fc594f4d9386be861bbc4770'; // client id
var client_secret = '1dd93767a7f64d249058ff32f4cbbeee'; // secret

// application requests authorization
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
      url: 'https://api.spotify.com/v1/audio-features/11dFghVXANMlKmJXsNCbNl',
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
