function getStatus() {
    $.get('/status/')
        .done(function(html){
            var files = $(html);
            files.find('.mdl-checkbox').each(function(i, elem){
                new MaterialCheckbox(elem)
            });
            $('.git__status').empty();
            $('.git__status').append(files)
        })
}

$(function(){
    getStatus();

    $('#service').on('change', function() {
        var sevrices = $('.service');
        sevrices.removeClass('service_shown_yes');
        $('.service_type_' + this.value).addClass('service_shown_yes');
    })

    $('.services__load-input').on('change', function(){
        var $form = $(this).parents('form');
        var formData =  new FormData($form[0]);

        $.ajax({
            url: $form.attr('action'),
            type: $form.attr('method'),
            cache: false,
            processData: false,
            contentType: false,
            dataType: 'json',
            data: formData
        })
        .done(function( data ) {
            if (data.status && data.status === 'error') {
                var dialog = $('.popup');
                dialog.addClass('popup_shown_yes');
                $('.popup .popup__close').on('click', function() {
                    dialog.removeClass('popup_shown_yes');
                })
            }
            getStatus();

            //console.log(data)
        })
    })
})