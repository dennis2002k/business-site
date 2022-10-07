$(document).ready(function {
    $('form').on('submit', function(event) {
        $.ajax({
            data: {
                date: $("#result").val(),

            },
            type: 'POST',
            url: '/datepicker'

        })
        .done(function(data) {

            $("#here").text(data.times).show();

        })

        event.preventDefault();
    })
});