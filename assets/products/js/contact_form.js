$('.errorlist:first').next('p').find('input,textarea').focus();
$('input,textarea', '.mail-message ~ p:first').focus();
$('input[type="text"],input[type="email"],textarea','.mail-success ~ p').val('');