var SecretData = require('../SecretData.js');
let secretData = new SecretData();
var request = require('request');

var SpotifyWebApi = require('spotify-web-api-node');
var client_id = secretData.client_id; // Your client id
var client_secret = secretData.client_secret; // Your secret

// credentials are optional
var spotifyApi = new SpotifyWebApi({
    clientId : secretData.client_id,
    clientSecret : secretData.client_secret,
    redirectUri : secretData.redirec_tUri
});

// gets recomended songs based on given features
function getRecomendations(options){
    getAuthorizationToken(function(token) { 
        spotifyApi.setAccessToken(token);
        spotifyApi.getRecommendations(options).then(function(data) {
            console.log('Artist albums', data.body);
        }, function(err) {
            console.error(err);
        });
    });
}

// doesn't seem to be outputting to JSON very well
function getSongsByName(songName){
    getAuthorizationToken(function(token) { 
        spotifyApi.setAccessToken(token);
        spotifyApi.searchTracks('track:'+songName)
        .then(function(data) {
        console.log('Search by ' + songName, data.body);
        }, function(err) {
        console.error(err);
        });
    });
}

// doesn't seem to be outputting to JSON very well
function getSongsByArtist(artistName){
    getAuthorizationToken(function(token) { 
        spotifyApi.setAccessToken(token);
        spotifyApi.searchTracks('artist:'+artistName)
        .then(function(data) {
        console.log('Search tracks by ' + artistName + ' in the artist name', data.body);
        }, function(err) {
        console.log('Something went wrong!', err);
        });
    });
}

// gets the audio features for a given song id
function getAudioFeaturesForTrack(trackID, callback){
    getAuthorizationToken(function(token) { 
        spotifyApi.setAccessToken(token);
        spotifyApi.getAudioFeaturesForTrack(trackID)
        .then(function(data) {
            //console.log(data.body);
            callback(data);
        }, function(err) {
            console.log('Something went wrong!', err);
        });
    });
        
}

function getTest(test){
    document.getElementById("demo").innerHTML = test;
    return test;
}
function getAuthorizationToken(callback){
    var token;
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
            token = body.access_token;
            callback(token);
        }
    });
    
}
var params = {min_energy: 0.4, seed_artists: ['6mfK6Q2tzLMEchAr0e9Uzu', '4DYFVNKZ1uixa6SQTvzQwJ'], min_popularity: 0 };

getAudioFeaturesForTrack('4tgJDSBLGNnDZC3BOTJAuy', function(data){ 
    console.log(data.body)
});
console.log(getTest(1));
