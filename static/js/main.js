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

	initScrollbar();
});

$(document).resize(function(){
	adjustHeight();
});

$(".articles").scroll(function(e) {
	if ($(".articles").scrollTop() === $(".articles").prop('scrollHeight') - $(".articles").height()) {
		$(".infinity-scroll").removeClass("none");
		console.log("Infinity scroll...");
	}
});

function initScrollbar() {
	var $container = $(".articles");

	adjustHeight();
	$container.perfectScrollbar();
}

function adjustHeight() {
	var $container = $(".articles");
	$container.height(screen.height - $(".header").outerHeight() - $(".post-add").outerHeight() - $("footer").outerHeight() - 100);
	$container.perfectScrollbar("update");
}

function updateApp() {
	updateLinks();
	updateDates();
}

function newBlogPost(displayName, username, time, content) {
	var r = parseInt(Math.random() * 1000000, 10);
	var newPost = '<article post-id="' + r + '" class="blog-post"><header><img class="profile-img" src="http://www.nicenicejpg.com/50"><a href="/profile/' + username + '" class="post-author" rel="author"><b>' + displayName + '</b> @' + username + '</a><time class="post-date" post-date="' + time + '"></time></header><p class="post-content">' + urls(content) + '</p></article>';
	$(".articles").prepend(newPost).slideDown('slow');
	dateMe($("[post-id='" + r + "'] .post-date"));
}

function updateDates() {
	$(".post-date").each(function(i, el) {
		dateMe(el);
	});
}

function dateMe(obj) {
	var dateFormat = "YYYY-MM-DD HH:mm:ss";
	$(obj).text(moment($(obj).attr("post-date"), dateFormat).fromNow());
}

function updateLinks() {
	$(".post-content").each(function(i, el){
		$(el).html(urls($(el).text()));
	});
}

function urls(str) {
	return Autolinker.link( str, {
		replaceFn : function( autolinker, match ) {
			switch( match.getType() ) {
				case 'twitter' :
					var userHandle = match.getTwitterHandle();

					return '<a href="/profile/' + userHandle + '">@' + userHandle + '</a>';

				case 'hashtag' :
					var hashtag = match.getHashtag();
					return '<a href="/tags/' + hashtag + '">#' + hashtag + '</a>';
			}
		},
		truncate: 25,
		hashtag: 'twitter'
	});
}