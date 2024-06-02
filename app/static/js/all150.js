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


var barChart;

//круговая bar
function generBar(){
    let canvas = document.getElementById('webixChart')
        ctx = canvas.getContext('2d'),
        fontSize = parseInt($('html').css('font-size')) * 1.2;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if(barChart)
        barChart.destroy();
    barChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: graph_bar['month'],
        datasets: [{
            data: graph_bar['count'],
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
                    color: '#453F64'
                }
            },
            y: {
                ticks: {
                    font: {
                        size: fontSize
                    },
                    color: '#453F64'
                },
                display: false
            }
        }
    }
    });
}

window.addEventListener('resize', (e) => {
    if(window.innerWidth == vw) return;
    vw = window.innerWidth
    vh = window.innerHeight
    // if(typeof(graph_bar) !== 'undefined') generBar();
});


//круговая диаграмма
function generPie(){
    var ctx = document.getElementById('pieChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
            data: graph_pie,
            backgroundColor: ['#3AA1FF', '#FF523A', '#F1EDFD', '#634FED'],
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