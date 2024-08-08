$(document).ready(function() {

    $('.deletesong').on('click', function(e){
        e.preventDefault();

        var songid = $(this).data('songid');
        var playlistid = $(this).data('playlistid');
        var csrftoken = $('input[name="csrftoken"]').val();

        $.ajax({
            type: 'POST',
            url: '/deletesongfromplaylist/',
            data: {
                'songid': songid,
                'playlistid': playlistid,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(response) {
                if(response.status === 'success') {
                    $(`#song-${songid}`).remove();
                } else {
                    alert('Failed to delete song from playlist');
                }
            },
            error: function(response) {
                alert('Error occurred');
            }
        });
    });

    $('#followunfollowbtn').on('click', function() {
        var button = $(this);
        var playlistId = $(this).data('playlistid');
        var csrftoken = $('input[name="csrftoken"]').val();
        var followerscount = $('#followerscount');

        $.ajax({
            url: '/playlist/' + playlistId + '/follow/',
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
