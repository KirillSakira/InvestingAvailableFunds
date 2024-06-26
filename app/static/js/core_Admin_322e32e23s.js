$('#aUserList').on('click', '.el_hoverer', function(){
    if(pathname[1] == '')
        window.open('/' + $(this).parent().attr('data-type') + '/' + this.getAttribute('data-id'), '_self');
});