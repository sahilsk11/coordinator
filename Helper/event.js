<!DOCTYPE HTML SYSTEM>
<html lang = "en">
	<head>
		<title>Coordinator - Event</title>
		<link href ="Helper/bootstrap.css" rel="stylesheet" type = "text/css">
		<link href ="Helper/organize.css" rel="stylesheet" type = "text/css">
		<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
		<link href="Helper/Images/icon.png" rel="icon">
		<link href = "https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet" type="text/css">
		<script src="Helper/jquery-2.2.4.min.js"></script>
		<script src="Helper/bootstrap.js"></script>
		<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyD9Cyy79DLP-pvlVVYB1rBCkZwNfojOhG0">
    		</script>
    	<script src="Helper/cookiesk.js"></script>
    	<script src="Helper/XHRequest.js"></script>
    	<script>

    		var users;
    		var my_data;
    		var map;
			var destination;
			var position_set = false;
			var lat = "";
			var lon = "";

			//list of methods:
			//deleteT()
			//update(lat, lon)
			//setWidth(number)


			//deletes event
			//related: none
    		function deleteT() {
    			var step = confirm("You are deleting the event.");
    			if (step == true) {
	    			function success1() {

	    			}
	    			XHRequest.createRequest({
	    				success: success1, 
	    				url: "/coordinator/scripts/datbase.py",
	    				params: {
	    					command: "delete"
	    				}
	    			});
	    		}
    		}

    		//updates the current user with lat and lon
    		//related : none
    		function update(lat, lon) {
				var user;
				user = getUserCookie();
    			function interpret(xhr, xhrConfig) {
    				var data = JSON.parse(xhr.responseText);
    				console.log(data);
    				if (data.complete == "Location") {
    					//location invalid
    				}
    				else if (data.complete == "True") {
    					return true;
    				}
    				else {
    					//destination invalid
    				}
    			}
    			console.log("update location");
    			XHRequest.createRequest({
					success: interpret, 
					url: "/coordinator/scripts/datbase.py",
					params: {
					command: "update",
					lat: lat,
					lon: lon,
					user: user
					}
    			});
    		}

    		//sets width of elements depending on how many there are
    		//related: showUsers
    		function setWidth(number) {
				var length = 12/number;
				if (length < 2) {
					length = 2;
				}
				return length;
				console.log(length);
			}

    		//displays all users and their information in the div
    		//related: check, success, setWidth
    		function showUsers() {
    			var titles = "";
    			for (var i = 0; i < users; i++) {
    				titles = titles + "<h3 class='text-center col-md-"+setWidth(users)+"'>" + my_data.people[i].name + "\'s time from destination: " + my_data.people[i].time + "</h3>";
    			}
    			document.getElementById("times").innerHTML = titles;
    		}

    		//success when "show" is called also displays interprets data and redirects
    		//related: check, showUsers
    		function success(xhr, xhrConfig) {
    			my_data = JSON.parse(xhr.responseText);
    			users = my_data.users;
    			var found = false;
    			for (var i = 0; i < users; i++) {
    				if (my_data.people[i].name == getUserCookie()) {
    					console.log("valid");
    					found = true;
    					showUsers();
    				}
    			}
    			if (found == false) {
    				setUserCookie("");
    				window.location = "createuser.html";
    			}
    			destination = {lat: my_data.destination.lat, lng: my_data.destination.lon};
    		}

    		//retrieves information and calls others to use it
    		//related: success, showUsers
    		function check() {
    			console.log("redirect");
    			XHRequest.createRequest({
				success: success, 
				url: "/coordinator/scripts/datbase.py",
				params: {
					command: "show"
				}
    			});
    		}

    		//detects browser and makes mobile site
    		//related: none
			function detectBrowser() {
				var useragent = navigator.userAgent;
				var mapdiv = document.getElementById("map");
				if (useragent.indexOf('iPhone') == -1 && useragent.indexOf('Android') == -1 ) {
			    	mapdiv.style.width = '100%';
			    	mapdiv.style.height = '50%';
			    	document.getElementById("show_map_button").innerHTML = "";
			    	document.getElementById("lead_image").innerHTML = "<img src='Helper/Images/co.png' class='page-logo'>\
						<hr width='65%' class='next-close'>";
			  	}
			  	else {
			  		function jump(controlDiv, map) {
						var controlUI = document.createElement('div');
				        controlUI.style.backgroundColor = '#fff';
				        controlUI.style.border = '2px solid #fff';
				        controlUI.style.borderRadius = '3px';
				        controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
				        controlUI.style.cursor = 'pointer';
				        controlUI.style.marginBottom = '22px';
				        controlUI.style.textAlign = 'center';
				        controlUI.title = 'Click to recenter the map';
				        controlDiv.appendChild(controlUI);
				        var controlText = document.createElement('div');
				        controlText.style.color = 'rgb(25,25,25)';
				        controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
				        controlText.style.fontSize = '16px';
				        controlText.style.lineHeight = '38px';
				        controlText.style.paddingLeft = '5px';
				        controlText.style.paddingRight = '5px';
				        controlText.innerHTML = 'Jump to Top';
				        controlUI.appendChild(controlText);
		        		controlUI.addEventListener('click', function() {
	          			window.location = "event.html#top";
	        			});
					}
			  		var jumpDiv = document.createElement('div');
		        	var centerControl = new jump(jumpDiv, map);
		        	jumpDiv.index = 1;
		        	map.controls[google.maps.ControlPosition.BOTTOM_LEFT].push(jumpDiv);
			  	}
			}

			//greets user with cookie
			//related: none
			function displayCookie() {
				var user = checkValidUser(getUserCookie());
				if (user != null) {
					console.log("user="+user);
					document.getElementById("user").innerHTML = "You are: " + user;
				}
				else {
					window.location = "createuser.html";
				}
			}

			//starts location
			//related: showPosition
			function showLocation () {
				if (navigator.geolocation) {
					navigator.geolocation.getCurrentPosition(showPosition);
				}
			}
			
			//sets lat and lon, and initializes map marker for location
			//related: showLocation
			function showPosition(position) {
				lat = position.coords.latitude;
				lon = position.coords.longitude;
				position_set = true;
				console.log("Location input");
				var current = new google.maps.Marker({
					animation: google.maps.Animation.DROP,
			  		position: {lat: lat, lng:lon},
			  		
			  		map: map,
			  		//animation: google.maps.Animation.DROP,
			  		title: 'Your position'
		  		});

			}

			//sets the map
			//related: none
			function start_map(destination) {
				map = new google.maps.Map(document.getElementById('map'), {
					center: destination,
					zoom: 10
				}); 
			}

			//creates marker for destination
			//related: none
			function show_destination() {
			  	var destination_icon = new google.maps.Marker({
			  		position: destination,
			  		icon: {
	      				path: google.maps.SymbolPath.CIRCLE,
	      				scale: 7
	   				},
			  		map: map,
			  		title: 'Destination'
			  	});
		  	}

		  	showLocation();
  	    	check();

			window.setInterval(function(){
		  		update(lat, lon);
		  		console.log("reload");
		  		showUsers();
		  		check();
		  		window.location.reload();
			}, 120000);
    		
    	</script>
	</head>
	<body class="static-nav">
		<a id="top"></a>
		<nav class="navbar-inverse">
			<div class="container-fluid">
				<div class="navbar-header">
					<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
			      		<span class="sr-only">Toggle navigation</span>
			      		<span class="icon-bar"></span>
			      		<span class="icon-bar"></span>
			      		<span class="icon-bar"></span>
		        	</button>
	    			<a href="index.html" class="navbar-brand">
	    				<img src="Helper/Images/co-grey.png" class="logo" onmouseover="this.src='Helper/Images/co-white.png'" onmouseout="this.src='Helper/Images/co-grey.png'">
	    			</a>
				</div>
	    		<div id="navbar" class="navbar-collapse collapse">
	    			<ul class="nav navbar-nav theme">
	      				<li class=""><a href="index.html">Home</a></li>
	      				<li class="active"><a href="newevent.html">Create a New Event</a></li>
	      				<li><a href="changeuser.html">Change Username</a></li>
	      				<li><a href="www.iotspace.tech">Back to IoT Space</a></li>
	      				<li><a href="https://www.github.com/sahilsk11/coordinator" target="_blank">GitHub Page</a></li>
	    			</ul>
	    		</div>
	 		</div>
		</nav>

		<div class="text-center" id="lead_image">
		</div>
		<!--AIzaSyD9Cyy79DLP-pvlVVYB1rBCkZwNfojOhG0>
		<!div class="size"
			<iframe width="100%" height="80%" frameborder="0" style="border:0" src="https://www.google.com/maps/embed/v1/place?q=place_id:ChIJEf1nWlY0joARpclcbmlnKdU&key=AIzaSyD9Cyy79DLP-pvlVVYB1rBCkZwNfojOhG0" allowfullscreen
			</iframe
		</div> -->
		<h5 id="user" class="col-offset-xs-1 col-xs-11">Hello, User<h5>
		<div id="times" class="col-xs-12">
			<!--<hr class="next" width="75%">-->
		</div>
		<hr class="next">

		<div class="header">
			<div class="action">
				<a class="custom-btn" href='#map' id="show_map_button"><button class="btn btn-default btn-sm">Jump to map</button>
				</a>

				<a class="custom-btn" href="http://maps.google.com/?daddr=37.321463,-121.947924" target="_blank" ><button id="start_directions" 
					class="btn btn-default btn-sm">Start Directions</button>
				</a>

				<a class="custom-btn" href="changeuser.html"><button id="change_username"
					class="btn btn-default btn-sm">Change Name</button>
				</a>

				<a class="custom-btn" href="changedestination.html"><button id="change_destination" class="btn btn-default btn-sm">Change Destination</button></a>

				<a class="custom-btn"><button class="btn btn-default btn-sm" onclick = "deleteT()">Del</button></a>
			</div>
		</div>

		<div class="location" id="map">
			hi
		</div>
		<script>
			//script here due to page loading
			displayCookie();
			start_map();
			show_destination();
			detectBrowser();
		 </script>
		
		<hr width="75%" class="next">
		


		<!--script type="text/javascript"
			var url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=37.291048|-121.777052";
			$.getJSON(url, function (json) {
				var time = json.results[0]["rows"][0]["elements"][0]["duration"]["text"];
			});
		</script> -->
	</body> 

</html>