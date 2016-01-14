$(document).ready(function() {
	var updateInterval = 10 * 1000;

	updateApp();
	updateProfile();
	
	setInterval(function(){
		updateApp();
	}, updateInterval);

	$("#subscribe-btn").on("click", function(){
		subscribe(this);
	});

	initNewPost();
	initSearch();
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
		e.stopPropagation();
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
			},
			error: function(response){
				$(".post-add").html(response);
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

				if(myDropzone.getQueuedFiles().length > 0) {
					myDropzone.processQueue();
				} else {
					$("#submitPost").submit();
				}
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
	updatePosts();
	updateLinks();
	updateDates();
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

function updateProfile() {
	$(".user-description").html(urls($(".user-description").text()));
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

function initSearch() {
	var mblogSearch = new Bloodhound({
		datumTokenizer: Bloodhound.tokenizers.obj.whitespace('username'),
		queryTokenizer: Bloodhound.tokenizers.whitespace,
		remote: {
			url: '/search/%QUERY',
			wildcard: '%QUERY'
		}
	});

	$('.search .typeahead').typeahead(null, {
		name: 'mblog-search',
		display: 'username',
		minLength: 3,
		limit: 10,
		hightlight: true,
		source: mblogSearch,
		templates: {
			empty: [
				'<div class="empty-message">',
				'Unable to find any users that match the current query',
				'</div>'
			].join('\n'),
			suggestion: function(data){
				var isOne = data.profile__displayName.length<1?"one":"two";
				return '<a href="/profile/' + data.username + '" class="search-element"><img width="32px" height="32px" class="user-thumbnail" src="' + data.profile__profileImage + '" alt="' + data.profile__displayName + '"/><div class="user-info ' + isOne + '"><h5>' + data.profile__displayName + '</h5><span class="username">@' + data.username + '</span></div></a>';
			}
		}
	});
}

function editProfile(save, username) {
	var editUrl = "/profile/" + username + "/edit/";
	var method = save?"POST":"GET";
	var data = "";

	if(save) {
		data = $("#profile-edit").serializeArray();
	}

	$.ajax({
		url: editUrl,
		method: method,
		data: data,
		success: function(response){
			$(".profile-summery").html(response);
			updateProfile();
		},
		error: function(response) {
			console.log(response);
		}
	});
}

function updatePosts() {
	var lastUpdate = $(".articles .blog-post header .post-date").attr("data-post-date") || null;

	$.ajax({
		url: "/post/load/",
		method: "GET",
		data: {"lastUpdate": lastUpdate},
		success: function(response){
			$(".articles").prepend(response).slideDown('slow');;
		}
	});
}