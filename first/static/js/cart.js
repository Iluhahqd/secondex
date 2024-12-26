function del_from_cart(n, user) {
    $.ajax({
        url: '/del_from_cart_ajax/',
        data: {'id': n, 'user_id': user},
        success : function(json) {
            $("#request-access").hide();
            location.reload();
        }
    });
};