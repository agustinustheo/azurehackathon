// Load the IFrame Player API code asynchronously.
function loadScript() {
    if (typeof(YT) == 'undefined' || typeof(YT.Player) == 'undefined') {
        var tag = document.createElement('script');
        tag.src = "https://www.youtube.com/player_api";
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    }
}

// Replace tlethe 'ytplayer' element with an <iframe> and
// YouTube player after the API code downloads.
var yt_id = document.getElementById("yt_id").value;
var player = new Array(8);
var playerConfig = new Array(8);
var playButton = new Array(8);
var containerName = new Array(8);
var startSecondsList = new Array(8);
var endSecondsList = new Array(8);
var count = 0;

function loadVideo(videoId, startSeconds, endSeconds, type, index){
    let ytPlayer = document.getElementById('ytplayer')
    let element = document.createElement('div');
    element.setAttribute("id", type+index);

    playButton[count] = document.createElement('input');
    playButton[count].setAttribute("type", "button");
    playButton[count].setAttribute("class", "judgeyou-play-button");
    playButton[count].setAttribute("value", "Play Video on 0.25x");

    startSecondsList[count] = startSeconds;
    endSecondsList[count] = endSeconds;
    containerName[count] = type + index;

    if(endSeconds - startSeconds > 0){
        ytPlayer.appendChild(element);
        ytPlayer.appendChild(playButton[count]);
    }

    window.onYouTubePlayerAPIReady = function(){
        for(let i = 0; i < count; i++){
            if(endSecondsList[i] - startSecondsList[i] > 0){
                playerConfig[i] = {
                    height: '300',
                    width: '480',
                    videoId: videoId,
                    playerVars: {
                        autoplay: 0, // Auto-play the video on load
                        controls: 0, // Show pause/play buttons in player
                        showinfo: 0, // Hide the video title
                        modestbranding: 1, // Hide the Youtube Logo
                        fs: 1, // Hide the full screen button
                        cc_load_policy: 0, // Hide closed captions
                        iv_load_policy: 3, // Hide the Video Annotations
                        start: startSecondsList[i],
                        end: endSecondsList[i],
                        loop: 0,
                        suggestedQuality: "small", // Loads a small quality video
                        autohide: 0, // Hide video controls when playing
                    },
                    events: {
                        'onStateChange': onStateChange
                    }
                };

                player[i] = new YT.Player(containerName[i], playerConfig[i]);

                playButton[i].onclick = function(){
                    player[i].mute()
                    player[i].setPlaybackRate(0.25)
                    player[i].loadVideoById({
                        videoId: videoId,
                        startSeconds: startSecondsList[i],
                        endSeconds: endSecondsList[i],
                        suggestedQuality: "small"
                    });
                }

                function onStateChange(state) {
                    if (state.data === YT.PlayerState.PLAYING) {
                        player[i].mute()
                        player[i].setPlaybackRate(0.25)
                    }
                }
            }
        }
    }
    count++;
}

axios.get('/getCommentary', {
    params:{
        id: yt_id
    }
})
.then(response => {
    loadScript();
    for (var x in response.data) {
        let container = document.createElement('div');
        container.setAttribute("class", "judgeyou-container");
        let element = document.createElement('div');
        element.setAttribute("class", "judgeyou-comment-box");
        let julie = document.createElement('img');
        julie.setAttribute("src", "/static/img/judgeyou%20mascot.png");
        if(x.includes('timestamp')){
            if(x.includes('micro')){
                if (response.data[x] != null) {
                    for(var key in response.data[x]){
                        loadVideo(
                            response.data.yt_id,
                            response.data[x][key.toString()]["start_time"], 
                            response.data[x][key.toString()]["end_time"],
                            x.toString().substring(0, x.indexOf("_timestamp")),
                            key
                        );
                        if(key == 3){
                            element.innerHTML = response.data[x.toString().substring(0, x.indexOf("_timestamp"))];
                            let createdDiv = document.getElementById(x.toString().substring(0, x.indexOf("_timestamp")).toString() + "1");
                            createdDiv.parentNode.appendChild(container);
                            container.appendChild(element);
                            element.parentNode.insertBefore(julie, element);
                        }
                    }
                }   
            }
            else{
                if (response.data[x] != null) {
                    loadVideo(
                        response.data.yt_id,
                        response.data[x]["start_time"], 
                        response.data[x]["end_time"],
                        x.toString().substring(0, x.indexOf("_timestamp")),
                        0
                    );
                    element.innerHTML = response.data[x.toString().substring(0, x.indexOf("_timestamp"))];
                    let createdDiv = document.getElementById(x.toString().substring(0, x.indexOf("_timestamp")).toString() + "0");
                    createdDiv.parentNode.appendChild(container);
                    container.appendChild(element);
                    element.parentNode.insertBefore(julie, element);
                }
            }
        } 
    }
})
.catch(ex => {
    alert('Error: check console for details');
    console.log(ex);
})