var table_scrol = $('.panel-body-all-messages')


/*
function get_id_folders() {

    dat = {}
    $.ajax({
        url: '% url "get_id_folders" %}', //url страницы (action_ajax_form.php)
        type: "GET", //метод отправки
        dataType: "html", //формат данныUх

        data: dat, // Сеарилизуем объект
        cache: true,
        success: function(response) { //Данные отправлены успешно
            console.log(response)
        },
        error: function(response) { // Данные не отправлены
            return { 'error': 'error' }
        }
    })
}

*/

/*
if (table_scrol.scrollHeight - table_scrol.scrollTop === table_scrol.clientHeight) { */
updater = true


var mouse_ov = false
$('.btn-pag-l').hover(() => {

    mouse_ov = true

})

$('.btn-pag-l').mouseleave(() => {

    mouse_ov = false

})



window.folder = $('.vhod-folder').attr('data-pk-id_folder')

function update_upodater(intsd) {
    let intdd = intsd || 1500


    update_page = setInterval(function() {

        if ($('.cr-styled input:checked').length < 1 && !window.update_stop && table_scrol.scrollTop() < 160 && !mouse_ov) {

            sort_Message({
                sort: window.sort || '-lifetime',
                page: window.page || 1,
                type: window.type || 'all',
                prof: window.prof

            })

        } else {

        }
    }, intdd)




}

update_upodater()

/*

function get_notificate() {
    $.ajax({
        type: "POST",
        url: get_notificate_url,
        cashe: false,
        success: function(data) {

            for (key in data) {
                alertify.success(data[key][1]);
            }
        }
    });
}


get_notificate()
*/