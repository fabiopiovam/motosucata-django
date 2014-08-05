function callImage(obj){
    $("#large-image")
        .attr('src',$('input',obj).val())
        .attr('title',$('img',obj).attr('title'))
        .attr('alt',$('img',obj).attr('alt'));
    
    $("#image-description").text($('img',obj).attr('title'));
    
    $(".tn_photo").css('border','none');
    $(obj).css('border','3px solid #B8B8B8');
}

$(document).on('click', ".tn_photo", function(){ callImage(this); } );

callImage($('.tn_photo:first'));