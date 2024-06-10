var pathname = location.pathname.split('/');

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