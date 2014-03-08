function reverse() {
    var pagePatt = new RegExp("&?page=[0-9]*");
    var search = location.search;
    var newSearch = search.replace(pagePatt, "");
    var patt = new RegExp("reversed=([a-zA-z0-9]*)");
    var result = patt.exec(location.search);
    if (result != null) {
        if (result[1] == 'true') {
            location.href = newSearch.replace(result[1], "false");
        }
        else if (result[1] != '') {
            location.href = newSearch.replace(result[1], "true");
        }
        else {
            location.href = newSearch.replace("reversed=", "reversed=true");
        }
    }
    else {
        var s = location.search.substring(0, 1);
        if (s == "?") {
            location.href = newSearch + "&reversed=true";
        }
        else {
            location.href = "?reversed=true";
        }
    }
}

function sort_by(by) {
    var patt = new RegExp("q=([a-zA-Z0-9]*\\+?)*");
    var result = patt.exec(location.search);
    if (result != null && result[0] != null) {
        location.href = "?" + result[0] + "&sort=" + by;
    }
    else {
        location.href = "?sort=" + by;
    }

}

function page(nr) {
    var patt = new RegExp("page=([0-9]+)");
    var result = patt.exec(location.search);
    if (result != null) {
        if (result[1] != '') {
            location.href = location.search.replace(result[1], nr);
        }
        else {
            location.href = location.search.replace("page=", "page=" + nr);
        }
    }
    else {
        var s = location.search.substring(0, 1);
        if (s == "?") {
            location.href = location.search + "&page=" + nr;
        }
        else {
            location.href = "?page=" + nr;
        }
    }
}