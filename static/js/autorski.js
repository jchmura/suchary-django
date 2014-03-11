function send_new() {
    var author = $('#author').text();
    var body = $('#new_joke').val();
    if (isBlank(body)) {
        $('#form-body').addClass('has-error');
    }
    else {
        $('#form-body').removeClass('has-error');
        $('#new_joke').attr('disabled', 'disabled');
        Dajaxice.autorski.send_new(Dajax.process, {'author': author, 'body': body});
    }
}
function disaply_form() {
    $(".create_new button").hide();
    $("#form").show();
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


function vote(pk, up) {
    Dajaxice.autorski.vote_joke(Dajax.process, {'pk': pk, 'up': up});
    return true;
}

function update_votes(pk, votes, up) {
    var div = $('#joke-' + pk);
    div.find(".badge").html('<b>' + votes + '</b>');
    var upvote = div.find("#up-" + pk);
    var downvote = div.find("#down-" + pk);
    if (up) {
        upvote.attr('disabled', 'disabled');
        upvote.removeClass('btn-default').addClass('btn-success');
        downvote.removeAttr('disabled');
        downvote.removeClass('btn-danger').addClass('btn-default');
    }
    else {
        downvote.attr('disabled', 'disabled');
        downvote.removeClass('btn-default').addClass('btn-danger');
        upvote.removeAttr('disabled');
        upvote.removeClass('btn-success').addClass('btn-default');
    }
}

function open_login() {
    setTimeout(function() {
        $("#login-dropdown").click()
    }, 200);
}