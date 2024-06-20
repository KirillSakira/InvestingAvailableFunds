if(pathname[1] == ''){
    const cloneClientBlock = $('.cloneClientBlock').clone();
    $('.cloneClientBlock').remove();
        
    $('#hnewClient').on('click', function(){
        if(!blocked_button){
            blocked_button = true;
            $('.newClientEmail').animate({
                height: "toggle"
            }, 500, function(){
                blocked_button = false;
            });
        }
    });

    $('form#mAddEmail_form').on('submit', function(e){
        e.preventDefault();
        if(blocked_button) return;
        clearForm();

        blocked_button = true;
        if($('#email').val().trim() == '') err('.email', 'Введите email');
        
        if(blocked_button && !errs){
            let params = $(this).serialize();
            request("/mAddClientMail/", params, function(result){
                try{
                    response = JSON.parse(result);
                    if(response.result == 'fail'){
                        err('form', response.description);
                        return;
                    }
                    res = JSON.parse(response.result);
                    if(res['status'] == 'success'){
                        clearForm();
                        $('#email').val('');
                        $('#error_message').text('');
                        $('#success_message').text(res.message);

                        let html = cloneClientBlock.html()
                        .replace('$id', res.id)
                        .replace('$name', res.name)
                        .replace('$balance', res.balance)
                        .replace('$balance_proc', res.balance_proc)
                        .replace('$color', (toString(res.balance_proc).includes("-")) ? 'col_red' : 'col_lb');
                        $('#mClientsList').prepend(html);
                        $('.cloneb').fadeIn(400);
                        setTimeout(() => $('.cloneb').removeClass('cloneb'), 400);

                        setTimeout(function(){
                            $('#hnewClient').click()
                            blocked_button = false;
                            setTimeout(() => $('#success_message').text(''), 500);
                        }, 600);
                        return;
                    }

                    err('form', res.message);
                    blocked_button = false;
                }
                catch(e){
                    err('form', 'Неожиданная ошибка');
                }
            });
        }
        blocked_button = false;
    });
}

$('#mClientsList').on('click', '.el_hoverer', function(){
    if(['', 'operations'].indexOf(pathname[1]) !== -1)
        window.open('/enterprise/' + this.getAttribute('data-id'), '_self');
});

if(pathname[1] == 'trade'){
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

function resizeHe(){
    if(['operations', 'tradeHistory'].indexOf(pathname[1]) !== -1){
        $('.nomh > div > div:nth-child(2)').css('max-height', 'calc(100vh - ' + ($('.header').height() + $('.nomh > div > div.h1').height()) + 'px - 10.5rem)');
    }
    if(pathname[1] == 'trade'){
        $('.nomh > div > div:nth-child(2)').css('max-height', 'calc(100vh - ' + ($('.header').height() + $('.tradeSels').height() + $('.nomh > div > div.h1').height()) + 'px - 13rem)');
    }
}
resizeHe();


window.addEventListener('resize', (e) => {
    if(window.innerWidth == vw && window.innerHeight == vh) return;
    vw = window.innerWidth;
    vh = window.innerHeight;
    resizeHe();
});