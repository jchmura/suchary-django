function send_new(){
    var author = $('#author').val();
    var body = $('#new_joke').val();
    var error = false;
    if(isBlank(author)) {
        error = true;
        $('#form-author').addClass('has-error');
    }
    else {
        $('#form-author').removeClass('has-error');
    }
    if(isBlank(body)) {
        error = true;
        $('#form-body').addClass('has-error');
    }
    else {
        $('#form-body').removeClass('has-error');
    }
    if(!error) {
        Dajaxice.autorski.send_new(Dajax.process,{'author':author, 'body': body});
    }
}
function disaply_form() {
    $(".create_new button").hide();
    $(".form").show();
    $("#submit").show();
}
function set_new(author, date, pk, body) {
    $(".form").hide();
    $(".new-joke").show();
    $("#name").text(author);
    $("#date").text(date);
    $("#date").attr("href", "/autorski/" + pk);
    $("#body").html(body);
    $('#votes').html('<b>0</b>')
}
function isBlank(str) {
    return (!str || /^\s*$/.test(str));
}