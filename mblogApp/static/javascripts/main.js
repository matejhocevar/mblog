$(document).ready(function() {
	var updateInterval = 2 * 1000;

	updateApp();
	setInterval(function(){
		updateApp();
	}, updateInterval);

	$("#subscribe-btn").on("click", function(){
		subscribe(this);
	});

	initNewPost();
});
$(window).resize(function(){
	$(".navigation").appendTo(".header-inner");
});


$(window).scroll(function () {
	if ($(window).scrollTop() >= $(document).height() - $(window).height() - 5) {
		infinityScroll();
	}
});

function subscribe(obj) {
	var type = "subscribe";
	var next = "Unsubscribe";

	if($(obj).val() == "Subscribe") {
		type = "subscribe";
		next = "Unsubscribe";
	}
	else if($(obj).val() == "Unsubscribe") {
		type = "unsubscribe";
		next = "Subscribe";
	}

	var user = $(".profile-summery .username").text().split("@")[1] || "null";

	$.ajax({
		url: /profile/ + user + "/" + type,
		method: "GET",
		success: function(response){
			$(".subscribers").html(response).fadeIn();

			$.ajax({
				url: /profile/ + user + "/info",
				method: "GET",
				success: function(response){
					$(".profile-summery").html(response).fadeIn();
					$("#subscribe-btn").on("click", function(){
						subscribe(this);
					});
				}
			});
		}
	});
}

function initNewPost() {
	initDropzone();

	$("#post-form").submit(function(e){
		e.preventDefault();
		parseLocation(getLocation());

		var data = new FormData($('#post-form').get(0));

		$.ajax({
			type:"POST",
			url: "/post/add/",
			data : data,
			cache: false,
			contentType: false,
			processData: false,
			success: function(response){
				$(".post-add").html(response);
				myDropzone.removeAllFiles();
			},
			error: function(response){
				$(".post-add").html(response);
				myDropzone.removeAllFiles();
			}
		});


	});
}

function parseLocation(location) {
	var town = '';
	var country = '';
	if(location.country !== null) {
		country = location.country;
		if(location.town !== null) {
			town = location.town;
		}
	}

	$("#post-form #id_town").val(town);
	$("#post-form #id_country").val(country);

	return;
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
				e.preventDefault();
				e.stopPropagation();
				myDropzone.processQueue();
				//myDropzone.removeAllFiles();
			});

			this.on("success", function(files, response){
				$(".post-add").html(response);
				myDropzone.removeAllFiles();
				initNewPost();
			});

			this.on("error", function(files, response){
				$(".post-add").html(response);
				myDropzone.removeAllFiles();
				initNewPost();
			});
		}
	};
}

function infinityScroll() {
	var nextPage = $(".infinity-next").attr("href");
	if(nextPage != null) {
		if($(".infinity-scroll").hasClass("none")) {
			$(".infinity-scroll").toggleClass("none");
		}

		$(".pagination").remove();

		$.ajax({
			url: nextPage,
			method: "GET",
			dataType: "html",
			success: function(response){
				$(".infinity-scroll").remove();
				$(".articles").append(response);
				$(".pagination").toggleClass("none");
			}
		});
	}
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
					return '<a href="/tag/' + hashtag + '">#' + hashtag + '</a>';
			}
		},
		truncate: 25,
		hashtag: 'twitter'
	});
}