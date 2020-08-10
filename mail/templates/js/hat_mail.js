$('#concret-search').on('click', function() {

    let block = $("#block-concret-block")
    block.toggleClass("block-concret-search-visible")
    block.toggleClass("block-concret-search")


})
var inputFocused = false;

$('#inputEmail4').focus(function() {

    $('.search-img').hide('slow')
    inputFocused = true


})




$('#inputEmail4').on('blur', function(e) {
    inputFocused = false;

    $("#inputEmail4").val('')
    $('.search-img').show('slow')
});


function update_promise_serch() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            search_message()

            resolve(true)

        }, 70)
    })
}


$("#inputEmail4").keypress(function(e) {
    if (e.which === 13) {
        if ($("#inputEmail4").val().replace(/\s{2,}/g, ' ') == '') {
            search_message()
            update_upodater()
            window.update_stop = false

        } else {



            window.update_stop = update_promise_serch();
            window.update_stop = true
                // update_upodater(700000)

        }
    }
});
var time_out = false

$(".searchBox").mouseout(function() {


    time_out = setTimeout(function() {


        let block = $("#block-concret-block")
        block.removeClass("block-concret-search-visible")
        block.addClass("block-concret-search")
        if (!inputFocused) {
            $('.search-img').show('slow')
        } else {}
    }, 1000)


});

$(".searchBox").mouseover(function() {
    if (time_out) {

        clearTimeout(time_out)


    } else {}
})

////


$('a.list-group-item').click(function() {

    if (!($(this).hasClass('new_message_button'))) {

        $('a.list-group-item').removeClass('active')
        if (!($(this).hasClass('folders'))) {
            $(this).addClass('active')
        } else {
            $(this).toggleClass('active')
        }

    } else {

    }
})