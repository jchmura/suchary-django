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

var old_text;

function edit_joke_on(app, pk) {
    var paragraph = $("#joke-" + pk + " > .panel-body > p");
    old_text = paragraph.html();
    paragraph.replaceWith("<textarea class='edit'>" + paragraph.html().replace(/<br>/g, "\n").trim() + "</textarea>")
    var edit = $(".edit");
    edit.css({
        'width': '100%',
        'resize': 'none'
    });

    edit.elastic();
    var send_btn = "<button type='button' class='btn btn-default btn-sm btn-edit-joke pull-right' " +
        "onclick='send_edit(" + '"' + app + '"' + ", " + pk + ")'>Edytuj</button>";
    edit.after(send_btn);
}

function edit_joke_off(pk) {
    var textarea = $("#joke-" + pk + " > .panel-body > textarea");
    textarea.replaceWith("<p>" + old_text + "</p>");
    $(".btn-edit-joke").remove();
}

function edit_joke(app, pk) {
    var panel = $("#joke-" + pk + " > div.panel-body");
    if (panel.has("p").length) {
        edit_joke_on(app, pk);
    }
    else {
        edit_joke_off(pk);
    }
}

function send_edit(app, pk) {
    var textarea = $("#joke-" + pk + " > .panel-body > textarea");
    var body = textarea.val();
    textarea.attr('disabled', 'disabled');
    $("#joke-" + pk + " > .panel-body > button").hide();
    if (app == 'obcy') {
        Dajaxice.obcy.edit_joke(Dajax.process, {'pk': pk, 'body': body});
    }
}

function edited_joke(pk) {
    old_text = $("#joke-" + pk + " > .panel-body > textarea").val().replace(/\n/g, "<br>");
    edit_joke_off(pk)
}