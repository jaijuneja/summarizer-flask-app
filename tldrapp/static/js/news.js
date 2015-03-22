// Resize news images appropriately for circular display
$(".news-image img").each(function() {
    $(this).on("load", function() {
        var img_height = $(this).get(0).naturalHeight;
        var img_width = $(this).get(0).naturalWidth;

        if (img_height > img_width) {
            $(this).parent().addClass('news-image-portrait');
        } else {
            $(this).parent().addClass('news-image-landscape');
        }
    })
});