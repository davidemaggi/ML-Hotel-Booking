$(function () {
    $('#datepicker').datepicker({
        language: "it"
    });
    // init the validator
    // validator files are included in the download package
    // otherwise download from http://1000hz.github.io/bootstrap-validator

    $('#messaggio').hide();


    // when the form is submitted
    $('#form-prenotazione').on('submit', function (e) {

        var hotel = $("#PrenotazioneHotel").val();
        var dataArrivo = $("#DataPrenotazioneArrivo").val();
        var dataPartenza = $("#DataPrenotazionePartenza").val();
        var adulti = parseInt($("#PrenotazioneAdulti").val());
        var bambini = parseInt($("#PrenotazioneBambini").val());
        var infant = parseInt($("#PrenotazioneInfant").val());
        var camera = $("#PrenotazioneCamera").val();
        var speciali = $("#PrenotazioneSpeciali").val();
        var trattamento = $("#PrenotazioneTrattamento").val();
        var postiAuto = parseInt($("#PrenotazionePostiAuto").val());
       

        var payload={
            "PrenotazioneHotel":hotel,
            "DataPrenotazioneArrivo":dataArrivo,
            "DataPrenotazionePartenza":dataPartenza,
            "PrenotazioneAdulti":adulti,
            "PrenotazioneBambini":bambini,
            "PrenotazioneInfant":infant,
            "PrenotazioneCamera":camera,
            "PrenotazioneSpeciali":speciali.length,
            "PrenotazioneTrattamento":trattamento,
            "PrenotazionePostiAuto":postiAuto,
            }

            

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
                    

                    if(data.previsione){
                        $('#messaggio').removeClass("alert-success");
                        $('#messaggio').addClass("alert-danger");
                    }else{
                        $('#messaggio').addClass("alert-success");
                        $('#messaggio').removeClass("alert-danger");
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