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
                // try{
                    response = JSON.parse(result);
                    if(response.result == 'fail'){
                        err('form', response.description);
                        return;
                    }
                    res = JSON.parse(response.result);
                    if(res['status'] == 'success'){
                        $('#email, #error_message').val('');
                        $('#success_message').val(response.message);
                        clearForm();

                        let html = cloneClientBlock.html()
                        .replace('$id', response.id)
                        .replace('$name', response.name)
                        .replace('$balance', response.balance)
                        .replace('$balance_proc', response.balance_proc)
                        .replace('$color', (response.balance_proc.includes("+")) ? 'col_lb' : 'col_red');
                        $('#mClientsList').append(html);

                        setTimeout(function(){
                            $('#hnewClient').click()
                            blocked_button = false;
                        }, 1000);
                        return;
                    }

                    err('form', res.message);
                    blocked_button = false;
                // }
                // catch(e){
                //     err('form', 'Неожиданная ошибка');
                // }
            });
        }
        blocked_button = false;
    });
}

$('.el_hoverer').on('click', function(){
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