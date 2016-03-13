$(function(){
    $('#service').on('change', function() {
        var sevrices = $('.service');
        sevrices.removeClass('service_shown_yes');
        $('.service_type_' + this.value).addClass('service_shown_yes');
    })
})