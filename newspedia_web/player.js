const player = new Plyr('#player');
player.muted = true;
player.play();
player.once('canplay', event => {
   player.currentTime = 240;
   updateTime();
   setInterval(updateVideo, 3000);
});

var currentVideo = "1";

function updateTime() {
    var url = 'http://18.223.188.119:5000/api/v1.0/update_time/' + currentVideo + '/' + Math.round(player.currentTime / 60).toString() + '/';
    $.get(url);    
}

function updateVideo() {
    console.log('hi');
    $.ajax({
        url: 'http://18.223.188.119:5000/api/v1.0/get_video_id/',
        dataType: 'json',
        async: false,
        success: function(json) {
            console.log(json);
            var newVideo = json.current_videoid;
            console.log(newVideo);
            if (newVideo !== currentVideo)
            {
                currentVideo = newVideo;
                changeSource(currentVideo);
            }
            updateTime();
        }});
}

function changeSource(programId) {
    console.log(programId);
	$('#status').removeClass('badge-secondary').addClass('badge-success');
    $("#status").text("Channel Change Request: Received for " + programs[programId].channel);

    var currentTime = player.currentTime;
    console.log(currentTime);
    player.source = {
        type: 'video',
        sources: [
        {
            src: programs[programId].video,
            type: 'video/mp4',
        }
        ]};
        player.pause();
        setTimeout(function() {player.currentTime = currentTime}, 800);
        player.play();
        setTimeout(function() {
           $('#status').removeClass('badge-success').addClass('badge-secondary');
           $("#status").text("Currently watching: " + programs[programId].channel); 
       }, 4000);
    }

