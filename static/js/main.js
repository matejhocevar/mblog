$(document).ready(function() {
	var updateInterval = 2 * 1000;

	updateAllDates();
	setInterval(function(){
		updateAllDates();
	}, updateInterval);


	$("#post-form").submit(function(e){
		e.preventDefault();
		var nowDate = moment().format("YYYY-MM-DD HH:mm:ss");
		var content = $("#post-new").val();
		newBlogPost("Surname Lastname", "username", nowDate, content);
		$("#post-new").val("");
	});
});

function dateMe(obj) {
	var dateFormat = "YYYY-MM-DD HH:mm:ss";
	$(obj).text(moment($(obj).attr("post-date"), dateFormat).fromNow());
}

function newBlogPost(displayName, username, time, content) {
	var r = parseInt(Math.random() * 1000000, 10);
	var newPost = '<article post-id="' + r + '" class="blog-post"><header><a href="/profile/' + username + '" class="post-author" rel="author"><b>' + displayName + '</b> @' + username + '</a><time class="post-date" post-date="' + time + '"></time></header><p class="post-content">' + content + '</p></article>';
	$(".articles").prepend(newPost).slideDown('slow');
	dateMe($("[post-id='" + r + "'] .post-date"));
}

function updateAllDates() {
	$(".post-date").each(function(i, el) {
		dateMe(el);
	});
}