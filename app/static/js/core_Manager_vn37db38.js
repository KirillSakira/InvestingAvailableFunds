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
            request("/managerAddClientMail/", params, function(result){
                try{
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
                }
                catch(e){
                    err('form', 'Неожиданная ошибка');
                }
            });
        }
        blocked_button = false;
    });
}

if(pathname[1] == 'operations'){
    $('.operation_el').on('click', function(){
        window.open('/operations/' + this.getAttribute('data-id'), '_blank');
    });
}