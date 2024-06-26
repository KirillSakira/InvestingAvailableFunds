
if(pathname[1] == 'trade'){
    $('.trade_tabs').on('click', '.el_hoverer', function(){
        window.open('/securitiesTrade/' + pathname[2] + '/' + this.getAttribute('data-id'), '_self');
    });
    
    $('button').on('click', function(){
        if(!blocked_button){
            blocked_button = true;
            let thiss = this;
            let tid = this.getAttribute('data-tab');
            $('button').removeClass('back_lb');
            $('.tabs').fadeOut(200);
            setTimeout(function(){
                $(thiss).addClass('back_lb');
                $('[data-tabId="' + tid + '"]').fadeIn(200);
                setTimeout(() => blocked_button = false, 200);
            }, 200);
        }
    });
}