{% load staticfiles %}

function get_message(pk_mes) {
    $.get(

        '{% url "read_mes" %}', {
            message: pk_mes,
        },
        onAjaxSuccess
    );






    function onAjaxSuccess(data) {
        let mes_title = data['message'][0]
        let mes_body = data['message'][1]
        let own_mes = data['message_group'][0]
        let files = data['files']

        let lifetime = data['message_group'][1].split('.')[0].replace('T', ' ')
        $('#title_modal').empty()
        $('#message_body').empty()
        $('#owner_mes').empty().append('От: ' + own_mes)
        $('#data_mes').empty().append(lifetime)
        $('#files').empty()


        $('#title_modal').append(mes_title)
        $('#message_body').append(mes_body)
        $('.gridModalLabel').append()

        if (files.length > 0) {
            $('#files').html('	<h4><i class="fa fa-paperclip m-r-10 m-b-10"></i>  Документы  </h4>')

            files.forEach(function(item, i, arr) {

                $('#files').append(
                    `<img src="{% static  'icon/file.png' %}" class="file br-radius m-r-10">${item[1]} </img>  
                <input type="checkbox" style="margin: 0px 6px 0;" class="chk-files" data-file-uuid=${item[0]}>`
                )


            });

            $('#files').append(`
                <input type="button" id="perem_files" value="Переместить" style="width:100px;height: 20px;float: inline-end;"> `)
        }
    }
}

params = `scrollbars=no,resizable=no,status=no,location=no,toolbar=no,menubar=no,
width=400,height=400,left=1000,top=-1`
new_win = false


$(document).on('click', '#perem_files', function() {
    let cheked = $('.chk-files:checked')
    c = new Array()
    let uuid = cheked.map(function(index, val) {
        c.push(val.getAttribute('data-file-uuid'))
        return 1
    })

    uuid = c.join(',')
    str_ = '{% url "poligon" %}' + '?names=' + uuid

    new_win = window.open(str_, 'file_manager', params)
    
   
    new_win.onload = function() {
  

    };
new_win.onblur = () => new_win.focus();
})