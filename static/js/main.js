$(document).ready(function() {
	var updateInterval = 2 * 1000;

	updateApp();
	setInterval(function(){
		updateApp();
	}, updateInterval);


	$("#post-form").submit(function(e){
		e.preventDefault();
		var nowDate = moment().format("YYYY-MM-DD HH:mm:ss");
		var content = $("#post-new").val();
		newBlogPost("Surname Lastname", "username", nowDate, content);
		$("#post-new").val("");
	});
});

function updateApp() {
	updateTags();
	updateDates();
}

function newBlogPost(displayName, username, time, content) {
	var r = parseInt(Math.random() * 1000000, 10);
	var newPost = '<article post-id="' + r + '" class="blog-post"><header><a href="/profile/' + username + '" class="post-author" rel="author"><b>' + displayName + '</b> @' + username + '</a><time class="post-date" post-date="' + time + '"></time></header><p class="post-content">' + tags(content) + '</p></article>';
	$(".articles").prepend(newPost).slideDown('slow');
	dateMe($("[post-id='" + r + "'] .post-date"));
}

function updateDates() {
	$(".post-date").each(function(i, el) {
		dateMe(el);
	});
}

function updateTags() {
	$(".post-content").each(function(i, el){
		$(el).html(tags($(el).text()));
	});
}

function dateMe(obj) {
	var dateFormat = "YYYY-MM-DD HH:mm:ss";
	$(obj).text(moment($(obj).attr("post-date"), dateFormat).fromNow());
}

function tags(str) {
	return str.replace(/(^|\s)([#@][a-z\d-]+)/g, function(){ 
		var arg = arguments[2];
		var type = arg[0];
		var tag = arg.substring(1);
		var link = type=="@"?"profile":"tag";
		return " <a href='/" + link + "/" + tag + "'>" + arg + "</a>";
	});
}