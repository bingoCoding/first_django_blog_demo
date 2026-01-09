(function($) {
    debugger
    const $content_md = $(".form-row .field-content_md");
    const $content_ck = $(".form-row .field-content_ck");
    const $is_md = $('input[name=is_md]');

    const switch_editor = function (is_md) {
        if (is_md) {
            console.info("switch to markdown", is_md)
            console.info("value", $content_md.text())
            $content_md.show();
            $content_ck.hide();
        } else {
            console.info("switch to markdown", is_md)
            console.info("value", $content_ck.text())
            $content_md.hide();
            $content_ck.show();
        }
    };
    $is_md.on('click', function () {
        switch_editor($is_md.is(':checked'));
    });
    switch_editor($is_md.is(':checked'));
})(jQuery);
