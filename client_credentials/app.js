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
      return Promise.all(playlistTracks.body.items.map(item => {
        return spotifyApi.getAudioFeaturesForTrack(item.track.id);
      }))
    })
    .then(songsAttributes => {
      //save to file here
      fs.writeFile("songs.json", JSON.stringify(songsAttributes), 'utf8', function (err) {
        if (err) {
          return console.log(err);
        }
        const clusterSongs = spawn('python3', ['clusterSongs.py', 'songs.json']);
        clusterSongs.on('close', (code) => {
          console.log(`child process exited with code ${code}`);
          var clusters = JSON.parse(fs.readFileSync('clusters.json', 'utf8'));
          getSongsFromSeed(clusters);
        });
      });
    })
    .catch(err => {
      console.log('error! ' + err);
    });
}

function getSongsFromSeed(clusterJson){
  spotifyApi.getRecommendations()
  .then(data => {
    console.log(data);
  })
  .catch(err => {
    console.log('error ' + err);
  });
  /*
  Promise.all(clusterJson.cluster.map(i => {
    console.log(i.danceability);
    return spotifyApi.getRecommendations({target_danceability: i.danceability});
  }))
  .then(data => {
    console.log(data);
  })
  .catch(err => {
    console.log('error ' + err);
  })
  */
}

spotifyApi.clientCredentialsGrant()
  .then(token => {
    spotifyApi.setAccessToken(token.body.access_token);
    return spotifyApi.getRecommendations({ min_energy: 0.4, seed_artists: [], min_popularity: 50 });
  })
  .then(data => {
    console.log(data);
  })
  .catch(err => {
    console.log('error' + err);
  });

seedPlaylist('124632828', '6X2OFVuHppo7uZHPjfJitd');

var app = express();
app.use(express.static(__dirname));
console.log('Listening on 8888');
app.listen(8888);