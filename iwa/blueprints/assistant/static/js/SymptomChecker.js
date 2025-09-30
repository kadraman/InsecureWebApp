
$.fn.SymptomChecker = function (options) {

    return this.each(function (index, el) {

        console.log("Initializing Symptom Checker");
        var settings = $.extend({
            url: "",
            method: "POST",
            dataType: "json"
        }, options);

        alert("URL: " + settings.url + ", Method: " + settings.method + ", DataType: " + settings.dataType);
        var $this = $(this);

        $this.find('#symptom-checker-button').on('click', function () {
            alert("Not implemented yet.");
        });

    });

};