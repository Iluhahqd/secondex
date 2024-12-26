function del_from_fav(n, user) {
    $.ajax({
        url: '/del_from_fav_ajax/',
        data: {'id': n, 'user_id': user},
        success : function(json) {
            $("#request-access").hide();
            location.reload();
        }
    });
};