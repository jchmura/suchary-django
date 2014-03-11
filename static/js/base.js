function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    }
});

function validate_signup() {
    var username_pattern = new RegExp("^[a-zA-Z0-9-_]+$");
    if (!username_pattern.test($("#exampleInputUsername").val())) {
        return false
    }

    var password1 = $("#exampleInputPassword").val();
    var password2 = $("#exampleInputPassword2").val();
    return password1 == password2;
}