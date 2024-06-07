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
