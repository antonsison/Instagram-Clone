$(document).ready(function(){
    $(".comment-reply-btn").click(function(event) {
        event.preventDefault();
        $(this).parent().next(".comment-reply").fadeToggle();
    })

    var likes = parseInt($('#like_count')[0].textContent);
    $('.like').click(function(){
        var initial = $(this).data('initial');
        var isLiked = $(this).data('bool');
        var post_id = $(this).data('name')
        var counter = $('#like_count')[0];

        $(this).data('bool', isLiked ? false:true);
    /*  console.log(isLiked)
        console.log(counter)
        console.log(likes, 'jhkhjk')
    */
        if (initial) {
            if (isLiked) {
                $(this).removeClass('btn-default').addClass('btn-info');
                $(this).attr('value', 'Like')
                counter.innerHTML = likes - 1

            } else {
                $(this).removeClass('btn-info').addClass('btn-default');
                $(this).attr('value', 'Unlike')
                counter.innerHTML = likes

            }
        } else {
            if (isLiked) {
                $(this).removeClass('btn-default').addClass('btn-info');
                $(this).attr('value', 'Like')
                counter.innerHTML = likes

            } else {
                $(this).removeClass('btn-info').addClass('btn-default');
                $(this).attr('value', 'Unlike')
                counter.innerHTML = likes + 1

            }
        }
        
        var csrf = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            type: "POST",
            url: $(this).data('url'),
            data: {'id': post_id, 'liked': isLiked, 'csrfmiddlewaretoken': csrf },
            success: function(data) {
                console.log(data.liked)
            },

            error: function(err) {
                console.log(err, 'error');
            }
        });
    });
});