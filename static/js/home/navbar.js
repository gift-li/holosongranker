$(document).ready(function () {
    // sidebar按鈕點擊
    $(".navbar-toggler").click(function () {
        if ($("#sidebar").hasClass("d-none")) {
            $("#sidebar").removeClass("d-none");
        } else {
            $("#sidebar").addClass("d-none");
        }
    });

    $(window).resize(function () {
        // 若螢幕放大且sidebar隱藏 => 展開sidebar
        if ($(window).width() > 992 && $("#sidebar").hasClass("d-none")) {
            $("#sidebar").removeClass("d-none");
        }

        // 若螢幕最小且sidebar開啟 => 隱藏sidebar
        if ($(window).width() < 400 && !$("#sidebar").hasClass("d-none")) {
            $("#sidebar").addClass("d-none");
        }
    });
});
