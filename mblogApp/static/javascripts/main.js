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
		var locationHtml = parseLocation(getLocation());
		newBlogPost("Matej Hočevar", "matox", nowDate, locationHtml, content);
		$("#post-new").val("");
		// TODO: when post you need to scroll to top, so user can see their post being published
	});

	initDropzone();
	infinityScroll();
});


$(window).resize(function(){
	$(".navigation").appendTo(".header-inner");
});

$(window).scroll(function () {
	if ($(window).scrollTop() >= $(document).height() - $(window).height() - 5) {
		infinityScroll();
	}
});

function parseLocation(location) {
	if(location.country !== null) {
		var town = '';
		if(location.town !== null) {
			town = location.town + ', ';
		}
		
		return '<span class="location-icon icon-LocationMarker"></span>' + town + location.country;
	}
	else return '';
}

function savePosition(position) {
    localStorage.setItem("location_latitude", position.coords.latitude);
    localStorage.setItem("location_longitude", position.coords.longitude);
}

function getLocation() {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(savePosition);
	}
	else {
		console.log("Geolocation is not supported by this browser.");
	}

	reverseLocation();

	var town = localStorage.getItem("location_town") !== "undefined"?localStorage.getItem("location_town"):null;
	var country = localStorage.getItem("location_country") !== "undefined"?localStorage.getItem("location_country"):null;
	
	return {"town":town, "country":country};
}

function reverseLocation() {
	var latitude = localStorage.getItem("location_latitude");
	var longitude = localStorage.getItem("location_longitude");

	$.get("http://nominatim.openstreetmap.org/reverse", {format:"json", lat:latitude, lon:longitude},
		function (response) {
			var town = '';
			if(response.address) {
				town = response.address.town;
			}

			var country = '';
			if(response.address) {
				country = response.address.country;
			}

			localStorage.setItem("location_town", town?town:"undefined");
			localStorage.setItem("location_country", country?country:"undefined");
		},
		"json"
	);
}

function initDropzone() {
	Dropzone.options.postForm = {
		autoProcessQueue: false,
		uploadMultiple: false,

		init: function() {
			var myDropzone = this;

			this.element.querySelector("#submitPost").addEventListener("click", function(e) {
				// e.preventDefault();
				// e.stopPropagation();
				// myDropzone.processQueue();
				myDropzone.removeAllFiles();
			});
		}
	};
}

function infinityScroll() {
	if($(".infinity-scroll").hasClass("none")) {
		$(".infinity-scroll").toggleClass("none");
	}

	setTimeout(function() {
		$.ajax({
			url: "/post/load",
			method: "GET",
			dataType: "html",
			success: function(response){
				$(".infinity-scroll").remove();
				$(".articles").append(response);
				$(".infinity-scroll").toggleClass("none");
			}
		});
	}, 3000);
}

function updateApp() {
	updateLinks();
	updateDates();
}

function newBlogPost(displayName, username, time, location, content) {
	var r = parseInt(Math.random() * 1000000, 10);
	var newPost = '<article post-id="' + r + '" class="blog-post"><header><img class="profile-img" src="/assets/images/sample/mtx_50x50.jpg"><a href="/profile/' + username + '" class="post-author" rel="author"><h5><b>' + displayName + '</b> @' + username + '</h5></a><div class="post-date" data-post-date="' + time + '"></div><div class="post-location">' + location + '</div></header><p class="post-content">' + urls(content) + '</p></article>';
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
	$(obj).text(moment($(obj).attr("data-post-date"), dateFormat).fromNow());
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