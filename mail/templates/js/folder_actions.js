function folderDelete(pk) {

    var dat = {
        pk: pk,
        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
    };



    $.ajax({
        url: '{% url "folderdelete" %}', //url страницы (action_ajax_form.php)
        type: "POST", //метод отправки
        dataType: "html", //формат данных

        data: dat, // Сеарилизуем объект
        cache: false,
        success: function(response) { //Данные отправлены успешно
            console.log(response)
        },
        error: function(response) { // Данные не отправлены
            console.log(response)
        }
    });
}