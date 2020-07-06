$(function () {
    
    
    //$("#DataPrenotazioneArrivo").val(new date());
    //$("#DataPrenotazionePartenza").val(new date());
    
    
    
    $('#datepicker').datepicker({
        format: "dd/mm/yyyy"
        
    });
    // init the validator
    // validator files are included in the download package
    // otherwise download from http://1000hz.github.io/bootstrap-validator

    function calcolaPrezzo() {

        var prezzo = 0;


        var camera = $("#PrenotazioneCamera").val();
        var speciali = $("#PrenotazioneSpeciali").val().length;
        var trattamento = $("#PrenotazioneTrattamento").val();
        var tipoCliente = $("#PrenotazioneTipoCliente").val();
        prezzo = 90;
        if (camera == "B") { prezzo = 100; }
        if (camera == "C") { prezzo = 110; }
        if (camera == "D") { prezzo = 120; }
        if (camera == "E") { prezzo = 130; }
        if (camera == "F") { prezzo = 140; }
        if (camera == "G") { prezzo = 150; }
        if (camera == "H") { prezzo = 160; }
        if (camera == "L") { prezzo = 170; }
        if (camera == "P") { prezzo = 180; }

        prezzo += speciali * 8;


        if (trattamento == "FB") { prezzo += 20; }
        if (trattamento == "HB") { prezzo += 10; }
        if (trattamento == "BB") { prezzo += 5; }
        if (trattamento == "SC") { prezzo += 0; }


        if (tipoCliente == "Group") { prezzo -= prezzo * 0.2; }
        if (tipoCliente == "Transient") { prezzo = prezzo; }
        if (tipoCliente == "Contract") { prezzo -= prezzo * 0.30; }



        return prezzo;
    }


    $('#messaggio').hide();

    $("#PrenotazioneCamera").on("change", function () {
       $('#PrenotazionePrezzo').attr("value", calcolaPrezzo());
    });


    $("#PrenotazioneTrattamento").on("change", function () {
        $('#PrenotazionePrezzo').attr("value", calcolaPrezzo());
     });

     $("#PrenotazioneSpeciali").on("change", function () {
        $('#PrenotazionePrezzo').attr("value", calcolaPrezzo());
     });

     $("#PrenotazioneTipoCliente").on("change", function () {
        $('#PrenotazionePrezzo').attr("value", calcolaPrezzo());
     });


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
        var prezzo = parseInt($("#PrenotazionePrezzo").val());
        var tipoCliente = $("#PrenotazioneTipoCliente").val();

        var payload = {
            "PrenotazioneHotel": hotel,
            "DataPrenotazioneArrivo": dataArrivo,
            "DataPrenotazionePartenza": dataPartenza,
            "PrenotazioneAdulti": adulti,
            "PrenotazioneBambini": bambini,
            "PrenotazioneInfant": infant,
            "PrenotazioneCamera": camera,
            "PrenotazioneSpeciali": speciali.length,
            "PrenotazioneTrattamento": trattamento,
            "PrenotazionePostiAuto": postiAuto,
            "PrenotazionePrezzo": prezzo,
            "PrenotazioneTipoCliente": tipoCliente,
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
                success: function (data) {


                    if (data.previsione) {
                        $('#messaggio').removeClass("alert-success");
                        $('#messaggio').addClass("alert-danger");
                    } else {
                        $('#messaggio').addClass("alert-success");
                        $('#messaggio').removeClass("alert-danger");
                    }




                    $('#risultato').html(`Questa Prenotazione ${data.previsione ? "verrà" : "non verrà"} cancellata.`);
                    $('#certezza').css('width', Math.floor(data.certezza * 100) + '%').attr('aria-valuenow', Math.floor(data.certezza * 100));
                    $('#certezza').text(Math.floor(data.certezza * 100) + '%');
                    $('#messaggio').show();
                    // let's compose Bootstrap alert box HTML
                    //alert(data)
                },
                complete: function () {

                }
            });
            return false;
        }
    })
});