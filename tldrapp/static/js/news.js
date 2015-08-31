$('.js-infinite-layout').infinitescroll({
    itemSelector: '.js-infinite-item',
    nextSelector: "div.js-infinite-navigation a:first",
    navSelector: "div.js-infinite-navigation",
    loading: {
        finishedMsg: "That's all, folks!"
    }
},
function()
{
    // Callback when new content is loaded from infinite scroll
    readMore();
}
);

readMore = function() {
    $('.readMore').click(function(){
        $(this).parent().siblings().removeClass('hidden');
        $(this).siblings().removeClass('hidden');
        $(this).addClass('hidden');
    });

    $('.readLess').click(function(){
        $(this).parent().siblings().addClass('hidden');
        $(this).siblings().removeClass('hidden');
        $(this).addClass('hidden');
    });
};