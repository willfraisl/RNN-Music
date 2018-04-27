/**
 * RNN-Music
 * app.js
 * Will Fraisl
 * Erik Fox
 */
var express = require('express'); // Express web server framework
var request = require('request'); // "Request" library
var fs = require('fs');
var SpotifyWebApi = require('spotify-web-api-node');
const {spawn} = require("child_process");

// credentials
var spotifyApi = new SpotifyWebApi({
  clientId : 'c0f7fcc3fc594f4d9386be861bbc4770',
  clientSecret : '2be1642fdb974830b848db3156441c91',
  redirectUri : 'http://localhost:8888/callback'
});

function test(){
  document.getElementById("test_text").innerHTML = "button pushed";
}
function seedPlaylist(userID, playlistID){
  spotifyApi.clientCredentialsGrant()
    .then(token => {
      spotifyApi.setAccessToken(token.body.access_token);
      return spotifyApi.getPlaylistTracks(userID, playlistID);
    })
    .then(playlistTracks => {
      return  spotifyApi.getAudioFeaturesForTracks(playlistTracks.body.items.map(item => item.track.id));
    })
    .then(songsAttributes => {
      //save to file here
      console.log("got attributes");
      fs.writeFile("songs.json", JSON.stringify(songsAttributes), 'utf8', function (err) {
        if (err) {
          return console.log(err);
        }
        const clusterSongs = spawn('python3', ['clusterSongs.py', 'songs.json']);
        clusterSongs.on('close', (code) => {
          //console.log(`child process exited with code ${code}`);
          var clusters = JSON.parse(fs.readFileSync('clusters.json', 'utf8'));
          getSongsFromSeed(clusters);
        });
        console.log("clustered songs");
      });
    })
    .catch(err => {
      console.log('error! ' + err);
    });
}

function getSongsFromSeed(clusterJson){
  var data0 = {};
  var clusterRecommendations = 'clusterRecommendations';
  data0[clusterRecommendations] = [];
  var count = 0;
  
  for(var i = 0; i<6;i++){
    spotifyApi.getRecommendations(clusterJson['cluster'][count]).then(data => {  
      var songs = [];
      spotifyApi.getAudioFeaturesForTracks(data['body']['tracks'].map(item => item.id)).then(attributes => {
        var count2 = 0;
        for(var j = 0; j < data['body']['tracks'].length; j++){
          songs.push({"token": data['body']['tracks'][count2]['id'],"attributes": attributes.body.audio_features[count2],"classification": 2});
          count2++;
        }
        data0[clusterRecommendations].push({songs});
        fs.writeFile("newSongs.json", JSON.stringify(data0), function (err) {
          if(err){
            throw err;
          }
        });
        console.log("Reccomendations fetched for cluster " + count);
        count++;
      }).catch(err => {
        console.log('error! ' + err);
      }); 
    }).catch(err => {
      console.log('error ' + err);
    });
  }
  classifySongs();
}

function classifySongs(){
  const classifySongs = spawn('python3', ['classifySongs.py', 'songs.json']);
  classifySongs.on('close', (code) => {
    //console.log(`child process exited with code ${code}`);
    var song = JSON.parse(fs.readFileSync('nextSong.json', 'utf8'));
    console.log(song);
  });
}

seedPlaylist('124632828', '6X2OFVuHppo7uZHPjfJitd');

var app = express();
app.use(express.static(__dirname));
console.log('Listening on 8888');
//app.listen(8888);