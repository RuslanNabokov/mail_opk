function search_mes_w(search, key, prof) {
    var dat = {
        search: search,
        key: key,
        prof: prof,
        type: window.folder,
        filter: window.filter || 'all'
            //   nepr: nepr || 'false'
    };

    $.ajax({
        url: '{% url "searc_mes" %}', //url страницы (action_ajax_form.php)
        type: "POST", //метод отправки
        dataType: "json", //формат данныUх

        data: dat, // Сеарилизуем объект
        cache: false,
        success: function(response) { //Данные отправлены успешно
            var clone = $($('.message')[0]).clone()
            if (response[0]) {
                $('.tbody > .message').slice(1).remove()
                for (key in response) {
                    if (key == 'paginator') {
                        pagination(response[key][0], response[key][1], response[key][2], response[key][3])
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
                }


            } else {
                alert('Ничего не найдено')
            } // endif 

        },
        error: function(response) { // Данные не отправлены
            alert(response)
        }
    })
};



// функция поиска по введенным данным

function search_message() {

    let search = $("#inputState :selected").data('sort');
    let words = $('#inputEmail4').val()
    let c = $('#inputState_prof >   option:contains(' + $('#inputState_prof').val() + ')')
    let id_prof = c.data('profile')
        // let check = $('#read_message').prop('checked')
    if (words.length > 0) {

        search_mes_w(search, words, id_prof)
    } else {
        window.update_stop = true
        update_promise('-lifetime', 1, id_prof).then((update) => {
            window.update_stop = update

        })
    }
}