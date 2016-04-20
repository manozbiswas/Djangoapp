//$(function () {
//    setNavigation();
//});
//
//function setNavigation() {
//    var path = window.location.pathname;
//    path = path.replace(/\/$/, "");
//    path = decodeURIComponent(path);
//    console.log(path)
//    $(".nav a").each(function () {
//        var href = $(this).attr('href');
//        if (path.substring(0, href.length) === href) {
//            $(this).closest('li').addClass('active');
//        }
//    });
//}

//jQuery(document).ready(function($){
//  // Get current path and find target link
//  var path = window.location.pathname.split("/").pop();
//  console.log(path);
//  // Account for home page with empty path
//  if ( path == '' ) {
//    path = 'mysite';
//  }
//
//  var target = $('nav a[href="'+path+'"]');
//  // Add active class to target link
//  target.addClass('active');
//});

//$(function() {
//  $('nav a[href^="/' + location.pathname.split("/")[1] + '"]').addClass('active');
//});