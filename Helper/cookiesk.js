/*
Sets the cookie to the set value
@param cvalue the name of the cookie
*/
function setCookie(cvalue) {
    document.cookie = "name" + "=" + cvalue;
}

function getCookie() {
    var name = "name=";
        var ca = document.cookie.split(';');
        for(var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
}

function checkCookie() {
        var string = getCookie();
        if (string != "" || string == null) {
            return true;
        } else {
            return false;
        }
}