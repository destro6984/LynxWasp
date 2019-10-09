$(function () {



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
        quantity.attr('value', parseInt(quantity.val()) + 1);
    });
    $('.minus').on('click', function () {
        quantity.attr('value', parseInt(quantity.val()) - 1);
    });
// end
// Adding ices

    $("input[name='ice']").change(function () {
        // reset checkboxe after change
        $('input[name=flavour]').prop("checked", false);
        $('.count').attr('value', 1);
        $('input[name=flavour]').prop("disabled", false);

        $('input[name=flavour]').click(function () {
            // adding thai ice
            if ($("#thai").prev("input[name='ice']").is(":checked")) {
                $('.count').attr('value', 1);
                // only 3 flavoures can be picked for Thai ice
                if ($('input[name=flavour]:checked').length >= 3) {
                    $(':checkbox:not(:checked)').prop('disabled', true);
                } else {
                    $('input[name=flavour]').prop("disabled", false);
                }
            }
            // adding scope depending on flavoures number
            else if ($("#scoope").prev("input[name='ice']").is(":checked")) {
                var input_flavour = $('input[name=flavour]:checked').length;
                $('.count').attr('value', input_flavour);

            }
        });

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