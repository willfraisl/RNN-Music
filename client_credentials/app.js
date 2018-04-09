/**
 * RNN-Music
 * app.js
 * Will Fraisl
 * Erik Fox
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

// gets the tracks in a public playlist
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