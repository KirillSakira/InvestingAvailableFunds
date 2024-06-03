var pathname = location.pathname.split('/');

if(pathname[1] == 'payment'){
    let val_sum = '';
    function in_inp_sum(){
    }
    $('.auth_inp_o_sum').on('keyup. input', function(e){
        let input = $('.auth_inp_o_sum');
        let val = input.val().replace(/[^0-9]/g, '');
        if(val != val_sum){
            let formatted = val.replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
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
}