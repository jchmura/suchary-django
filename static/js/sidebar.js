function scale_sidebar(){
	var window_height = $(window).height();
	var height = $(".sidebar").height();
	var margin = $("#jokes").offset().left;
	var top_margin = (window_height - height)/2
	// alert(margin);
	var sidebar = $(".sidebar");
	sidebar.css({'height': height, 'visibility': 'visible', 'max-width': margin/2, 'top': top_margin});
	// sidebar.css({'visibility': 'visible'});

}

// $('.sidebar').hover(function() {
//     $(this).animate({
//         height: '300px'
//     }, 300);
// },function() {
//     $(this).animate({
//         height: '30px'
//     }, 300);
// });

$(".vertical_table").each(function(){$(this).height($(this).width())})