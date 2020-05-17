	$(function() {
	    // using jQuery
	    /*
    
	    mast have token v zdanii
    
	    */

	    function getCookie(name) {
	        var cookieValue = null;
	        if (document.cookie && document.cookie != '') {
	            var cookies = document.cookie.split(';');
	            for (var i = 0; i < cookies.length; i++) {
	                var cookie = jQuery.trim(cookies[i]);
	                // Does this cookie string begin with the name we want?
	                if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                    break;
	                }
	            }
	        }
	        return cookieValue;
	    }


	    /*
    
	    Работа с модулем выбора и вставки жаблона сообщения в новое сообщение
    
    
	    */


	    var csrftoken = getCookie('csrftoken')


	    $('#modal-shablon').off().on('click', '.add_text', function() {
	        let html = $('#right').html()

	        $('#id_body').data("wysihtml5 ").editor.setValue(html);


	    });

	    function add_shablon(response) {
	        $('#right').empty()
	        $('#right').append(response['text'])

	    }


	    function search_shabl(pk) {
	        dat = {
	                pk_mes: pk
	            },
	            $.ajax({
	                url: '{% url "get_shablons" %}', //url страницы (action_ajax_form.php)
	                type: "GET ", //метод отправки
	                dataType: "json ", //формат данныUх

	                data: dat, // Сеарилизуем объект
	                cache: false,
	                success: function(response) { //Данные отправлены успешно
	                    add_shablon(response)
	                },
	                error: function(response) { // Данные не отправлены
	                    console.log(response)
	                }
	            })
	    }

	    $('.btn-show').off().on('click', function() {
	        let pk_shabl = $(this).attr('data-pk')
	        search_shabl(pk_shabl)
	        return false
	    })


	    $('#btn_shablon').on('click', function() {

	    })

	    var ret_name = function() {
	        let mass = []
	        $('.names > p').each(function() {
	            mass.push(this.innerText)
	        })
	        return mass
	    }



	    $('#btn').click(function() {

	        $('#ss')[0].value = ret_name()
	        $('#csrf').val(getCookie('csrftoken'))
	    });


	    closel = function(pk, pk_prof) {
	        if (pk) {
	            $('[data-id=' + pk + ']').remove()
	        } else {}
	        if (pk_prof) {
	            $('[data-id-prof=' + pk_prof + ']').remove()
	        } else {}
	    }

	    var arr = ['id_file_fild', 'id_title', 'id_body', 'id_users', 'form_control', 'id_number']
	    $.each(arr, function(index, value) {
	        eval(`$("#${value} ")`).addClass("form-control ")
	    })


	    var dataList = document.getElementById('json-datalist');
	    var input = document.getElementById('#txtSearch');


	    function add_user(pk, pk_prof, sec, label) {

	        let p = "<p class='new' data-id=" + " '" + pk + "' " + " data-id-prof=" + " '" + pk_prof + "' " + " data-sec='" + sec + "' " + "> " + label + ' <
	        buttuon onclick = "closel' +  '(' + pk + ' , ' +  pk_prof +     ')"
	        ' + '
	        class = "close"
	        ' + "data-fg=" + "'
	        " + pk  + "
	        '" + "></button></p>"

	        $('.names ').append(p);
	    }
	    /*
	    {% if answer %}
    
	    add_user({{answer.owner.pk}},0, 0,"{{answer.owner.username}}")
    
	    {% endif %}
	    */
	    { % if users % }

	    { % for i in users % }


	    add_user({
	        { i.pk }
	    }, {
	        { i.pk }
	    }, 0, "{{i.username}}") { % endfor % }

	    { % endif % }

	    function AutoCompleteSelectHandler(event, ui) {
	        var selectedObj = ui.item;
	        if ($(`[data-id = 1 ]`).length > 0) {
	            alertify.error("Пользователь уже добавлен");
	        } else {
	            add_user(ui.item["pk"], ui.item["pk_prof"], ui.item["sec"], ui.item["label"])
	        }
	    }





	    $("#txtSearch").autocomplete({

	        source: '{% url "searchmessage" %} ',
	        minLength: 1,

	        select: function(event, ui) { //item selected
	            AutoCompleteSelectHandler(event, ui)
	        },
	        open: function(event, ui) {

	        }
	    });
	    t = 0

	    setTimeout(function() {




	        let but = $('<button id="btn_shablon" type="button" data-toggle="modal" data-target="#modal-shablon" style="position: absolute; left: 70%" class="btn btn-dark my-btn">Выбрать шаблон</button>') $('#id_body').wysihtml5() $('.btn-default').last().remove();
	        $('.btn-default').last().remove();
	        $('.btn-default').last().remove();
	        $(".wysihtml5-toolbar").append(but)
	    }, 20);
	});