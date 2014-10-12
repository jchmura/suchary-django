function delete_joke(app, pk) {
    var body = $("#joke-" + pk + " > .panel-body > p").text();
    var message = "Detele joke?\n\n" + body;
    if (confirm(message)) {
        if (app == 'obcy') {
            $.ajax({
                url: '/obcy/delete/' + pk,
                type: 'POST',
                success: function() {
                    deleted_joke(pk)
                },
                error: function(xhr, status, errorThrown) {
                    console.log("Error: " + errorThrown);
                    console.log("Status: " + status);
                }
            });
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
        $.ajax({
            url: '/obcy/edit/' + pk,
            type: 'POST',
            data: {
                body: body
            },
            success: function() {
                edited_joke(pk)
            },
            error: function(xhr, status, errorThrown) {
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
            }
        });
    }
}

function edited_joke(pk) {
    old_text = $("#joke-" + pk + " > .panel-body > textarea").val().replace(/\n/g, "<br>");
    edit_joke_off(pk)
}

function clean_joke(app, pk) {
    var panel = $("#joke-" + pk + " > div.panel-body");
    var paragraph = panel.children('p');
    var body = paragraph.html().replace(/<br>/g, '\n');
    if (app == 'obcy') {
        $.ajax({
            url: '/obcy/clean',
            type: 'GET',
            data: {
                body: body
            },
            success: function(data) {
                edit_joke_on(app, pk);
                var textArea = panel.children('textarea');
                textArea.val(data.cleaned);
            },
            error: function(xhr, status, errorThrown) {
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
            }
        });
    }
}

function verify_joke(app, pk) {
    if (app === 'obcy') {
        $.ajax({
            url: '/obcy/verify/' + pk,
            type: 'POST',
            success: function() {
                verified_joke(pk)
            },
            error: function(xhr, status, errorThrown) {
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
            }
        });
    }
}

function verified_joke(pk) {
    var panel = $('#joke-' + pk + ' > div.panel-heading');
    console.log(panel.find('.glyphicon-ok'));
    panel.find('.glyphicon-ok')
        .removeClass('glyphicon-ok')
        .addClass('glyphicon-remove')
        .attr('title', 'Unverify')
        .click(function() {
            unverify_joke('obcy', pk);
        });
}

function unverify_joke(app, pk) {
    if (app === 'obcy') {
        $.ajax({
            url: '/obcy/unverify/' + pk,
            type: 'POST',
            success: function() {
                unverified_joke(pk)
            },
            error: function(xhr, status, errorThrown) {
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
            }
        });
    }
}

function unverified_joke(pk) {
    var panel = $('#joke-' + pk + ' > div.panel-heading');
    panel.find('.glyphicon-remove')
        .removeClass('glyphicon-remove')
        .addClass('glyphicon-ok')
        .attr('title', 'Verify')
        .click(function() {
            verify_joke('obcy', pk);
        });
}