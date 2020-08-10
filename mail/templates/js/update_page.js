var table_scrol = $('.panel-body-all-messages')

var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
var isFirefox = navigator.userAgent.toLowerCase().indexOf('firefox') > -1;
var isIE = navigator.appName == 'Microsoft Internet Explorer' || !!(navigator.userAgent.match(/Trident/) || navigator.userAgent.match(/rv:11/));

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




$('table').on('mouseenter', '.fa', function(e) {
    mouse_ov = true

})



$('table').on('mouseleave', '.fa', function(e) {



    mouse_ov = false
})





$('table').on('mouseenter', '.fa-users', function(e) {

    mouse_ov = true
    let message = $(e.currentTarget).data('tooltip')

    $(e.currentTarget).parent().parent().find('.mes-titled').hide()
    $(e.currentTarget).parent().parent().find('.mes-sinopsis').hide()
    $(e.currentTarget).parent().parent().find('.mes-users').text("Сообщение было отправлено: " + message)
    $(e.currentTarget).parent().parent().find('.mes-users').show()



    /*.mail-news-title */
})


$('table').on('mouseleave', '.fa-users', function(e) {

    $(e.currentTarget).parent().parent().find('.mes-sinopsis').show()
    $(e.currentTarget).parent().parent().find('.mes-titled').show()
    $(e.currentTarget).parent().parent().find('.mes-users').hide()
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

//Действия при клики на строку сообщения 

$('table').on('click', 'td', function(e) {
    //    
    var no_action_click = ['mail-select', 'my-fa', 'answ', 'fa', 'chk', 'fa-star-active'];
    var locate = $($(e.target.closest('tr'))).find('.block-i').find('.fa-envelope-o').attr('href')
    let id_mes = ($(e.target.closest('tr')).attr('data-pk'))
    if (isFirefox) {

        if (no_action_click.indexOf(e.originalEvent.originalTarget.className.split(' ')[0]) != -1) {

        } else {
            window.location = locate

        }
    } else {




        if (no_action_click.indexOf($(e.toElement).context.className.split(' ')[0]) != -1) {


        } else {

            window.location = locate
        }
    }
});