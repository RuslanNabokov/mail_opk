function sort_Message(obj) {


    var page = obj.page || 1
    var dat = {
        sort: obj.sort || '-lifetime',
        page: obj.page || 1,
        prof: obj.prof || 'undefiend',
        type: window.folder || 'all', //window.location['href'].split('/')[5].replace('#', ''),
        filter: obj.filter || window.filter || 'all',
        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),

    };
    console.log('sort')
    var url = '{% url "ajax_get_all_message" %}'

    $.ajax({
        url: url, //url страницы (action_ajax_form.php)
        type: "POST", //метод отправки
        dataType: "json", //формат данныUх

        data: dat, // Сеарилизуем объект
        cache: false,
        success: function(response) { //Данные отправлены успешно
            window.sort = dat.sort
            window.page = dat.page
            window.type = dat.type
            if (dat.prof) {
                window.prof = dat.prof
            }
            $(".btn-pag").each(function() {
                $(this).attr('data-sort', dat.sort)

            })

            var clone = $($('.message')[0]).clone()

            $('.tbody > .message').slice(1).remove()

            pagination(response["paginator"][0], response["paginator"][1], response["paginator"][2], response['paginator'][3])
            for (key in response) {
                if (key == 'status') {
                    //alert('empty')
                    console.log('empty')
                } else {
                    if (key !== 'paginator' && key != 'notification' && key != 'count_messages') {
                        console.log(key)
                        let pk = response[key][0]
                        let own = response[key][2]
                        let title = response[key][1]

                        let lifetime = String(response[key][3]).split('.')[0].replace('T', ' ')
                        let pk_mes = response[key][4]
                        let answ = response[key][5]
                        let favorite = response[key][6]
                        let sinopsis = response[key][7]
                        let read = response[key][8]
                        let redact = response[key][9]
                        let img_path = response[key][10]
                        create_Mes(pk, own, title, lifetime, clone, pk_mes, answ, favorite, sinopsis, read, img_path, redact)
                    }
                }
                if (key == "notification") {

                    for (i in response['notification']) {
                        alertify.success(response['notification'][i])
                    }
                }

            }

        },
        error: function(response) { // Данные не отправлены

        }
    })


}