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
var SpotifyWebApi = require('spotify-web-api-node');

var client_id = getClientId(); // Your client id
var client_secret = getClientSecret(); // Your secret

// credentials are optional
var spotifyApi = new SpotifyWebApi({
  clientId : getClientId(),
  clientSecret : getClientSecret(),
  redirectUri : getRedirectURI()
});

function getClientId(){
  return '2153204389124b6097a0e86ca3a17f46'; // Your client id
}

function getClientSecret(){
  return '55a4e744962a4d8e97bf54cc4bc44c32'; // Your secret
}

function getRedirectURI(){
  return 'http://localhost:8888/callback'; // Redirect URI
}

/*
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
*/

// gets recomended songs based on given features
function getRecomendations(options){
  getAuthorizationToken(function(token) { 
      spotifyApi.setAccessToken(token);
      spotifyApi.getRecommendations(options)
      .then(function(data) {
          console.log('Artist albums', data.body);
      }, function(err) {
          console.error(err);
      });
  });
}

// gets the audio features for a given song id
function getAudioFeaturesForTrack(trackID, callback){
  getAuthorizationToken(function(token) { 
      spotifyApi.setAccessToken(token);
      spotifyApi.getAudioFeaturesForTrack(trackID)
      .then(function(data) {
          callback(data);
      }, function(err) {
          console.log('Something went wrong!', err);
      });
  });
}

// gets the audio features for a given song id
function getPlaylistTracks(UserID, PlaylistID, callback){
  getAuthorizationToken(function(token) { 
      spotifyApi.setAccessToken(token);
      spotifyApi.getPlaylistTracks(UserID, PlaylistID)
      .then(function(data) {
          callback(data);
      }, function(err) {
          console.log('Something went wrong!', err);
      });
  });
}

function getAuthorizationToken(callback){
  var token;
  // your application requests authorization
  //document.getElementById("demo").innerHTML = "test";
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
          token = body.access_token;
          callback(token);
      }
  });
  
}
/*
var params = {min_energy: 0.4, seed_artists: ['6mfK6Q2tzLMEchAr0e9Uzu', '4DYFVNKZ1uixa6SQTvzQwJ'], min_popularity: 0 };

getAudioFeaturesForTrack('4tgJDSBLGNnDZC3BOTJAuy', function(data){ 
  console.log(data.body)
});
*/

getPlaylistTracks('124632828', '6X2OFVuHppo7uZHPjfJitd', function(data){
  for(var i=0; i<data.body.total; i++){
    getAudioFeaturesForTrack(data.body.items[i].track.id, function(data){ 
      console.log(data.body)
    });
  }
});

var app = express();
app.use(express.static(__dirname));
console.log('Listening on 8888');
app.listen(8888);