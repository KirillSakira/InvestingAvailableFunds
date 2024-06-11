if(pathname[1] == 'payment' || pathname[1] == 'withdraw'){
    let val_sum = '';
    function in_inp_sum(){
    }
    $('.auth_inp_o_sum').on('keyup. input', function(e){
        let input = $('.auth_inp_o_sum');
        let val = input.val();
        if(val != val_sum){
            let formatted = val.replace(/[^0-9]/g, '').replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
            formatted = formatted ? formatted + ' ₽' : '';
            input.prop("selectionStart");
            input.val(formatted);
            if (formatted.endsWith(' ₽')) {
                let newCursorPosition = formatted.length - 2;
                input.prop("selectionStart", newCursorPosition);
                input.prop("selectionEnd", newCursorPosition);
            }
        }
        val_sum = val;
    });
    $('.auth_inp_o_num').on('keyup, input', function(e){
        let val = $('.auth_inp_o_num').val().replace(/[^0-9]/g, '').substr(0, 16).replace(/(.{4})/g, '$1 ').trim();
        $('.auth_inp_o_num').val(val);
    });
    $('.auth_inp_o_date').on('keyup, input', function(e){
        let val = $('.auth_inp_o_date').val().replace(/[^0-9]/g, '').substr(0, 4).replace(/(\d{2})(\d{2})/g, '$1/$2').trim();
        $('.auth_inp_o_date').val(val);
    });


    
    $('form#doPayment').on('submit', function(e){
        e.preventDefault();
        if(blocked_button) return;
        clearForm();

        blocked_button = true;
        if($('#summa').val().trim() == '') err('.summa', 'Введите сумму пополнения');
        if($('#card_num').val().trim() == '') err('.card_num', 'Введите номер карты');
        if($('#card_date').val().trim() == '') err('.card_date', 'Введите срок карты');
        if(blocked_button && !errs){
            let params = $(this).serialize();
            request("/refill/", params, function(result){
                try{
                    response = JSON.parse(result);
                    if(response.result == 'fail'){
                        err('form', response.description);
                        return;
                    }
                    res = JSON.parse(response.result);
                    if(res['status'] == 'success'){
                        window.location.href = '/';
                        clearForm();
                        blocked_button = false;
                        return;
                    }

                    err('form', res.message);
                }
                catch(e){
                    err('form', 'Неожиданная ошибка');
                }
            });
        }
        blocked_button = false;
    });
}


if(pathname[1] == 'analytic'){
    $('.analytic_slick').slick({
        dots: false,
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1
    });

    $(window).on("scroll", function(e){
        $('.slick-arrow').css('top', 'calc(50vh + ' + ($(window).scrollTop() - $('.header').height())  + 'px');
    });
    $(window).scroll();
}