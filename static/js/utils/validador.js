/**
 * Validador de formularios
 * 
 * se valida según la etiqueta class
 * 
 * <input id="nombre" name="nombre" type="text" class="required numeric show-error"/>
 * <span class="help-error" id="err_nombre"></span>
 * 
 * Muestra los errores en una etiqueta con el id 
 * de la manera err_IdDelInput
 *
 * Copyright (c) 2013 Dailyscript - Team. http://dailyscript.com.co
 * Dual licensed under the MIT and GPL licenses:
 * http://www.opensource.org/licenses/mit-license.php
 * http://www.gnu.org/licenses/gpl.html
 * 
 * Dev languages by: Angel Sullon @asullom
 */

//Array.prototype.inToArray = function(valor) { var i; for (i = 0; i < this.length; i++) { if (this[i] === valor) return true;} return false;};
/*
var elementosErr = []; 
//Tipo de validaciones, cada validación en el array corresponde a un método
var validaciones = ["requerido",'numeric','integer','ipv4'];
*/
var elemErr = [];
var tagsForm = ["input", "select", "textarea", "button"];
var validators = ["input-required", "input-alphanum", "input-list", "input-numeric", "input-integer", "input-user", "input-pass"];

(function($)
{     
    $.FormsValidation = {

        language:null,
validForm: function (form, confirmation) { 

    if(confirmation!= false) {        
        if(!confirm(translation.ugettext("You is sure to continue the operation?."))) {
            return false;
        }        
    }    
    var enviar = true
    var form = $('form[name="'+form+'"]');
    var cont = 0;
    var campos = tagsForm.length;
    var first_input;    
    for(i = 0 ; i < campos ; i++) {                 
        form.find(tagsForm[i]).each(function(k) {
            var input = $(this);
            //alert(input.attr('name'));
            if(input.attr('class') == undefined) {
                return true;
            }            
            var clases = input.attr('class').split(' ');
            for(c = 0 ; c < clases.length ; c++) {
                if($.inArray(clases[c], validators) >= 0) {
                    tmp = clases[c].split('-');
                    if(tmp[1] == undefined || tmp[1] == null || tmp[1] == '') {
                        continue;
                    }                    
                    fn = '$.FormsValidation.input'+ucFirst(tmp[1])+'("'+input.attr("id")+'")';                         
                    contenedor = input.parent();
                    if(contenedor.hasClass('controls')) {
                        contenedor = contenedor.parent();
                    }
                    if (!eval(fn)) {
                        elemErr.push("err_" + input.attr("id"));                     
                        if(contenedor.hasClass('controls') || contenedor.hasClass('control-group')) {
                            contenedor.addClass('control-error');
                        }                        
                        if(cont == 0) {
                            first_input = input;
                        }
                        cont++;
                    } else {                        
                        if(contenedor.hasClass('controls') || contenedor.hasClass('control-group')) {
                            contenedor.removeClass('control-error'); 
                        }                                                        
                    }
                }
            }            
        });        
    }    
    if (cont > 0) {
        enviar = false;
        try {
            errorForm();
        } catch(e) {
            
            alert(''+translation.ugettext("Errors found while processing the form. Please check the data and try again.")+'');            
        }
        try { 
            limpiarClaves(); 
        } catch(e) { }
        setTimeout(function(){ first_input.focus(); }, 2500);
        return false;
    }    
    if(enviar) {
        //@see var,js
        DwSpinner('show');
    }    
    return enviar;
},
inputRequired: function (input) {      
    field = $('#'+input);
    if (field.val() == null || field.val().length == 0 || /^\s+$/.test(field.val()) ) {
        $("#err_"+input).html(''+translation.ugettext("Required field.")+'');
        return false;
    }
    $("#err_"+input).html('');
    return true;
},

inputList: function (input) {
    field = $('#'+input);
    if (field.val() == null || field.val().length == 0 || /^\s+$/.test(field.val()) ) {
        $("#err_"+input).html(''+translation.ugettext("Select an item from the list.")+'');
    return false;
    }
    $("#err_"+input).html('');
    return true;
},


inputAlphanum: function (input) {
    field = $('#'+input);
    if (!(field.val() == null || field.val().length == 0 || /^\s+$/.test(field.val()))) {
        if (!(/^[a-zA-Z0-9-ZüñÑáéíóúÁÉÍÓÚÜ._\s]+$/.test(field.val()))) {            
            $("#err_"+input).html(''+translation.ugettext("Enter only alphanumeric values.")+'');
            return false;
        } else {
            $("#err_"+input).html('');
            return true;
        }
    } else { return true; }
},

inputNumeric: function (input) {
    field = $('#'+input);
    if (!(field.val() == null || field.val().length == 0 || /^\s+$/.test(field.val()))) {
        if (! (/^[-]?\d+(\.\d+)?$/.test(field.val()))) {            
            $("#err_"+input).html(''+translation.ugettext("Enter only numeric values.")+'');
            //$("#err_"+input).html(''+translation.ugettext("The user must have between %s and %s characters.","4","12")+'');
            return false;
        } else {            
            $("#err_"+input).html('');
            return true;
        }
    } else {
        return true;
    }
},

inputUser: function (input) {    
    var minLength = 4;
    var maxLength = 15;
    field = $('#'+input);
    if (field.val() == null || field.val().length == 0 ||/^[a-z0-9_]$/.test(field.val()) ) {
        $("#err_"+input).html(''+translation.ugettext("Required field.")+'');
        return false;
    }
    if(!$.FormsValidation.inputAlphanum(input)){
       return false; 
    }
    if(field.val().length >= minLength && field.val().length <= maxLength) {
        $("#err_"+input).html('');
        return true;
    } else {
        $("#err_"+input).html(''+translation.ugettext("The user must have between %s and %s characters.",minLength, maxLength)+'');
        return false;
    }
    $("#err_"+input).html('');
    return true;    
},

inputPass: function (input) {
    field = $('#'+input);
    var minLength = 5;    
    if (!(field.val() == null || field.val().length == 0 || /^\s+$/.test(field.val()))) {
        if ( $.FormsValidation.inputAlphanum(input) ) {
            if ( (field.val().length >= minLength) ) {                
                //Verifico si existe el input-repass
                if($(".input-repass").size() > 0) {
                    refield = $('.input-repass:first');
                    if(refield.val() !== field.val() ) {
                        $("#err_"+input).html(''+translation.ugettext("Passwords do not match.")+'');
                        return false;
                    } else {
                        $("#err_"+refield.attr('id')).html('');
                    }               
                }
                $("#err_"+input).html('');
        return true;
            } else {
                $("#err_"+input).html(''+translation.ugettext("The password must be at min %s characters.",minLength)+'');
        return false;
            }
    } else {
            $("#err_"+input).html(''+translation.ugettext("You have entered an invalid character.")+'');            
            return false;
    }
    } else { return true; }
},
/**
         * Inicializa el plugin
         *
         */
        initialize: function(lang) {
            // Obtiene el language
            
            this.language  = lang; //es-pe
            
        },
        /**
         * choise language
         *
         */
        setLanguage: function(lang) {
            
            $.FormsValidation.language  = lang; //es-pe
        }

    }
    // Inicializa el plugin
    $.FormsValidation.initialize('en-us');//es-pe
    
    var translation=$.FormsValidation.translation = {
        trans: 
        {
            'en-us': 
            {
                "You is sure to continue the operation?.":"You is sure to continue the operation?.",
                "Errors found while processing the form. Please check the data and try again.":"Errors found while processing the form. Please check the data and try again.",
                "Required field.":"Required field.",
                "Select an item from the list.":"Select an item from the list.",
                "Enter only alphanumeric values.":"Enter only alphanumeric values.",
                "Enter only numeric values.":"Enter only numeric values.",
                "Passwords do not match.":"Passwords do not match.",
                "You have entered an invalid character.":"You have entered an invalid character.",

                "The user must have between %s and %s characters.":"The user must have between %s and %s characters.",
                "The password must be at min %s characters.":"The password must be at min %s characters.",
            
            },
        },
        ugettext: function() {
            lang_objx = $.FormsValidation.language;
            var cadena = arguments[0];
            if (typeof this.trans[lang_objx] !== "undefined") {
                cadena = this.trans[lang_objx][cadena];
            }
           if(typeof cadena == "undefined") cadena = arguments[0];
            total = arguments.length;
            for(i=1;i<total;i++) {
              valor = arguments[i];
              cadena = cadena.replace("%s", arguments[i]);
            }
            return cadena;
        }
    }

})(jQuery);





/*
function alfabetico(valor, idEtiqueta) {
    if (!(valor == null || valor.length == 0 || /^\s+$/.test(valor))) {
        if (!(/^[a-zA-ZüñÑáéíóúÁÉÍÓÚÜ\s]+$/.test(valor))) {
            document.getElementById(idEtiqueta).innerHTML = 'Introduzca solo valores alfabéticos';
            return false;
        } else {
            document.getElementById(idEtiqueta).innerHTML = '&nbsp;';
            return true;
        }
    } else { return true; }
}



function texto(valor, idEtiqueta) {
    if (!(valor == null || valor.length == 0 || /^\s+$/.test(valor))) {
	if (!(/^[a-z0-9\sÁÉÍÓÚÑáéíóúñ.,_:;\-\&\=\*\+\/\#\%\$\"\(\)\@\/]+$/i.test(valor))) {
            document.getElementById(idEtiqueta).innerHTML = 'Ha introducido un caracter no válido';
            return false;
	} else {
            document.getElementById(idEtiqueta).innerHTML = '&nbsp;';
            return true;
	}
    } else {        
        return true;
    }
}

function slug(valor, idEtiqueta) {
    return texto(valor,idEtiqueta);
}

function fecha(valor, idEtiqueta) {    
    if (!(valor == null || valor.length == 0 || /^\s+$/.test(valor))) {                         
        if ( !(/^[-]?\d+(\.\d+)?$/.test(valor)) && !(/^\d{2,4}\/\d{1,2}\/\d{1,2}$/.test(valor)) ){
            document.getElementById(idEtiqueta).innerHTML = '&nbsp;';
            return true;
	} else {
            document.getElementById(idEtiqueta).innerHTML = 'Fecha incorrecta. AAAA-MM-DD';
            return false;
	}
    } else { return true; }
}









function pass(valor, idEtiqueta) {
    var limite = 6;
    if (!(valor == null || valor.length == 0 || /^\s+$/.test(valor))) {
        if ( alfanumerico(valor,idEtiqueta) ){
            if ((valor.length >= limite) ) {
                document.getElementById(idEtiqueta).innerHTML = '&nbsp;';
		return true;
            } else {
                document.getElementById(idEtiqueta).innerHTML = 'La contraseña debe tener entre mínimo '+limite+' caracteres';
		return false;
            }
	} else {
            document.getElementById(idEtiqueta).innerHTML = 'Haz introducido un caracter no válido';
            return false;
	}
    } else { return true; }
}

function numerico(valor, idEtiqueta) {
    if (!(valor == null || valor.length == 0 || /^\s+$/.test(valor))) {
        if (! (/^[-]?\d+(\.\d+)?$/.test(valor)) ) {
            document.getElementById(idEtiqueta).innerHTML = 'Introduzca solo valores numéricos';
            return false;
        } else {            
            document.getElementById(idEtiqueta).innerHTML = '&nbsp;';
            return true;
        }
    } else {
        return true;
    }
}

function entero(valor, idEtiqueta) { 
    if (!(valor == null || valor.length == 0 || /^\s+$/.test(valor))) {
        if (!(/^(?:\+|-)?\d+$/.test(valor))) {
            document.getElementById(idEtiqueta).innerHTML = 'El número debe ser entero';
            return false;
        } else {
            document.getElementById(idEtiqueta).innerHTML = '&nbsp;';
            return true;
        }
    } else {
        return true;
    }
}

function telefono(valor, idEtiqueta) {
    var limiteMenor = 7;
    var limiteMayor = 10;
    if (!(valor == null || valor.length == 0 || /^\s+$/.test(valor))) {        
        if(numerico(valor,idEtiqueta) && entero(valor, idEtiqueta)) {
            if ((valor.length == limiteMenor) || (valor.length == limiteMayor)) {
                document.getElementById(idEtiqueta).innerHTML = '&nbsp;';
                return true;
            } else {
                document.getElementById(idEtiqueta).innerHTML = 'El número debe tener de 7 o 10 dígitos';
                return false;
            }
        } else {
            return false;
        }
    } else {
        return true;
    }
}

function url(valor, idEtiqueta) { if (!(valor == null || valor.length == 0 || /^\s+$/.test(valor))) { if (!(/^(ht|f)tp(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)( [a-zA-Z0-9\-\.\?\,\'\/\\\+&%\$#_]*)?$/.test(valor))) { document.getElementById(idEtiqueta).innerHTML = 'La página web no es válida'; return false; } else { document.getElementById(idEtiqueta).innerHTML = '&nbsp;'; return true; } } else { return true; } }
function email(valor, idEtiqueta) { if (!(valor == null || valor.length == 0 || /^\s+$/.test(valor))) { if (!(/^([a-zA-Z0-9_\.\-])+(\+[a-zA-Z0-9]+)*\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/.test(valor))) { document.getElementById(idEtiqueta).innerHTML = 'El formato del e-mail no es válido'; return false; } else { document.getElementById(idEtiqueta).innerHTML = '&nbsp;'; return true; } } else { return true; } }


function celular(valor, idEtiqueta) { var tamano = 10; if (!(valor == null || valor.length == 0 || /^\s+$/.test(valor))) { if(numerico(valor,idEtiqueta) && entero(valor, idEtiqueta)) { if (valor.length == tamano) { document.getElementById(idEtiqueta).innerHTML = '&nbsp;'; return true; } else { document.getElementById(idEtiqueta).innerHTML = 'El número debe tener 10 dígitos'; return false; } } else { return false; } } else { return true; } }
function fotografia(file, idEtiqueta) {var ext;if (!(file == null || file.length == 0 || /^\s+$/.test(file))) {ext = getFileExtension(file);if(ext != "jpeg" && ext != "jpg" && ext != "png" && ext != "gif") {document.getElementById(idEtiqueta).innerHTML = 'Formato de imagen no válido.';return false;} else {document.getElementById(idEtiqueta).innerHTML = '&nbsp;';return true;}} else { return true; }}
function getFileExtension(filename) {var i = filename.lastIndexOf(".");return (i > -1) ? filename.substring(i + 1, filename.length).toLowerCase() : "";}
function ipv4(valor, idEtiqueta) { var patronIp = new RegExp("^([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3}).([0-9]{1,3})$"); if (!(valor == null || valor.length == 0 || /^\s+$/.test(valor))) { if (!(patronIp.test(valor))) { document.getElementById(idEtiqueta).innerHTML = 'Dirección Ipv4 no válida'; return false; } else { valores =   valor.split("."); if(valores[0]<=255 && valores[1]<=255 && valores[2]<=255 && valores[3]<=255) { document.getElementById(idEtiqueta).innerHTML = '&nbsp;'; return true; } else { document.getElementById(idEtiqueta).innerHTML = 'Rango de dirección no válido'; return false; } } } else { return true; } }
*/
function limpiarErr() { var total = elementosErr.length;for (var i = 0; i < total; i++)document.getElementById(elementosErr.shift()).innerHTML = '&nbsp;';}
function ucFirst(string){ return string.substr(0,1).toUpperCase()+string.substr(1,string.length).toLowerCase(); }




function validFormXXXXXXXXXXXXX(form, confirmation) { 
    /*
    var form = $('form[name="'+form+'"]');
    form.find("input").each(function(k) {
        var input = $(this);
        alert(input.attr('name'));
    });
*/
    if(confirmation!= false) {        
        if(!confirm('Está seguro de continuar con la operación?')) {
            return false;
        }        
    }    
    var enviar = true
    var form = $('form[name="'+form+'"]');
    var cont = 0;
    var campos = tagsForm.length;
    var first_input;    

    form.find("input").each(function(k) {
            var input = $(this);
            alert(input.attr('name'));
            if(input.attr('class') == undefined) {
                return true;
            }            
                       
            var clases = input.attr('class').split(' ');
            
            
    });
    
}