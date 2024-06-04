const urls = location.pathname;
let blocked_button = false;

function request(url, requestParams, callback){
    let response = {},
        xhr = new XMLHttpRequest();

    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    blocked_button = true;
    document.body.style.cursor = "wait";
    xhr.onreadystatechange = function(){
        if(xhr.readyState !== 4){
            return;
        }
        if(xhr.status === 200){
            response = {
                result: xhr.responseText,
                description: ""
            };
        }
        else{
            response = {
                result: "fail",
                description: "Ошибка " + xhr.status
            };
            $('#error_message').text('Неожиданная ошибка');
        }
        callback(JSON.stringify(response));
        document.body.style.cursor = "default";
    };
    xhr.send(requestParams);
};

$(document).ready(function() {
    $('#preloader').fadeOut(200);
    setTimeout(() => $('body').removeClass('bpreloader'), 300);
});

var vw = window.innerWidth,
    vh = window.innerHeight;


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
        plugins: {
            legend: {
                display: false
            }
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
                display: false
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
        }
    });
}