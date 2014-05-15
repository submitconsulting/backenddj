/**
* 
* Dev languages by: Angel Sullon @asullom
*/
        function getCookie(name) 
        {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') 
            {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) 
                {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) 
                    {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
        return cookieValue;
        }
        function setCsrfToken() {
            $( "#csrfmiddlewaretoken" ).val(getCookie('csrftoken'));
        }
    //TODO: onsubmit="setCsrfToken()" para el search

(function($)
{     
    $.fn.dwGrid = function(method){ 
                
        if ( methods[method] ) {  
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));  
        } else if ( typeof method === 'object' || ! method ) {  
            return methods.init.apply( this, arguments );  
        } else {  
            $.error( 'Este método ' +  method + ' no existe en jQuery.dwGrid' );  
            return false;
        }



    }; 
    
    
    

    var methods = {  
        //languagem  : null,
        init : function( options ) { 
                    //Defino unas opciones por defecto
                    var opt = {           
                        language        : 'es-pe',             
                        form_search     : false,
                        form_action     : '',
                        form_col        : 'data-search',
                        form_attr       : 'class="dw-form js-remote form-search"',
                        order_attr      : 'class="dw-ajax data-order dw-spinner"',
                        col_collapse    : 'col-collapse',
                        order_action    : '',
                        contenedor      : 'dw-shell-content',
                        form_load_data  : 'dw-shell-content'   
                    }            
                    //methods.languagem = opt.language;

                    $.extend(opt, options); //Extiende las opciones recibidas con las default
                    
                    $.ajaxSetup({ //Permite la busqueda autorixando el CSRFToken
                        beforeSend: function(xhr, settings) {
                            if(settings.type == "POST")
                            {
                                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                            }
                        }
                    });
                    return this.each(function(k) {  
                        
                        var table = $(this); //Tomamos el objeto tansformado en jquery                                                                                        
                        
                        thead = table.find("thead");
                        tbody = table.find("tbody");
                        hdrCols = thead.find("th");
                        bodyRows = tbody.find("tr");                                                
                        
                        if(table.parent().hasClass('dw-overflow')) {                             
                            container = table.parent().prev().hasClass('btn-toolbar') ? table.parent().prev() : $('<div class="btn-toolbar btn-toolbar-top"></div>');
                        } else {
                            container = table.prev().hasClass('btn-toolbar') ? table.prev() : $('<div class="btn-toolbar btn-toolbar-top"></div>');
                        }                                                
                        
                        containerCol = $('<div class="pull-right"><div class="btn-group"><button class="btn btn-only dropdown-toggle" data-toggle="dropdown"><span class="hidden-tablet hidden-phone"> '+translation.ugettext(opt.language,"COLUMNS")+' <i class="caret"></i></span><span class="hidden-desktop"><i class="icon-th"></i></span></button><ul class="dropdown-menu pull-right" /></div></div>');
                        
                        var th_responsive = [];
                        
                        hdrCols.each(function(i) {  
                            
                            var th = $(this), classes = th.attr("class");
                            //Se asigna un id a la colomna definida en el thead                            
                            var id = "col-"+k+"-"+ i;
                            th.attr("id", id);   
                                                        
                            if(!th.hasClass('no-responsive')) {
                                th_responsive.push('td:nth-of-type('+(i+1)+'):before { content: "'+th.text()+': "; }');
                            }
                                                        
                            // Hay que revisar los colspan
                            bodyRows.each(function(){
                                var cell = $(this).find("th, td").eq(i);                        
                                cell.attr("headers", id);                                
                                if (classes) { cell.addClass(classes); };
                                
                                if(opt.order_action!='') {
                                    if(th.attr('data-search')!=undefined) {                                    
                                        text = th.text();
                                        order = th.attr('data-search');
                                        asc = opt.order_action+''+order+'/';
                                        desc = opt.order_action+'-'+order+'/';
                                        cell.append('<div class="btn-group hidden-desktop"><a class="" data-toggle="dropdown" href="#"><span class="caret"></span></a><ul class="dropdown-menu pull-right"><li><a href="'+asc+'" '+opt.order_attr+' data-div="'+opt.contenedor+'"><i class="icon-caret-up icon-expand"></i>'+translation.ugettext(opt.language,"Ascending")+'</a></li><li><a href="'+desc+'" '+opt.order_attr+' data-div="'+opt.contenedor+'"><i class="icon-caret-down icon-expand"></i>'+translation.ugettext(opt.language,"Descending")+'</a></li></ul></div>');
                                    }
                                }
                                
                            });  
                                                        
                            // Creo las columnas para mostrar/ocultar 
                            if (opt.col_collapse && th.hasClass(opt.col_collapse) ) {
                                //Regisro las columnas
                                text = th.text();
                                text = text.substr(0,1).toUpperCase()+text.substr(1,text.length).toLowerCase();
                                var toggle = $('<li><label class="checkbox" for="toggle-col-'+i+'">'+text+'<input type="checkbox" name="toggle-cols" id="toggle-col-'+i+'" value="'+id+'" /></label></li>');
                                //Agrego las columnas que se pueden ocultar
                                containerCol.find("ul").append(toggle);                                 
                                toggle.find("input").change(function(){                                    
                                    var input = $(this), 
                                    val = input.val(), 
                                    cols = $("#" + val + ", [headers="+ val +"]", table);	                                                   
                                    (input.is(":checked")) ? cols.removeClass('hidden').css('display','block') : cols.addClass('hidden').css('display','none');
                                    //(input.is(":checked")) ? cols.attr('style', 'display: block !important'): cols.css('display', 'none');
                                }).bind("updateCheck", function(){
                                    if (th.hasClass('hide')) {
                                        $(this).attr("checked", false);
                                    } else {
                                        $(this).attr("checked", true);
                                    }                                    
                                }).trigger("updateCheck");                                
                            }
                            
                            //Creo la opción para seleccionar el orden
                                                                             
                            
                        });
                        

                        
                        $('head').append('<style type="text/css">@media (max-width: 640px) { '+th_responsive.join('')+'}</style>');
                        
                        
                        if(opt.form_search) {
                            
                            if(opt.form_action==undefined || opt.form_action=='') {
                                alert('No se ha definido una url para la búsqueda para el datagrid');
                                exit();
                            }                               
                            var select = '';
                            
                            hdrCols.each(function(i) {
                                if(!$(this).hasClass('no-form-search')) {
                                    field = $(this).attr('data-search');
                                    if(field!=undefined) {
                                        //text = field.replace('_', ' ').replace('_', ' ').toLowerCase();
                                        //text = text.split('.');
                                        //text = (text.length > 1) ? text[1] : text[0];
                                        // las 3 lineas anteriores ya no se necesita
                                        text = $(this).text();
                                        text = DwUcFirst(text);
                                        select = (select!='') ? select+'<option value="'+field+'">'+text+'</option>' : '<option value="'+field+'">'+text+'</option>';
                                    }
                                }                                
                            }); 
                            
                            if(select=='') {
                                select = '<option value="">NO DISPONIBLE</option>';
                            }
                            
                            containerForm = '<div class="row-fluid form-search-container hidden"><form action="'+opt.form_action+'" method="post"  style-form="form-inline" '+opt.form_attr+' data-to="'+opt.form_load_data+'" ><div class="span3"><input type="hidden" name="csrfmiddlewaretoken" value="" /><select id="field" name="field"  class="field select input-medium">'+select+'</select></div> <div class="span3"><input id="value" name="value" type="text" value="" class="field text input-medium" placeholder="'+translation.ugettext(opt.language,"word or text")+'"/></div><div class="span2"><input type="submit" value="'+translation.ugettext(opt.language,"SEARCH")+'" class="btn btn-info btn-medium" /></div></form></div>';
                                                                                    
                        }

                        hdrCols.each(function(i) {  
                            
                            var th = $(this);
                            //Creo la opción para seleccionar el orden
                            if(opt.order_action!='') {
                                if(th.attr('data-search')!=undefined) {                                    
                                    text = th.text();
                                    order = th.attr('data-search');
                                    asc = opt.order_action+''+order+'/';
                                    desc = opt.order_action+'-'+order+'/';
                                    th.html('<div class="btn-group hidden-phone"><a class="" data-toggle="dropdown" href="#">'+text+' <span class="caret"></span></a><ul class="dropdown-menu"><li><a href="'+asc+'" '+opt.order_attr+' data-div="'+opt.contenedor+'"><i class="icon-caret-up icon-expand"></i>'+translation.ugettext(opt.language,"Ascending")+'</a></li><li><a href="'+desc+'" '+opt.order_attr+' data-div="'+opt.contenedor+'"><i class="icon-caret-down icon-expand"></i>'+translation.ugettext(opt.language,"Descending")+'</a></li></ul></div>');
                                }
                            }                                                  
                            
                        });
                        
                        (table.parent().hasClass('dw-overflow')) ? table.parent().before(container) : table.before(container);
                        
                        if(opt.col_collapse) {
                            container.prepend(containerCol);                                                
                        }                 
                        
                        if(!container.find('.btn-actions').length) {
                            container.append('<div class="btn-actions"></div>');
                        }                                                
                        
                        container.append('<hr class="divider">');                        
                        
                        if(opt.form_search) {
                            //$( "#csrfmiddlewaretoken" ).val(javascript:getCookie(name));
                            container.find('.btn-actions').prepend('<button class="btn btn-info dw-text-bold btn-form-search"><i class="btn-icon-only icon-search"></i> <span class="hidden-phone">'+translation.ugettext(opt.language,"SEARCH")+'</span></button>');
                            container.append(containerForm);                                                   
                            container.append('<hr class="divider hidden">');                        
                        }
                                                
                    });  
                                        
                } ,
        getLanguagem : function(  ) {
            return "";//methods.languagem;
        }

    };   

    var translation=$.fn.dwGrid.translation = {
    
        'en-us': 
            {
                "SEARCH":"SEARCH",
                "word or text":"word or text",
                "COLUMNS":"COLUMNS",
                "Ascending":"Ascending",
                "Descending":"Descending",

            },
        
        ugettext: function(lang_obj,cadena) {
            lang_obj = this[lang_obj];
            if (!(typeof lang_obj === "undefined")) {
                if (!(typeof lang_obj[cadena] === "undefined")) {
                    cadena = (lang_obj[cadena]);
                }
            }
            for(i=2;i<arguments.length;i++) {
                cadena = cadena.replace("%s", arguments[i]);
            }
            return cadena;

        }
    }    
    
         
    
})(jQuery);

$(function() {  
    
    $('body').on('click', '.btn-toolbar-top .btn-form-search', function() {          
        contenedor = $(this).parents('.btn-toolbar:first').find('.form-search-container:first'); 
        if(contenedor.hasClass('hidden')) {
            contenedor.removeClass('hidden').hide().fadeIn(250);
            contenedor.next('hr').removeClass('hidden').hide().fadeIn(250);
        } else {
            contenedor.fadeOut(50).addClass('hidden');
            contenedor.next('hr').fadeOut(50).addClass('hidden');                                        
        }
    });   
    
    $('body').on('click', '.table-responsive tbody tr', function() {          
        elem = $(this).find('td.btn-actions:first');
        accion = (elem.is(':hidden')) ? 'mostrar' : 'ocultar';         
        all = $(this).parent().find('td.btn-actions');
        all.each(function(){
            if(!$(this).is(':hidden')) { $(this).hide(); }
        });                
        (accion=='mostrar') ? elem.css('display','block') : elem.hide();                        
    });

 
    
})