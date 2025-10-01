/*
        InsecureWebApp - an insecure Python/Flask Web application

        Copyright (C) 2024-2025  Kevin A. Lee (kadraman)

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

$.fn.SubscribeNewsletter = function (options) {
    const MIN_SUBSCRIBER_ID = 1000000
    const MAX_SUBSCRIBER_ID = 9999999;

    return this.each(function (index, el) {

        var settings = $.extend({
            color: "#556b2f",
            backgroundColor: "white"
        });

        var $this = $(this), $email = $this.find('#email-subscribe-input');
        $this.find('#email-subscribe-button').on('click', function () {
            if (_validateEmail($email.val())) {
                _saveEmail($email.val()).then(response => {
                    _showConfirmationText("Thank you your email address has been registered.", $email.val(), "text-success");
                }).catch(error => {
                    _showConfirmationText("Error registering email address:", $email.val(), "text-danger");
                });
            } else {
                _showConfirmationText("Invalid email address:", $email.val(), "text-danger");
            }
        });
    });

    function _showConfirmationText(text, email, cssClass) {
        const confirmationH5 = document.createElement("h4");
        confirmationH5.classList.add(cssClass);
        if (cssClass === 'text-danger') {
            confirmationH5.innerHTML = text + "<br/><br/><h5>" + email + "</h5>";
            console.error("ERROR: " + text)
        } else {
            confirmationH5.innerHTML = text
            console.log(text);
        }
        const confirmationDiv = document.createElement("div");
        confirmationDiv.classList.add("m-4", "text-center");
        confirmationDiv.appendChild(confirmationH5);
        $('#confirmation-modal').find('#confirmation-modal-body').empty().append(confirmationDiv);
        $('#confirmation-modal').modal('toggle');
        return confirmationDiv;
    }

    async function _saveEmail(email) {
        let subscriberId = Math.random() * (MAX_SUBSCRIBER_ID - MIN_SUBSCRIBER_ID) + MIN_SUBSCRIBER_ID;
        let data = JSON.stringify(
            {
                id: subscriberId,
                name: "",
                email: email,
                role: "ROLE_GUEST"
            }
        )
        return await $.ajax({
            url: '/api/users/subscribe-user',
            type: 'POST',
            contentType: 'application/json',
            data: data
        })
    }

    function _validateEmail(email) {
        var emailExpression = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        return emailExpression.test(email);
    }
};
