(function ($) {
    $(".dropdown .dropdown-menu #log-out").click(function (event) {
        $.ajax({
            url: "/",
            type: "POST",
            data: {'operation': 'logout'},

            success: function () {
                location.reload()
            }
        });
    })
})(jQuery)