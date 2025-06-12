
document.addEventListener('DOMContentLoaded', function () {

    // animate out any auto dismiss alerts
    /*var autoDismiss = function() {
        $(".auto-dismiss").each(function (i, obj) {
            let self = this;
            setTimeout(function() {
                $(self).fadeTo(2000, 500).slideUp(500, function () {
                    $(self).slideUp(500);
                })
            });
        });
    }
    autoDismiss();*/

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        //form.classList.add('was-validated')
      }, false)
    })

    // offcanvas navbar and user account menu
    var userAccountMenu = document.getElementById("offcanvasUserAccount");
    var myOffcanvas = document.getElementById('offcanvasDarkNavbar')
    myOffcanvas.addEventListener('hidden.bs.offcanvas', 
    function () {
        userAccountMenu.classList.add("text-end");
    })

    var myOffcanvas = document.getElementById('offcanvasDarkNavbar')
    myOffcanvas.addEventListener('show.bs.offcanvas', 
    function () {
        userAccountMenu.classList.remove("text-end");
    })

}, false);