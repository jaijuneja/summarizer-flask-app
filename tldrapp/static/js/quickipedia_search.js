$(function scrollToElement() {
    var el_summary = "#search-results";
    if ($(el_summary).length) {
        $('html, body').animate({
            scrollTop: $(el_summary).offset().top
        }, 1000);
    }
});