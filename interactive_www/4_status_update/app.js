main = function(){
    $('.btn').addClass('disabled');
    $('.btn').click( function() {
        var post = $('.status-box').val();
        $('<li>').text(post).prependTo('.posts');
        $('.status-box').val('');
        $('.counter').text(140);
        $('.btn').addClass('disabled');
        });
    $('.status-box').keyup(function(){
        var postLength = $(this).val().length;
        var charactersLeft = 140 - postLength;
        if (charactersLeft <0) {$('.btn').addClass('disabled')}
        else if (charactersLeft === 140) {$('.btn').addClass('disabled')}
        else {$('.btn').removeClass('disabled')}
        $('.counter').text(charactersLeft)
    
        });
    
    };

$(document).ready(main)
