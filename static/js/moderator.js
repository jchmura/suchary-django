$.fn.multiline = function (text) {
    this.text(text);
    this.html(this.html().replace(/\n/g, '<br/>'));
    return this;
};

$('#deleteModal').on('shown.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var pk = button.data('pk');
    var paragraph = $("#joke-" + pk + " > .panel-body > p");
    var jokeBody = paragraph.html();
    var modalJokeBody = $('#modal-joke-body');
    modalJokeBody.html(jokeBody);
    var duplicateBody = $('#modal-duplicate-joke-body');
    duplicateBody.css('display', 'none');
    $('#confirm-joke-delete').data('pk', pk);
    $('#confirm-joke-duplicate').data('pk', pk);
});

function delete_joke(pk) {
    $.ajax({
        url: '/obcy/delete/' + pk,
        type: 'POST',
        success: function () {
            deleted_joke(pk)
        },
        error: function (xhr, status, errorThrown) {
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
        }
    });

}

function deleted_joke(pk) {
    $("#joke-" + pk).hide();
    $('#deleteModal').modal('hide');
}

$(document).ready(function () {
    $('#duplicate-form').submit(function (event) {
        get_duplicate();
        event.preventDefault();
    });
    $('#confirm-joke-delete').click(function () {
        var pk = $(this).data('pk');
        delete_joke(pk);
    });
    $('#confirm-joke-duplicate').click(function () {
        var pk = $(this).data('pk');
        set_duplicate(pk);
    });
});

function get_duplicate() {
    var key = $('#duplicateKey').val();
    $.getJSON('/api/obcy/' + key, function (data) {
        var duplicateBody = $('#modal-duplicate-joke-body');
        duplicateBody.multiline(data.body);
        duplicateBody.css('display', 'inherit');
    });
}

function set_duplicate(pk) {
    var key = $('#duplicateKey').val();
    $.ajax({
        url: '/obcy/duplicate/' + pk + '/' + key,
        type: 'POST',
        success: function () {
            deleted_joke(pk)
        },
        error: function (xhr, status, errorThrown) {
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
        }
    });
}

var old_text;

function edit_joke_on(pk) {
    var paragraph = $("#joke-" + pk + " > .panel-body > p");
    old_text = paragraph.html();
    paragraph.replaceWith("<textarea class='edit'>" + paragraph.html().replace(/<br>/g, "\n").trim() + "</textarea>");
    var edit = $(".edit");
    edit.css({
        'width': '100%',
        'resize': 'none'
    });

    edit.elastic();
    var send_btn = "<button type='button' class='btn btn-default btn-sm btn-edit-joke pull-right' " +
        "onclick='send_edit(" + pk + ")'>Edytuj</button>";
    edit.after(send_btn);
}

function edit_joke_off(pk) {
    var textarea = $("#joke-" + pk + " > .panel-body > textarea");
    textarea.replaceWith("<p>" + old_text + "</p>");
    $(".btn-edit-joke").remove();
    $('.versions-selector').remove();
}

function edit_joke(pk) {
    var panel = $("#joke-" + pk + " > div.panel-body");
    if (panel.has("p").length) {
        edit_joke_on(pk);
        get_revisions(pk);
    }
    else {
        edit_joke_off(pk);
    }
}

//noinspection JSUnusedGlobalSymbols
function send_edit(pk) {
    var textarea = $("#joke-" + pk + " > .panel-body > textarea");
    var body = textarea.val();
    textarea.attr('disabled', 'disabled');
    $("#joke-" + pk + " > .panel-body > button").hide();
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

function edited_joke(pk) {
    var text = $("#joke-" + pk + " > .panel-body > textarea").val();
    var escaped = $('<div/>').text(text).html();
    old_text = escaped.replace(/\n/g, "<br>");
    edit_joke_off(pk)
}

function clean_joke(pk) {
    var panel = $("#joke-" + pk + " > div.panel-body");
    var paragraph = panel.children('p');
    var body = paragraph.html().replace(/<br>/g, '\n');
    $.ajax({
        url: '/obcy/clean',
        type: 'GET',
        data: {
            body: body
        },
        success: function(data) {
            edit_joke_on(pk);
            var textArea = panel.children('textarea');
            textArea.val(data.cleaned);
        },
        error: function(xhr, status, errorThrown) {
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
        }
    });
}

function verify_joke(pk) {
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

function verified_joke(pk) {
    var panel = $('#joke-' + pk + ' > div.panel-heading');
    panel.find('.glyphicon-exclamation-sign')
        .removeClass('glyphicon-exclamation-sign')
        .addClass('glyphicon-ok')
        .attr('title', 'Unverify');
}

function showVersions(pk, versions) {
    var body = $('#joke-' + pk + ' > div.panel-body');
    var textarea = body.children('textarea');
    $('<select class="selectpicker versions-selector" data-style="btn-xs pull-left"/>').insertAfter(textarea);
    var select = $('.selectpicker');

    versions.forEach(function(version) {
        $('<option/>', {
            value: version.body,
            text: version.date.toLocaleDateString() + ' ' + version.date.toLocaleTimeString()
        }).appendTo(select);
    });

    select.selectpicker();
    if( /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
        select.selectpicker('mobile');
    }


    select.change(function() {
        var textarea = $("#joke-" + pk + " > .panel-body > textarea");
        textarea.val(this.value);
        textarea.trigger('change');
    });
}
function get_revisions(pk) {
    $.getJSON('/obcy/revisions/' + pk, function(data) {
        var versions = [];
        data.forEach(function(version) {
            versions.push({date: new Date(version.date), body: version.body})
        });
        showVersions(pk, versions);
    });
}