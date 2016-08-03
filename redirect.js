if (window.location.href.indexOf("www") < 0 || window.location.href.indexOf("https") < 0) {
	if (window.location.href.indexOf("iot") < 0) {
		if (window.location.href.indexOf("local") < 0) {
			var start = window.location.href.indexOf("iot");
		}
		else {
			var start = window.location.href.indexOf("local");
		}
	}
	else {
		var start = window.location.href.indexOf("iot");
	}
	window.location = "https://www." + window.location.href.substring(start);
}