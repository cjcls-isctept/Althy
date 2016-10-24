
$(function(){
$('.upvote_comment, .upvote_comment_on').click(function(){
    var catid;
    catid=$(this).attr("data-catid");
    var aux='/website/';
    var aux2= '/upvote_comment/';
    var url=aux.concat(catid,aux2);
    console.log(url);
    var $parent= $(this).parent().closest('div'); 
    $.get(url,function(data){
        $parent.find('#count').html(data);
    });
     if($(this).hasClass('upvote_comment')){
        $(this).removeClass();
        $(this).addClass('upvote_comment_on');
    }else{
        $(this).removeClass();
        $(this).addClass('upvote_comment');
    }   
    
    
    var aux2= $parent.find('#downvote')
     if($(aux2).hasClass('downvote_comment_on')){
        $(aux2).removeClass();
        $(aux2).addClass('downvote_comment');
    }   
    
});
});


$(function(){
$('.downvote_comment, .downvote_comment_on').click(function(){
    var catid;
    catid=$(this).attr("data-catid");
    var aux='/website/';
    var aux2= '/downvote_comment/';
    var url=aux.concat(catid,aux2);
    console.log(url);
    var $parent= $(this).parent().closest('div'); 
    $.get(url,function(data){
        $parent.find('#count').html(data);
    });
     if($(this).hasClass('downvote_comment')){
        $(this).removeClass();
        $(this).addClass('downvote_comment_on');
    }else{
        $(this).removeClass();
        $(this).addClass('downvote_comment');
    }  
    var aux2= $parent.find('#upvote')
     if($(aux2).hasClass('upvote_comment_on')){
        $(aux2).removeClass();
        $(aux2).addClass('upvote_comment');
    }  
});
});

$(function(){
$('#load').click(function(){
    
    var $parent= $(this).parent().closest('comments_container'); 

    $.get(url,function(data){
        $parenta.appendChild(data);
    });
});
});





/*
$().append('<div class="click">ola</div>');

*/