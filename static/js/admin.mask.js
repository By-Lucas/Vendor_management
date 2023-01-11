$(document).ready(function ($) {
    $('.telephone').mask('(00) 00000-0000');
    $('.cep').mask('00000-000');
    $('.cpf').mask('000.000.000-00');
    $('.cnpj').mask('00.000.000/0000-00');

    //VERIFICA SE EXISTE CPF/CNPJ NO FORM - INICIO
    let cpfcnpj = $('.cpfcnpj');

    if (cpfcnpj.length) {
        let cpfcnpj_val = cpfcnpj.val();
        let options = {
            onKeyPress: function (cpfcnpj_val, e, field, options) {
                let masks = ['000.000.000-009', '00.000.000/0000-00'];
                let mask = (cpfcnpj_val.length > 14) ? masks[1] : masks[0];
                $('.cpfcnpj').mask(mask, options);
            }
        };

        if (cpfcnpj_val.length > 14) {
            cpfcnpj.mask('00.000.000/0000-00', options);
        } else {
            cpfcnpj.mask('000.000.000-00', options);
        }

    }
    //VERIFICA SE EXISTE CPF/CNPJ NO FORM - FIM

});