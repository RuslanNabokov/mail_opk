$('.folder-icon').on('click', function() {

    let folder = $(this).data('id')
    let params = { sort: 'lifetime', type: folder }

    window.update_stop = true
    update_promise(params).then((update) => {
        window.update_stop = update

    })


    window.folder = folder
    $('.page-title > .title').text($(this).data('pk-name'))

    return false

})





$('.folder').on('click', function() {

    let folder = $(this).data('pk-id_folder')
    let params = { sort: '-lifetime', type: folder }
    window.update_stop = true
    update_promise(params).then((update) => {
        window.update_stop = update

    })

    window.folder = folder
    $('.page-title > .title').text($(this).data('pk-name'))

    return false

})


var demo3Rows = {
    '1': { name: 'First row', description: 'Lorem ipsum dolor sit amet' },
    '2': { name: 'Second row', description: 'Nemo enim ipsam voluptatem quia voluptas' },
    '3': { name: 'Third row', description: 'Ut enim ad minima veniam' }
};

var menu = new BootstrapMenu('.folder-icon', {
    fetchElementData: function($rowElem) {
        var rowId = $rowElem.data('id')
        return rowId
    },
    actions: [{
            name: 'Удалить',
            onClick: function(row) {
                folderDelete(row)
                let a = $(`.folder-icon[data-id = ${row} ]`)
                $($(a).parent()).hide('slow')
            }
        },
        {
            name: 'Переместить в папку',
            onClick: function(row) {

                in_fold(row)
            }
        }
    ]
});


var menu = new BootstrapMenu('.right-panel', {
    fetchElementData: function($rowElem) {
        return 'click'
    },
    actions: [{
            name: 'Создать папку',
            onClick: function(row) {
                //  folderDelete(row)

                $('#feedbackFormModal').modal()
            }
        },

    ]
});