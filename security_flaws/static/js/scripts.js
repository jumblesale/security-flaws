const submit_registration_form = (function() {
    const $secret   = $('#secret');
    const $username = $('#username');
    const $errors   = $('#errors');
    $('#registration').submit(function(e) {
        $.post('user', JSON.stringify({
            username: $username.val(),
            secret:   $secret.val()
        }))
        .then(function(success) {
            data = JSON.parse(success);
            console.log(success);
            $errors.hide();
            window.location.href = 'user_page.html?id=' + data.id
        }, function(failure) {
            const response = JSON.parse(failure.response);
            console.log(response);
            console.log(response.errors);
            $secret.val('');
            const errors_ul = $('#errors ul');
            errors_ul.html('');
            for (let i = 0; i < response.errors.length; i++) {
                const error = response.errors[i];
                errors_ul.append('<li>' + error + '</li>');
            }
            $errors.show();
        });
        return false;
    });

    return this;
})();
