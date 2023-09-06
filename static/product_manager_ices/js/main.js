$(function () {
  //calculator for counting change
  var sumToPay = $("#sumtopay").attr("value");
  $("#clientmoney").on("input", function () {
    var forClient = sumToPay - $("#clientmoney").val();
    $("#clientchange").text(forClient + "zł");
  });
  // /end

  // quantity
  var quantity = $(".count");
  $(".plus").on("click", function () {
    quantity.attr("value", parseInt(quantity.val()) + 1);
  });
  $(".minus").on("click", function () {
    quantity.attr("value", parseInt(quantity.val()) - 1);
  });
  // end

  // Check if Opened Order
  var openOrderButton = $("#openedOrder");
  function isOrderOpened() {
    var orderItemForm = $("#orderitem-form");
    if (openOrderButton.length) {
      orderItemForm.toggleClass("fade-out");
    }
  }
  isOrderOpened();

  openOrderButton.on("click", function () {
    isOrderOpened();
  });

  // end
  // Adding ices
  var inputNameIce = $("input[name='ice']");
  var inputNameFlavour = $("input[name=flavour]");

  inputNameIce.on("change", function () {
    // reset checkbox after change
    resetCount();

    inputNameFlavour.on("click", addIce);
  });

  function resetCount() {
    inputNameFlavour.prop("checked", false);
    $(".count").attr("value", 1);
    inputNameFlavour.prop("disabled", false);
  }
  function addIce() {
    // adding thai ice
    if ($("#THAI").prev("input[name='ice']").is(":checked")) {
      $(".count").attr("value", 1);
      // only 3 flavours can be picked for Thai ice
      if ($("input[name=flavour]:checked").length >= 3) {
        $(":checkbox:not(:checked)").prop("disabled", true);
      } else {
        inputNameFlavour.prop("disabled", false);
      }
    }
    // adding scope depending on flavours number
    else if ($("#SCOOPE").prev("input[name='ice']").is(":checked")) {
      var inputFlavour = $("input[name=flavour]:checked").length;
      $(".count").attr("value", inputFlavour);
    }
  }

  // end
  // #Setting crsf token  for all ajax form django docs.#

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  var csrftoken = getCookie("csrftoken");

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
  });

  // end#
});
