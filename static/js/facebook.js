window.fbAsyncInit = function () {
    FB.init({
        appId: '628784013845093',
        status: false,
        xfbml: false
    });
};

(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {
        return;
    }
    js = d.createElement(s);
    js.id = id;
    js.src = "//connect.facebook.net/pl_PL/all.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

$(document).ready(function () {
    //Handles menu drop down
    $('.dropdown-menu').find('form').click(function (e) {
        e.stopPropagation();
    });
});

function send_info(uid, accessToken, expiresIn, username) {
    $.post("/fb-login/", {'uid': uid, 'accessToken': accessToken, 'expiresIn': expiresIn, 'username': username},
        function () {
            window.location.reload(true);
        }
    );
}

function FB_login() {
    FB.getLoginStatus(function (response) {
        if (response.status === 'connected') {
            // the user is logged in and has authenticated your
            // app, and response.authResponse supplies
            // the user's ID, a valid access token, a signed
            // request, and the time the access token
            // and signed request each expire
            var uid = response.authResponse.userID;
            var accessToken = response.authResponse.accessToken;
            var expiresIn = response.authResponse.expiresIn;
            FB.api("/me", function (response) {
                send_info(uid, accessToken, expiresIn, response.username);
            });
        } else if (response.status === 'not_authorized') {
            FB.login(function (response) {
                return FB_login();
            });
        } else {
            FB.login(function (response) {
                return FB_login();
            });
        }
    });
}