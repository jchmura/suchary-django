function send_new(){
    var author = $('.create_new #author').val();
    var body = $('.create_new #new_joke').val();
    var error = false;
    if(isBlank(author)) {
        error = true;
        $('.create_new #author').css('background-color', 'lightcoral');
    }
    else {
        $('.create_new #author').css('background-color', '');
    }
    if(isBlank(body)) {
        error = true;
        $('.create_new #new_joke').css('background-color', 'lightcoral');
    }
    else {
        $('.create_new #new_joke').css('background-color', '');
    }
    if(!error) {
        Dajaxice.autorski.send_new(Dajax.process,{'author':author, 'body': body});
    }
}
function disaply_form() {
    $(".create_new button").hide();
    $(".form").show();
    $(".form").css("margin-bottom", "50px");
}
function set_new(author, date, id, body) {
    $(".form").hide();
    $(".new_joke").show();
    $(".new_joke #author").text(author);
    $(".new_joke #date").text(date);
    $(".new_joke a").attr("href", "autorski/" + id);
    $(".new_joke .joke_body p").text(body);
}
function isBlank(str) {
    return (!str || /^\s*$/.test(str));
}