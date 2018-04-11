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

// credentials are optional
var spotifyApi = new SpotifyWebApi({
  clientId : 'c0f7fcc3fc594f4d9386be861bbc4770',
  clientSecret : '2be1642fdb974830b848db3156441c91',
  redirectUri : 'http://localhost:8888/callback'
});

spotifyApi.clientCredentialsGrant()
  .then(token => {
    spotifyApi.setAccessToken(token.body.access_token);
    return spotifyApi.getPlaylistTracks('124632828', '5WFfUARNKNylRTkJexElzb');
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
<<<<<<< HEAD
      console.log("The file was saved!");
    });
  })
  .catch(err => {
    console.log('error! ' + err);
  });
=======
  });
  
}

var jsonData = {
  "song": []
}

function getFile(callback){
  getPlaylistTracks('124632828', '6X2OFVuHppo7uZHPjfJitd', function(data){
    var itemsRemaining = data.body.total;
    for(var i=0; i<data.body.total; i++){
      //var variables = jsonData;
      getAudioFeaturesForTrack(data.body.items[i].track.id,function(data){ 
        itemsRemaining--;
        jsonData.song[itemsRemaining] = data.body;
        //console.log(jsonData);
        if(itemsRemaining == 0){
          callback(jsonData);
        }
      });
    }
  });
}

getFile(function(data){
  console.log(data);
});
>>>>>>> 080bbef6f86e5b37292111a13ca3bdf76e9ca6e2




var app = express();
app.use(express.static(__dirname));
console.log('Listening on 8888');
app.listen(8888);