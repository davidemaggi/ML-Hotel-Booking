$(function () {

    // init the validator
    // validator files are included in the download package
    // otherwise download from http://1000hz.github.io/bootstrap-validator

    $('#messaggio').hide();


    // when the form is submitted
    $('#form-prenotazione').on('submit', function (e) {

        var campo1 = $("#campo1").val();
        var campo2 = $("#campo2").val();
       

        var payload={"Campo1":campo1,"Campo2":campo2}



        // if the validator does not prevent form submit
        if (!e.isDefaultPrevented()) {
            var url = "./api/predictCancellazioni";

            // POST values in the background the the script URL
            $.ajax({
                type: "POST",
                url: url,
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                data: JSON.stringify(payload),
                success: function (data)
                {
                    // data = JSON object that contact.php returns

                    // we recieve the type of the message: success x danger and apply it to the 
                    var messageAlert = 'alert-' + data.type;
                    var messageText = data.message;

                    if(data.previsione){
                        $('#messaggio').addClass("alert-danger");
                    }else{
                        $('#messaggio').addClass("alert-success");
                    }
                    

                    

                    $('#risultato').html(`Questa Prenotazione ${data.previsione?"verrà":"non verrà"} cancellata.`);
                    $('#certezza').css('width', Math.floor(data.certezza*100)+'%').attr('aria-valuenow', Math.floor(data.certezza*100)); 
                    $('#certezza').text(Math.floor(data.certezza*100)+'%'); 
                    $('#messaggio').show();
                    // let's compose Bootstrap alert box HTML
                    //alert(data)
                },
                complete: function(){
                  
                  }
            });
            return false;
        }
    })
});