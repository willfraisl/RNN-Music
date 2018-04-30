/**
 * Music
 * app.js
 * Will Fraisl
 * Erik Fox
 */
var express = require('express'); // Express web server framework
var request = require('request'); // "Request" library
const readline = require('readline-sync');
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
        /*const clusterSongs = spawn('python3', ['clusterSongs.py', 'songs.json']);
        clusterSongs.on('close', (code) => {
          //console.log(`child process exited with code ${code}`);
          var clusters = JSON.parse(fs.readFileSync('clusters.json', 'utf8'));
          getSongsFromSeed(clusters);
        });*/
        //console.log("clustered songs");
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
          songs.push({
            "name":data['body']['tracks'][count2]['name'],
            "artist": data['body']['tracks'][count2]['artists'][0]['name'],
            "token": data['body']['tracks'][count2]['id'],
            "previewURL":data['body']['tracks'][count2]['preview_url'],
            "attributes": attributes.body.audio_features[count2],
            "classification": 2});
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

  classifySongs(function(song){
    getUserInput(song);
  });
}

function addSong(song, classification){
  var allSongs = JSON.parse(fs.readFileSync('allSongs.json', 'utf8'));
  songInlist = false;

  // update songs classification if it is not new
  for(i = 0; i < allSongs.songs.length; i++){
    if(allSongs.songs[i].key == song.token){
      allSongs.songs[i].classification = classification;
      songInlist = true;
      break;
    }
  }

  // add song to list if it is new
  if(songInlist == false){
    allSongs.songs.push({
      "key": song.token,
      "attributes": {
        "danceability": song.attributes.danceability,
        "energy": song.attributes.energy,
        "key": song.attributes.key,
        "loudness": song.attributes.loudness, 
        "mode": song.attributes.mode,
        "speechiness": song.attributes.speechiness,
        "acousticness": song.attributes.acousticness,
        "instrumentalness": song.attributes.instrumentalness,
        "liveness": song.attributes.liveness,
        "valence":song.attributes.valence,
        "tempo":song.attributes.tempo},
      "classification": classification});
  }
  // update the json file
  fs.writeFile("allSongs.json", JSON.stringify(allSongs), 'utf8', function (err) {
    if (err) {
      return console.log(err);
    }
  });
}

function getUserInput(song){
  // display song
  console.log(song);
  var userInput;
  // get users opinion on song
  input = readline.question("l,d,s,u: ");
  while(true){
    if (input == "l"){
      console.log("Liked");
      userInput = 0;
      break;
    } else if (input == "d"){
      console.log("Disliked");
      userInput = 1
      break;
    } else if (input == "s"){
      console.log("Skipped");
      userInput = 2;
      break
    } else if (input == "u"){
      console.log("Unsure");
      userInput = 3;
      break
    }
  }
  // update the song dataset with the new song & classification
  addSong(song, userInput)
}


function classifySongs(callback){
  //run python code to get the next song
  const classifySongs = spawn('python3', ['classifySongs.py', 'songs.json']);
  classifySongs.on('close', (code) => {
    //console.log(`child process exited with code ${code}`);
    var song = JSON.parse(fs.readFileSync('nextSong.json', 'utf8'));

    //send song to callback
    callback(song)
  })
}

function clusterSongs() { 
  const clusterSongs = spawn('python3', ['clusterSongs.py', 'allSongs.json']);
  clusterSongs.on('close', (code) => {
    //console.log(`child process exited with code ${code}`);
    var clusters = JSON.parse(fs.readFileSync('clusters.json', 'utf8'));
    getSongsFromSeed(clusters);
  });
  return new Promise(resolve => {
    setTimeout(() => {
      resolve("clusered songs");
    }, 2000);
  });
}

async function mainLoop() {
  var firstLoop = true;
  while(true){
    if(firstLoop == true){
      seedPlaylist('124632828', '6X2OFVuHppo7uZHPjfJitd');
      firstLoop = false;
    } else {
      var x = await clusterSongs();
      console.log(x);
    }
  }
}

// clear the previous data
allSongs = {}
fs.writeFile("allSongs.json", JSON.stringify(allSongs), 'utf8', function (err) {
  if (err) {
    return console.log(err);
  }
});

mainLoop();

var app = express();
app.use(express.static(__dirname));
//console.log('Listening on 8888');
//app.listen(8888);