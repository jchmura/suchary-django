function delete_joke(app, pk) {
    var body = $("#joke-" + pk + " > .panel-body > p").text();
    var message = "Detele joke?\n\n" + body;
    if (confirm(message)) {
        if (app == 'obcy') {
            Dajaxice.obcy.delete_joke(Dajax.process, {'pk': pk});
        }
    }

}

function deleted_joke(pk) {
    $("#joke-" + pk).hide();
}