$(function(){
$('.downvote_post, .downvote_post_on').click(function(){
    var catid;
    catid=$(this).attr("data-catid");
    var aux='/website/';
    var aux2= '/downvote_post/';
    var url=aux.concat(catid,aux2);
    var $parent= $(this).parent().closest('div'); 
    $.get(url,function(data){
        $parent.find('#count').html(data);
    });
     if($(this).hasClass('downvote_post')){
        $(this).removeClass();
        $(this).addClass('downvote_post_on');
    }else{
        $(this).removeClass();
        $(this).addClass('downvote_post');
    }  
    var aux2= $parent.find('#upvote')
     if($(aux2).hasClass('upvote_post_on')){
        $(aux2).removeClass();
        $(aux2).addClass('upvote_post');
    }  
});
});



$(function(){
$('.upvote_post, .upvote_post_on').click(function(){
    var catid;
    catid=$(this).attr("data-catid");
    var aux='/website/';
    var aux2= '/upvote_post/';
    var url=aux.concat(catid,aux2);
    var $parent= $(this).parent().closest('div'); 
    $.get(url,function(data){
        $parent.find('#count').html(data);
    });
     if($(this).hasClass('upvote_post')){
        $(this).removeClass();
        $(this).addClass('upvote_post_on');
    }else{
        $(this).removeClass();
        $(this).addClass('upvote_post');
    }   
     var aux2= $parent.find('#downvote')
     if($(aux2).hasClass('downvote_post_on')){
        $(aux2).removeClass();
        $(aux2).addClass('downvote_post');
    }   
});
});



/*
$().append('<div class="click">ola</div>');

*/