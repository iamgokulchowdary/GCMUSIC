$(document).ready(function() {
    $('#followunfollowbtn').on('click', function() {
        var button = $(this);
        var artistId = $(this).data('artistid');
        var csrftoken = $('input[name="csrftoken"]').val();
        var followerscount = $('#followerscount');
        

        $.ajax({
            url: '/artist/' + artistId + '/follow/',
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            success: function(data) {
                if (data.status === 'ok') {
                    if (data.action === 'followed') {
                        button.text('UnFollow');
                        button.data('action', 'unfollow');
                        followerscount.text(data.followerscount);
                    } else {
                        button.text('Follow');
                        button.data('action', 'follow');
                        followerscount.text(data.followerscount);
                    }
                }
                
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });
});
