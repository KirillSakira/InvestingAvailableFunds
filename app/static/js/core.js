var pathname = location.pathname.split('/');
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
    if(window.innerWidth == vw && window.innerHeight == vh) return;
    vw = window.innerWidth;
    vh = window.innerHeight;
    barChartData.forEach((item) => generBar(item.elem, item.dataPie, item.con));
});

//круговая диаграмма
function generPie(elem, dataPie){
    var ctx = document.getElementById(elem).getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
            data: dataPie.map(obj => obj.count),
            backgroundColor: dataPie.map(obj => obj.color),
            borderWidth: 0,
            borderRadius: 1000,
            }]
        },
        options: {
            cutout: '90%',
            rotation: -10 * Math.PI,
            onHover: (event, chartElement) => {
                const items = document.querySelectorAll('.legend-item');
                items.forEach(item => item.classList.remove('highlight'));
                $('.hportfolio_proc_names').removeClass('pieHoverGraphParent');

                if (chartElement.length > 0) {
                    const index = chartElement[0].index;
                    $('.pie_item_chart').removeClass('pieHoverGraph');
                    $('.hportfolio_proc_names').addClass('pieHoverGraphParent');
                    $('.pie_item-' + index).addClass('pieHoverGraph');
                }
            }
        }
    });
}
$('.canvas_pie').on('mouseout', function() {
    $('.hportfolio_proc_names').removeClass('pieHoverGraphParent');
    $('.pie_item_chart').removeClass('pieHoverGraph');
});

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