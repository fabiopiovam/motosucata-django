$(document).on('submit','#search-form',function(){
    text = $('#text',this).val();
    text = text.replace(/[ ]+/g,'-');
    window.location = '/q/' + text;
    return false;
});