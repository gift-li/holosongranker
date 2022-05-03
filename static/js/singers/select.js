$(document).ready(function () {
    if ("{{request.session.view_select}}" == "total_view") {
        $("#date_select").hide();
    } else {
        $("#date_select").show();
    }

    $("#view_select").change(function () {
        if ($(this).val() == "total_view") {
            $("#date_select").hide();
            $("#select_form").submit();
        } else {
            $("#date_select").show();
        }
    });
    $("#date_select").change(function () {
        if ($("#view_select").val() == "total_view_weekly_growth") {
            $("#select_form").submit();
        }
    });
});
