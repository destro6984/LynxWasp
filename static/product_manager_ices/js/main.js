$(function () {
// open popup window to add new message
    $('#checkout').click(function (e) {
        $('.bg-modal').css('display', 'flex')
    });

    $('.close').click(function () {
        $('.bg-modal').css('display', 'none')
    });
    // end


    //calculator for counting change
    var summm = $("#sumtopay").attr("value");
    $("#clientmoney").on("input", function () {
        var forclient = summm - $("#clientmoney").val();
        $('#clientchange').text(forclient + "zł");
    });
    // /end

    // quantity
    var quantity = $('.count');
    $('.plus').on('click', function () {
        quantity.val(parseInt(quantity.val()) + 1);
    });
    $('.minus').on('click', function () {
        quantity.val(parseInt(quantity.val()) - 1);
    });
// end
// adding scope by adding flavoures
    var type_ice_s = $("#scoope").prev("input[name='ice']").change(function (event) {
        if (type_ice_s.is(":checked")) {
            $('input[name=flavour]').click(function (event) {

                var input_flavour = $('input[name=flavour]:checked').length;
                $('.count').attr('value', input_flavour);

            });
        }
    });
    // adding thai ice limitation on 3 ices
    var type_ice = $("#thai").prev("input[name='ice']").change(function (event) {
        if (type_ice.is(":checked")) {
            $('input[name=flavour]').click(function (event) {
                $('.count').attr('value', 1);
                if ($('input[name=flavour]:checked').length >= 3) {
                    $("input:checkbox:not(:checked)").each(function () {
                        $(this).prop('disabled', true);
                    });
                } else {
                    $("input:checkbox:not(:checked)").each(function () {
                        $(this).prop('disabled', false);
                    });
                }

            });

        }
    });
// reset checkboxes after change
    $(".radio-toolbar input[name='ice']").change(function (event) {
        $('input[name=flavour]').prop("checked", false);
        $('.count').attr('value', 1);
    });


// end
// change number to status detail view
    sts = ($(".statusoforder"));
    switch (sts.text()) {
        case "1":
            sts.text('Started');
            break;
        case "2":
            sts.text('Postponed');
            break;
        case "3":
            sts.text('Finished');
            break;
    }
    // end


})
;