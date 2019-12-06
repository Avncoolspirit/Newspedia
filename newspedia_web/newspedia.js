$(document).ready(function() {
	updateCards();
	setInterval(updateCards, 7120);
});

function updateCards()
{
	updateCurrentCard();
	updateRelatedCards();
}

var minutes = 0;
var currentId = "1";

function updateCurrentCard()
{
	updateVideo();
	var url = "http://18.223.188.119:5000/api/v1.0/get_recos/" + currentId + "/52/";
	console.log(url);
	var currentProgram = programs[currentId];
	var logo = currentProgram.logo;
	var programName = currentProgram.programName;
	$.ajax({
		url: url,
		dataType: 'json',
		async: false,
		success: function(json) {
			var keyword0 = json.keywords[0][0].toUpperCase();
			var keyword1 = json.keywords[1][0].toUpperCase();
			var keywords = json.keywords.slice(2);
			for (var i = 0; i < keywords.length; i++)
			{
				keywords[i] = keywords[i][0];
			}
			keywords = keywords.join(', ');
			minutes = json.time_elased;	
			var progress = Math.round(minutes / currentProgram.totalTime * 100);
			var cardCurrent = '<h5 class="card-header border-light"><img src="' + logo + '" height="25" /> ' + programName 
			+ '</h5><div class="card-body"><h6 class="card-title">Talking about<br/><br/> <span class="badge most-important-keyword">' 
			+ keyword0 + '</span>&nbsp;&nbsp;<span class="badge most-important-keyword">' 
			+ keyword1 + '</span></h6><p class="card-text" style="font-size:120%;">Keywords: ' + keywords 
			+ '</p><div class="progress"><div class="progress-bar" role="progressbar" style="width: ' + progress 
			+ '%" aria-valuenow="' + progress.toString() + '" aria-valuemin="0" aria-valuemax="100">' + minutes.toString() + ' minutes</div></div></div>';
			$('#currently-watching').html(cardCurrent);
		}});
}

function updateVideo()
{
	$.ajax({
		url: 'http://18.223.188.119:5000/api/v1.0/get_video_id/',
		dataType: 'json',
		async: false,
		success: function(json) {
			currentId = json.current_videoid;
		}});
}

function updateRelatedCards()
{
	var cardRelated = '';
	for (var i = 0; i < allPrograms.length; i++) {
		if (String(currentId) === allPrograms[i])
		{
			continue;
		}
		var relatedId = allPrograms[i];
		var url = "http://18.223.188.119:5000/api/v1.0/get_recos/" + relatedId + "/52/";
		var relatedProgram = programs[relatedId];
		var logo = relatedProgram.logo;
		var programName = relatedProgram.programName;
		$.ajax({
			url: url,
			dataType: 'json',
			async: false,
			success: function(json) {
				var keyword0 = json.keywords[0][0].toUpperCase();
				var keyword1 = json.keywords[1][0].toUpperCase();
				var keywords = json.keywords.slice(2);
				for (j = 0; j < keywords.length; j++)
				{
					keywords[j] = keywords[j][0];
				}
				keywords = keywords.join(', ');
				cardRelated += '<div class="card border-light"><h5 class="card-header border-light"><img src="' + logo + '" height="25" /> ' + programName 
				+ '</h5><div class="card-body"><h6 class="card-title">Talking about<br/><br/> <span class="badge most-important-keyword">' 
			+ keyword0 + '</span>&nbsp;&nbsp;<span class="badge most-important-keyword">' 
			+ keyword1 + '</span></h6><p class="card-text" style="font-size:120%;">Keywords: ' + keywords 
			+ '</p><a href="#" class="btn btn-play text-light" id="btn-' 
				+ relatedId.toString() + '" onClick="play(this.id)">Play on TV</a></div></div>';
			}});
	}
	$('#related-news').html(cardRelated);
}

function play(id)
{
	var newId = id.split('-')[1];
	var url = 'http://18.223.188.119:5000/api/v1.0/update_time/' + newId + '/' + minutes.toString() + '/';
	console.log(url);
	$.get(url);
}