
function animate(target, animation) {
    const square = document.querySelector(target);
    square.classList.remove(animation);

    // Create the observer, same as before:
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          square.classList.add(animation);
          return;
        }
        // Remove the transition class
        // square.classList.remove(animation);
      });
    });

    observer.observe(document.querySelector(target));
  }

 // Animate MG section
 animate(".sd-col:nth-child(1)", "animation")
 animate(".sd-col:nth-child(2)", "animation")
 animate(".sd-col:nth-child(3)", "animation")

 // Agency
 animate(".agency-animation:nth-child(1)", "animation")
 animate(".agency-animation:nth-child(2)", "animation")

 // We do
 animate(".we-do-animation:nth-child(1)", "animation")
 animate(".we-do-animation:nth-child(2)", "animation")
 animate(".we-do-animation:nth-child(3)", "animation")

 // Vision
 animate(".vision-animation:nth-child(1)", "animation")
 animate(".vision-animation:nth-child(2)", "animation")

 // talking
 animate(".talk-animation:nth-child(1)", "animation")
 animate(".talk-animation:nth-child(2)", "animation")




$(document).ready(function () {

    // popover
    var popover = new bootstrap.Popover(document.querySelector('.time-popover'), {
        container: 'body'
    })

    var time = undefined;
    var date = $("#result").val();
    console.log("hi there");


    $(".btn-check").click(function () {
        time = $(this).next("label").text();
        $("#submit-btn").removeAttr("disabled");
        $(".time-popover").popover('dispose');


        $(".btn-check").next("label").css("background-color", "");
        $(".btn-check").next("label").css("color", "");

        console.log(time);

    })

    // disable non available times
    $(".rd-day-body").click(function () {
        console.log("hi there again")
        this.click();

        // reset times choices
        time = undefined;
        $("#submit-btn").attr("disabled", "disabled")
        var popover = new bootstrap.Popover(document.querySelector('.time-popover'), {
            container: 'body'
        })
        $(".btn-check").next("label").css("background-color", "white");
        $(".btn-check").next("label").css("color", "black");

        console.log(time);
        $.ajax({
                data: {
                    date: $("#result").val(),
                },
                type: "POST",
                url: "/datepicker",
            })
            .done(function (data) {
                for (let i = 0; i < 9; i++) {
                    $("#time" + (i + 1)).removeAttr('disabled');
                    if (data.times[i] == "True") {
                        name = $("#time" + (i + 1)).attr('disabled', 'disabled');
                        console.log(name)
                    }
                }
            })

        event.preventDefault();
    })

    // submit final meeting date
    $(".set-meeting-btn").click(function () {
        var new_date = $("#result").val();
        var email = $("#email").val();
        var phone_number = $("#phone-number").val();

        if (email == "" && phone_number == "") {
            $("#fail-alert").removeAttr("hidden")
        } else {
            $("#fail-alert").attr("hidden", true)
            $("#success-alert").removeAttr("hidden")
            $.ajax({
                    data: {
                        date: new_date,
                        time: time,
                        email: email,
                        phone_number: phone_number
                    },
                    type: "POST",
                    url: "/submit_meeting"
                })
                .success(function () {
                    // do sth here
                })
        }


    })


});





