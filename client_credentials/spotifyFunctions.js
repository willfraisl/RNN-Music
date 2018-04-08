var request = require('request');
var SpotifyWebApi = require('spotify-web-api-node');

var client_id = getClientId(); // Your client id
var client_secret = getClientSecret(); // Your secret

// credentials are optional
var spotifyApi = new SpotifyWebApi({
    clientId : sgetClientId(),
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

function getAuthorizationToken(callback){
    var token;
    // your application requests authorization
    document.getElementById("demo").innerHTML = "test";
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
