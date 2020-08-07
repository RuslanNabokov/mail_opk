async function otw_mes(pk_mes) {
    var val;
    dat = { 'message': pk_mes }
    $.ajax({
        url: '{% url "answ_mes" %}', //url страницы (action_ajax_form.php)
        type: "GET", //метод отправки
        dataType: "json", //формат данныUх

        data: dat, // Сеарилизуем объект
        cache: true,
        async: true,
        success: function(response) { //Данные отправлены успешно
            answ = response['answ']
            group = response['group']
            $('[data-mes-pk-to-mes=' + pk_mes + ']').attr('message-pk', answ)
            $('[data-mes-pk-to-group=' + pk_mes + ']').attr('href', '/mail/message/' + answ)


            //  $('[data-id='+id+']')
        },

    })

    return val
}


/*
async function img_organization(owner) {
    var val;
    dat = { 'user': owner }
    console.log()
    $.ajax({
        url: '{% url "img_organization" %}', //url страницы (action_ajax_form.php)
        type: "GET", //метод отправки
        dataType: "json", //формат данныUх
        data: dat, // Сеарилизуем объект
        cache: true,
        async: true,
        success: function(response) { //Данные отправлены успешно
            answ = response['img']
            console.log(answ)
            if ($('[img_pk_own=' + owner + ']').attr('style') == "background-image:" + 'url(' + '/' + answ + ')') {

            } else {
                console.log(($('[img_pk_own=' + owner + ']').attr('style')))
                $('[img_pk_own=' + owner + ']').attr('style', 'background-image: ' + 'url(' + '/' + answ + ')')
            }

        },

    })

    return val
}

*/



function get_users(pk_mes) {
    var val;
    dat = { 'message': pk_mes }
    $.ajax({
        url: '{% url "get_users" %}', //url страницы (action_ajax_form.php)
        type: "GET", //метод отправки
        dataType: "json", //формат данныUх

        data: dat, // Сеарилизуем объект
        cache: false,
        async: false,
        success: function(response) { //Данные отправлены успешно
            val = response['users']
            console.log(val)
        },

    })

    return val
}


var options = {
    //   era: 'long',
    // year: '2-digit',
    month: '2-digit',
    day: 'numeric',
    weekday: 'short',
    //    timezone: 'UTC',
    hour: 'numeric',
    minute: 'numeric',
    //  second: 'numeric'
};


function format_data(dat) {
    let dats = dat.split(" ")[0].split('-')
    let time = String(String(dat).split(" ")[1]).split(':')
    day = new Date(parseInt(dats[0]), parseInt(dats[1]) - 1, parseInt(dats[2]), parseInt(time[0]), parseInt(time[1]), parseInt(time[2]))
    now_date = new Date(Date.now())
    console.log([now_date.getFullYear(), now_date.getMonth()] == [day.getFullYear(), day.getMonth()])

    if (now_date.getFullYear() == day.getFullYear() & now_date.getMonth() == day.getMonth()) {
        if (now_date.getDate() - day.getDate() < 1) {
            return `Сегодня в  ${dat.split(" ")[1]}`;
        } else if ((now_date.getDate() - day.getDate() < 2)) {
            return `Вчера  в  ${dat.split(" ")[1]}`;
        }
    }

    return day.toLocaleString("ru", options)


}

/*
var sliced = text.slice(0,10);
if (sliced.length < text.length) {
sliced += '...';
}

*/
function create_Mes(pk_group, owner, title, lifetime, clone, pk_mes, answ, favorite, sinopsis, read, img_path, redact) {
    $('#loader').show()

    var c = clone.clone()
    c.attr('data-pk', pk_mes)
    if (favorite) {

        $(c.find('.fa-star')).addClass('fa-star-active')
    } else {
        $(c.find('.fa-star')).removeClass('fa-star-active')
    }
    c.find('.fa-star').attr('data-pk', pk_mes)
    c.find('.chk').data()['pk'] = pk_group // ssilkana group
    if (answ) {
        otw_mes(pk_mes)

        c.find('.own-user').html(`<img id ="search-img"  style='font-size: 10px' src = ${static_icon_peresilka} >` + '' + owner) // ot kogo
        c.find('.own-user').append('  <i style= " font-size: 13px" data-mes-pk-to-mes=' + pk_mes + '  class = "my-fa fa ion-eye" data-pk = ""  data-toggle="modal" data-target="#modal-mes" > </i>')
        c.find('.own-user').append(' <a style= "margin-right: 10px; font-size: 13px" data-mes-pk-to-group=' + pk_mes + '   class = "my-fa fa fa-envelope-o" href="' + '/mail/message/' + ' ' + '"' + '</a>')


    } else {
        c.find('.own-user').text('' + owner)
    }
    c.find('.own-user').attr('href', '/mail/message/' + pk_mes) // ssilka

    c.find('.mes-titled').html(' ' + title + '  ') // title
    c.find('.block-i').html('<a class = "fa my-fa fa-envelope-o" href =' + '"/mail/message/' + pk_mes + '"' + ' ></a> ' + '      <v> <i style="font-size: 16px" class = "my-fa ion-eye"  data-toggle="modal" data-target="#modal-mes" > </i> </v>')
    if (redact) {

        c.find('.block-i').append('<a style= "font-size: 16px" class = "fa my-fa fa-pencil-square-o" href="/mail/new_message/' + pk_group + '"' + ' >' + " </a>")
        c.find('.block-i').prepend('<a  style= "font-size: 14px;" data-pk ="' + pk_mes + '"class = "fa my-fa fa-users" data-tooltip="' + "" + '"> </a>')


    } else {}

    c.find('.mes-title').attr('href', '/mail/message/' + pk_mes) // title
    c.find('.mes-sinopsis').text(' ' + sinopsis)


    c.find('.time').text(format_data(lifetime)) // lifetime 

    if (!read) {
        c.addClass("no_read_message");
    }




    c.find('.ion-eye').attr('message-pk', pk_mes)



    c.find('.letter_or_picter').attr('img_pk_own', owner)
    if (img_path && img_path != 'undefiend') {
        c.find('.letter_or_picter').attr('style', 'background-image: ' + 'url(' + '/' + img_path + ')')
        c.find('.letter_or_picter').text('')
    } else {
        c.find('.letter_or_picter').text(String(owner).slice(0, 1).toUpperCase())
    }

    c.show()
    $('.tbody').append(c)


    setTimeout(function() {
        $('#loader').remove()

    }, 140);

}


$('#datatable').on('mouseenter', '[data-tooltip]',
    function() {
        pk_mes = parseInt($(this).data("pk"))
        console.log(pk_mes)
        users = get_users(pk_mes)
        $(this).attr('data-tooltip', users)
    }


)