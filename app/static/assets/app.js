function getStatus() {
    $.get('/status/' + '?rnd=' + (new Date()).getTime())
        .done(function(html) {
            var files = $(html);
            files.find('.mdl-checkbox').each(function(i, elem){
                new MaterialCheckbox(elem)
            });
            $('.git__status').empty();
            $('.git__status').append(files)
        })
}

function enableSettings () {
    if ($('.services__select select').val() && $('.services__load-input').val()) {
        $('.services__settings').show();
    } else {
        $('.services__settings').hide();
    }
}

$(function(){
    getStatus();

    $('#service').on('change', function() {
        var sevrices = $('.service');
        sevrices.removeClass('service_shown_yes');
        $('.service_type_' + this.value).addClass('service_shown_yes');

        enableSettings();
    });

    $('.services__load-input').on('change', function(){
        var file = $(this).val(),
            text, paths, reg;

        if (file) {
            reg = new RegExp('/', 'g');
            paths = file.replace(reg, '\\').split('\\');
            text = paths[paths.length - 1];
        } else {
            text = 'Файл не выбран'
        }

        $('.services__image').text(text);

        enableSettings();

    });

    $('.services__upload').on('click', function(){
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
        })

        return false;
    })

    $('.git__checkout').on('click', function(){
        $.get('/checkout/'  + '?rnd=' + (new Date()).getTime())
        .done(function() {
            getStatus();
        })

        return false;
    })

    $('.git__commit').on('click', function(){
        var $form = $(this).parents('form');
        var formData = new FormData($form[0]);

        $.ajax({
            url: $form.attr('action'),
            type: $form.attr('method'),
            cache: false,
            processData: false,
            contentType: false,
            dataType: 'json',
            data: formData,
            headers: {
                'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()
            }
        })
        .done(function( data ) {
            //if (data.status && data.status === 'error') {
            //    var dialog = $('.popup');
            //    dialog.addClass('popup_shown_yes');
            //    $('.popup .popup__close').on('click', function() {
            //        dialog.removeClass('popup_shown_yes');
            //    })
            //}
            getStatus();
        })

        return false;
    })
})