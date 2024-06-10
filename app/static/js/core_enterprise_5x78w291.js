var barChart = [];
var barChartData = [];

//bar
function generBar(elem, dataPie, con = 0){
    let canvas = document.getElementById(elem)
        ctx = canvas.getContext('2d'),
        fontSize = parseInt($('html').css('font-size')) * 1.2;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if(barChart[con])
        barChart[con].destroy();

    barChart[con] = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: dataPie['month'],
        datasets: [{
            data: dataPie['count'],
            backgroundColor: '#634FED',
            borderRadius: 20,
            barPercentage: 0.9,
            hoverBackgroundColor: '#7664f0'
        }]
    },
    options: {
        title: {
            display: false
        },
        scales: {
            x: {
                ticks: {
                    font: {
                        size: fontSize
                    },
                    color: '#6E6598'
                }
            },
            y: {
                ticks: {
                    font: {
                        size: fontSize
                    },
                    color: '#6E6598'
                },
                display: false,
            }
        },
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                enabled: true,
                mode: 'index',
                intersect: false,
                backgroundColor: '#453F64',
                titleFont: {
                    size: fontSize,
                    weight: 'bold'
                },
                bodyFont: {
                    size: fontSize
                },
                xPadding: 15,
                yPadding: 15,
                caretPadding: 5,
                caretSize: 5,
                cornerRadius: 8,
                borderWidth: 0,
                borderColor: '#6E6598',
                callbacks: {
                    label: function(tooltipItem) {
                        return 'Количество: ' + tooltipItem.raw;
                    },
                    labelColor: function(tooltipItem) {
                        return {
                            borderColor: '#6E6598', // прозрачная граница
                            backgroundColor: '#6E6598' // прозрачный фон
                        };
                    },
                    labelPointStyle: function() {
                        return {
                            pointStyle: 'line' // задаем стиль точки, чтобы квадрат не отображался
                        };
                    }
                }
            }
        }
    }
    });
    barChartData[con] = {
        'elem': elem,
        'dataPie': dataPie,
        'con': con
    }
}

window.addEventListener('resize', (e) => {
    if(window.innerWidth == vw) return;
    vw = window.innerWidth;
    vh = window.innerHeight;
    barChartData.forEach((item) => generBar(item.elem, item.dataPie, item.con));
});

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
        console.log($(window).scrollTop(), $('.header').height())
        $('.slick-arrow').css('top', 'calc(50vh + ' + ($(window).scrollTop() - $('.header').height())  + 'px');
    });
    $(window).scroll();
}