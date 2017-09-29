const submit_registration_form = (function() {
    const $secret    = $('#secret');
    const $username  = $('#username');
    const $errors    = $('#errors');
    const $errors_ul = $('#errors ul');
    $('#registration').submit(function(e) {
        $.post('user', JSON.stringify({
            username: $username.val(),
            secret:   $secret.val()
        }))
        .then(function(success) {
            data = JSON.parse(success);
            $errors.hide();
            $errors_ul.html('');
            window.location.href = 'user_page?id=' + data.id;
        }, function(failure) {
            const response = JSON.parse(failure.response);
            $secret.val('');
            $errors_ul.html('');
            for (let i = 0; i < response.errors.length; i++) {
                const error = response.errors[i];
                $errors_ul.append('<li>' + error + '</li>');
            }
            $errors.show();
        });
        return false;
    });

    return this;
})();

const send_message_form = (function() {
    const $to_username   = $('#to_username');
    const $from_username = $('#from_username');
    const $message       = $('#message');
    const $errors        = $('#errors');
    const $errors_ul      = $('#errors ul');
    $('#message_form').submit(function(e) {
        $.post('notes', JSON.stringify({
            from_username: $from_username.val(),
            to_username:   $to_username.val(),
            note:          $message.val()
        }))
        .then(function(success) {
            data = JSON.parse(success);
            console.log(success);
            $errors_ul.html('');
            $errors.hide();
            $message.val('');
        }, function(failure) {
            const response = JSON.parse(failure.response);
            console.log(response);
            console.log(response.errors);
            $errors_ul.html('');
            for (let i = 0; i < response.errors.length; i++) {
                const error = response.errors[i];
                $errors_ul.append('<li>' + error + '</li>');
            }
            $errors.show();
        });
        return false;
    });

    return this;
})();
