Backend Manager for Django
======================

Módulo Backend para aplicaciones web SaaS seguras escritas en Django y con la elegancia de Bootstrap.

Por medio del BackendDJ podrás gestionar las diferentes partes del sistema: usuarios, perfiles, recursos, permisos, módulos, planes SaaS, menús, asociaciones, empresas, sedes, logs, seguridad, internacionalización y mucho más!.

Ahora, cuando inicias un proyecto comenzarás directamente a atender(implementar) los requisitos de tu nuevo sistema, ya que BackendDJ se encargó de todo el trabajo inicial repetitivo de todo proyecto de software así como de los componentes o librerías que necesitas antes de comenzar a desarrollar una aplicación web moderna y segura.

BackendDJ es el entregable más importante de todo UN MARCO DE TRABAJO para desarrollar app WEB MODERNAS Y SEGURAS denominado "ScrumSAD".


Documentación
-------------------

`Diseño UML <http://backenddj-model.appspot.com>`_

`Guía del desarrollador en PDF <https://github.com/submitconsulting/backenddj/blob/master/project/manuales/BackendDJ-devguide.pdf?raw=true>`_

`Demo en línea <http://dbackend.python.org.pe>`_
-------------------

Usuario: admin

Pass: 12345


Instalación
-------------------
Para instalar el BackendDJ simplemente lo descargas e instale los requerimientos de test ejecutando (dentro de la carpeta backenddj) el siguiente comando:
::
	backenddj>pip install -r project/requirements/test.txt


Requirements

Python 2.7.6

Django==1.6.2

PIL==1.1.7

To install `admin doc utils <http://sourceforge.net/projects/docutils/files/docutils/0.11/docutils-0.11.tar.gz/download?use_mirror=ufpr&download=>`_
run the following command:
::
	docutils-0.11>python setup.py install



Local Run
-------------------

To exec webapp, run the following command:
::
	backenddj>python manage.py runserver

Usuario: admin

Pass: 12345


Unit testing
-------------------

To exec unit test, run the following command:
::
	backenddj>python manage.py test apps.params.tests.ParamsViewsTestCase.test_locality_index


Backup/load database
-------------------
See in the settings.py setting for FIXTURE_DIRS
::
	>python manage.py dumpdata > fixtures/testdata.json
	>python manage.py loaddata testdata


Clean/restore database
-------------------
Run the following command:
::
	>python manage.py flush


exec
::
	delete from django_content_type;
	delete from auth_permission;

And run the following command:
::
	>python manage.py loaddata testdata
	

**Mayor detalle**, revise la `Guía del desarrollador en PDF <https://github.com/submitconsulting/backenddj/blob/master/project/manuales/BackendDJ-devguide.pdf?raw=true>`_

**Para principiantes en Django**, revise `Manuales para principiantes <http://es.scribd.com/asullom>`_





Principales Características
======================


Gestión de Usuarios del sistema.  
-------------------
Permite la creación, edición, bloqueo y eliminación de Usuarios del sistema.
Los usuarios del sistema tienen sedes asociados y en cada sede tiene perfiles asociados, con ello se puede controlar los permisos de cada usuario dependiendo de los perfiles que posea cuando gestiona una sede, empresa o asociación.
Los usuarios usan el modelo ``django.contrib.auth.models.User``

Gestión de Perfiles de usuario. 
-------------------
Permite la creación, edición y eliminación de Perfiles de usuarios.
Los perfiles indican el tipo de función o rol de un usuario dentro del sistema. 
Por ejemplo: 
Usuario MASTER, GERENTE VENTAS, etc.
Los perfiles usan el modelo ``django.contrib.auth.models.Group``

Gestión de Recursos del sistema. 
-------------------
Permite la creación, edición y eliminación de Recursos del sistema.
Los recursos son cada uno de los módulos (páginas) que tiene la aplicación. Cada recurso está identificado por una url
Ejemplo de recursos:
app_name/controllername/action_name/ Acción específica del Controlador del Módulo 
app_name/controllername/ Todas las acciones del Controlador del Módulo
app_name/ Todos los Controladores y Acciones del Módulo

**Importante:** El controllername debe nombrarse de corrido sin subguión. Por ejemplo: ``mod_backend/loclitytype/add_form/``  Para mayor detalle ir a la sección de Convenciones de la `Guía del desarrollador en PDF <https://github.com/submitconsulting/backenddj/blob/master/project/manuales/BackendDJ-devguide.pdf?raw=true>`_. 
Si respeta la convenciones solo debe usar el decorador ``@permission_resource_required`` para asegurar la url.
Los recursos usan los modelos ``django.contrib.auth.models.Permission`` y ``django.contrib.contenttypes.models.ContentType``

Gestión de Permisos de usuarios. 
-------------------
Permite establecer a qué Recursos tiene acceso cada Perfil de usuario dentro del sistema. 
Los Permisos usan los modelos ``django.contrib.auth.models. Group`` y ``django.contrib.auth.models.Permission``. 
**NOTA:** Hasta aquí se personaliza la administración de los modelos de django. Esto mismo podría lograrlo con el módulo admin de django pero nada más simple que hacerlo con el módulo BackendDJ. Los siguientes modelos son diseñados por BackendDJ.

Gestión de Módulos del sistema. 
-------------------
Permite la creación, edición y eliminación de Módulos del sistema.
Un Módulo del sistema está asociando un conjunto de Perfiles de usuario, esto con el fin de limitar los permisos de los usuarios.

Gestión de Soluciones del sistema. 
-------------------
Permite la creación, edición y eliminación de Soliciones del sistema.
Una Solución indica el nivel del servicio a ofrecer a los clientes o usuarios del sistema. Ejemplo: Básico, Profesional, Empresarial, etc.

Gestión de Planes de Servicio (SaaS). 
-------------------
Permite la creación, edición y eliminación de Planes del sistema.
Permite establecer a qué Módulos tiene acceso cada Solución del sistema, esto es con el fin de personalizar los Módulos que conforma el  Servicio que se ofrece a los clientes.

Gestión de Menús. 
-------------------
Permite la creación, edición y eliminación de Menús del sistema.
Cada menú está asociado a un Recurso y a un Módulo del sistema, esto con el fin de generar menús dinámicos que solo carguen los ítems a los que un Perfil de usuario tenga acceso dentro de un Módulo. Mayor detalle en la sección de Convenciones de la `Guía del desarrollador en PDF <https://github.com/submitconsulting/backenddj/blob/master/project/manuales/BackendDJ-devguide.pdf?raw=true>`_

Gestión de Asociaciones. 
-------------------
Permite la creación, edición, bloqueo y eliminación de Asociaciones del sistema, así como el cambio de plan de servicio.
Una Asociación agrupa muchas Sedes.

Gestión de Empresas. 
-------------------
Permite la creación, edición, bloqueo y eliminación de Empresas del sistema, así como el cambio de plan de servicio.
Una empresa tiene muchas sedes y queda vinculada a una Asociación cuando por lo menos una de sus sedes está vinculada a dicha asociación.

Gestión de Sedes. 
-------------------
Permite la creación, edición, bloqueo y eliminación de Sedes de las empresas, así como el cambio de asociación.
Una sede o sucursal es la unidad fundamental para las operaciones del sistema.

Accesos. 
-------------------
Permite la visualización de las entradas y salidas de los usuarios del sistema.

Auditorías. 
-------------------
Permite la visualización de las acciones realizados por los usuarios.

Logs. 
-------------------
Permite la visualización de los logs del sistema.

Utilitarios. 
-------------------
El BackendDJ cuenta con componentes de seguridad, mensajería, carga de fotos, ente otros y se integran y se extienden con suma facilidad.
El frontend del BackendDJ es compatible con los navegadores más populares ya que combina HTML5, CSS3 y Javascript y se adecúa a diferentes dispositivos como celulares, tabletas, TVs y PCs. Los idiomas de los mensajes producidos con javascript también pueden extenderse para otro lenguaje en particular.



