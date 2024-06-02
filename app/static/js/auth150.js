const nameInput = {
    'username': 'Логин',
    'email': 'Почту',
    'password': 'Пароль',
    'title': 'наименование организации',
    'typeProperty': 'вид собственности',
    'address': 'адрес главного офиса',
    'name': 'ФИО',
    'phone': 'Номер телефона'
}

function inInp(element){
    let el = $(element.target).parent().parent();
    $(el).removeClass('error');
    $(el).find('.error_podinp').text('');
}

function err(el, val){
    let interval = 100;
    if(el != 'form'){
        $(el).addClass('error');
        $(el).find('.error_podinp').text(val);
    }
    else{
        $(el).find('h3').text(val);
    }
    $(el).animate({left: '-20px'}, interval);
    setTimeout(() => $(el).animate({left: '15px'}, interval), interval);
    setTimeout(() => $(el).animate({left: '-10px'}, interval), interval * 2);
    setTimeout(() => $(el).animate({left: '5px'}, interval), interval * 3);
    setTimeout(() => $(el).animate({left: '0px'}, interval), interval * 4);
    setTimeout(() => blocked_button = false, interval * 5);
}

function clearForm(){
    $('.inputs_bl').removeClass('error');
    $('.error_podinp').text('');
}

$('input').on('input', (e) => inInp(e));
$('input').on('change', (e) => inInp(e));

$(document).ready(function() {
    const inps = document.querySelectorAll('.inputs_bl input');
    
    $('#password').keydown(function(event) {
      if (event.keyCode == 13) $('#auth_but, #reg_but').click();
    });
    
    $('form#auth_form').on('submit', function(e){
        e.preventDefault();
        if(blocked_button) return;
        clearForm();

        blocked_button = true;
        inps.forEach(item => {
            if(item.value.trim() == '') err('.' + item.id, 'Введите ' + nameInput[item.id]);
        });
        
        if(blocked_button){
            let params = $(this).serialize();
            request("/login/", params, function(result){
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
    });

    $('form#registration_form').on('submit', function(e){
        e.preventDefault();
        if(blocked_button) return;
        clearForm();

        blocked_button = true;
        inps.forEach(item => {
            if(item.value.trim() == '') err('.' + item.id, 'Введите ' + nameInput[item.id]);
        });
        
        if(blocked_button){
            let params = $.param({'login': $('#email').val()}) + '&' + $(this).serialize();
            request("/reg/", params, function(result){
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
                    
                    inps.forEach(item => {
                        if(res[item.id] != undefined) err('.' + item.id, res[item.id]);
                    });
                    blocked_button = false;
                }
                catch(e){
                    err('form', 'Неожиданная ошибка');
                }
            });
        }
    });
});