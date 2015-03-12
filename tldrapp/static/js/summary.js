// Settings for summary toggle button
var menu_elements = document.querySelectorAll('.summary-buttons button'),
    menu_length = menu_elements.length;
for (var i = 0; i < menu_length; i++) {
    menu_elements[i].addEventListener('click', function (e) {
        var target_button = e.target.closest('button');
        var target = document.querySelector('.summary-container>.' + target_button.classList[0]); // clicked element
        Array.prototype.filter.call(target.parentNode.children, function (siblings) {
            siblings.style.display = 'none'; // hide sibling elements
        });
        target.style.display = 'block'; // show clicked element
    });
}

$(".summary-buttons button").click(function(){
    // Note that the parent().siblings().children() chain is required because each
    // button is contained in a div
    $(this).addClass("active").parent().siblings().children().removeClass("active");
});

$(function scrollToElement() {
    var el_summary = "#summary";
    if ($(el_summary).length) {
        $('html, body').animate({
            scrollTop: $(el_summary).offset().top
        }, 1000);
    }
});