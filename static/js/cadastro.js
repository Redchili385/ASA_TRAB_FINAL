$(function() {
    $("#form_cadastro").submit(function(e) {

        e.preventDefault(); // avoid to execute the actual submit of the form.

        var form = $(this);
        var url = form.attr('action');

        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(), // serializes the form's elements.
            success: function(data)
            {
                console.log(data)
                resultado = JSON.parse(data)
                console.log(resultado)
                if(resultado["cadastrado"] == '1')
                    alert('Cadastrado'); // show response from the php script.
                else
                    alert('Erro no cadastro')
            }
            });
    });
});