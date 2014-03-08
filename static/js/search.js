$(window).bind("resize", function () {
    fitInput();
});
//resize on window change

$(document).ready(function () {
    fitInput();
});
//resize after loading

function fitInput() {
    var divW = $(".search").width();
    var labelW = $("label[for='input']").width();
    $("input[type='text']").width(divW - labelW - 30);
}
//resize function