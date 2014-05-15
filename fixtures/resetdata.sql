/*
delete from django_content_type;
delete from auth_permission;
*/
delete from auth_permission where codename like 'add_%' or codename like 'change_%' or codename like 'delete_%';


delete from space_solution;
insert  into space_solution(id,name,description,is_active,registered_at,modified_in) values 
(1,'Shomware Basic','Limitado para ventas',1,'2013-10-31 04:52:44','2013-11-13 05:03:19');
insert  into space_solution(id,name,description,is_active,registered_at,modified_in) values 
(2,'Shomware Ultimate','Backend + Ventas',1,'2013-10-31 04:53:33','2013-10-31 04:53:33');

delete from sad_module;
insert  into `sad_module`(`id`,`module`,`name`,`is_active`,`icon`,`description`,`registered_at`,`modified_in`) values
(1,'BACKEND','Backend',1,NULL,'','2013-10-31 04:51:34','2013-11-10 16:57:52');
insert  into `sad_module`(`id`,`module`,`name`,`is_active`,`icon`,`description`,`registered_at`,`modified_in`) values
(2,'VENTAS','Ventas',1,NULL,'','2013-10-31 04:52:14','2013-11-13 05:03:15');
insert  into `sad_module`(`id`,`module`,`name`,`is_active`,`icon`,`description`,`registered_at`,`modified_in`) values
(3,'PRO','Profesional',1,NULL,'','2013-11-20 22:06:44','2013-11-20 22:06:44');

delete from sad_module_solutions;
insert  into `sad_module_solutions`(`id`,`module_id`,`solution_id`) values 
(1,1,2);
insert  into `sad_module_solutions`(`id`,`module_id`,`solution_id`) values
(2,3,2);
insert  into `sad_module_solutions`(`id`,`module_id`,`solution_id`) values
(3,3,1);
insert  into `sad_module_solutions`(`id`,`module_id`,`solution_id`) values
(4,2,2);
insert  into `sad_module_solutions`(`id`,`module_id`,`solution_id`) values
(5,2,1);


delete from auth_group;
insert  into `auth_group`(`id`,`name`) values 
(1,'MASTER');
insert  into `auth_group`(`id`,`name`) values 
(2,'CATASTRO');
insert  into `auth_group`(`id`,`name`) values 
(3,'GERENTE VENTAS');
insert  into `auth_group`(`id`,`name`) values 
(4,'VENDEDOR');
insert  into `auth_group`(`id`,`name`) values 
(5,'RRHH');


delete from sad_module_groups;
insert  into `sad_module_groups`(`id`,`module_id`,`group_id`) values 
(1,1,1);
insert  into `sad_module_groups`(`id`,`module_id`,`group_id`) values 
(2,1,2);
insert  into `sad_module_groups`(`id`,`module_id`,`group_id`) values 
(3,3,5);
insert  into `sad_module_groups`(`id`,`module_id`,`group_id`) values 
(4,2,4);
insert  into `sad_module_groups`(`id`,`module_id`,`group_id`) values 
(5,2,3);


delete from sad_module_initial_groups;
insert  into `sad_module_initial_groups`(`id`,`module_id`,`group_id`) values 
(1,1,1);
insert  into `sad_module_initial_groups`(`id`,`module_id`,`group_id`) values 
(2,3,5);
insert  into `sad_module_initial_groups`(`id`,`module_id`,`group_id`) values 
(3,2,3);


delete from django_content_type;
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(1,'log entry','admin','logentry');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values 
(2,'permission','auth','permission');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(3,'group','auth','group');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(4,'user','auth','user');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(5,'content type','contenttypes','contenttype');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(6,'session','sessions','session');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(7,'site','sites','site');

insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(8,'locality type','params','localitytype');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(9,'locality','params','locality');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(10,'person','params','person');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(11,'ticket','params','ticket');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(12,'solution','space','solution');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(13,'association','space','association');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(14,'enterprise','space','enterprise');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(15,'headquar','space','headquar');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(16,'profile','sad','profile');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(17,'user state','sad','userstate');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(18,'access','sad','access');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(19,'backup','sad','backup');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(20,'module','sad','module');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(21,'menu','sad','menu');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(22,'user profile enterprise','sad','userprofileenterprise');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(23,'user profile headquar','sad','userprofileheadquar');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(24,'user profile association','sad','userprofileassociation');

insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(25,'resource','sad','resource');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(26,'group','sad','group');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(27,'user','sad','user');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(28,'audit','sad','audit');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(29,'log','sad','log');

insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(30,'maintenance','sad','maintenance');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(31,'system','sad','system');

insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(32,'dashboard','mod_backend','dashboard');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(33,'','home','');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(34,'profile','accounts','profile');

insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(50,'last','last','last');



/*Mod ventas*/
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(51,'categoria','params','categoria');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(52,'producto','maestros','producto');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(53,'dashboard','mod_ventas','dashboard');

/*Mod profesional*/
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(61,'employee','rrhh','employee');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(62,'dashboard','mod_pro','dashboard');





delete from auth_permission;
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values 
(1,'Puede hacer TODAS las oper. de tipos d localidades',8,'localitytype');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(2,'Puede hacer TODAS las operaciones de localidades',9,'locality');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(3,'Puede ver el index de localidades',9,'locality_index');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(4,'Puede agregar localidad',9,'locality_add');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(5,'Puede actualizar localidades',9,'locality_edit');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(6,'Puede eliminar localidades',9,'locality_delete');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(7,'Puede reportar localidades',9,'locality_report');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(8,'Puede inactivar y reactivar localidades',9,'locality_state');

insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(9,'Puede hacer TODAS las operaciones de personas',10,'person');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(10,'Puede hacer TODAS las operaciones de ticket',11,'ticket');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(11,'Puede hacer TODAS las operaciones de soluciones',12,'solution');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(12,'Puede hacer TODAS las operaciones de asociaciones',13,'association');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(13,'Puede hacer TODAS las operaciones de empresas',14,'enterprise');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(14,'Puede hacer TODAS las operaciones de sedes',15,'headquar');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(15,'Puede hacer TODAS las operaciones de access',18,'access');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(16,'Puede hacer TODAS las operaciones de backup',19,'backup');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(17,'Puede hacer TODAS las operaciones de modulos',20,'module');

insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(18,'Puede hacer TODAS las operaciones de menus',21,'menu');

insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(19,'Submodulo del sistema para la gestion de los recur',25,'resource');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(20,'Submodulo del sistema para los perfiles de usuario',26,'group');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(21,'Submodulo para la administracion de los usuarios d',27,'user');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(22,'Submodulo para auditorias',28,'audit');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(23,'Submodulo para logs',29,'log');

insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(24,'Submodulo para maintenance de tablas del SGBD',30,'maintenance');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(25,'Submodulo para archivos de confi del system',31,'system');

insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(26,'Submodulo Dashboard del mod_backend',32,'dashboard');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(27,'Submodulo Todo',33,'');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(28,'Submodulo Editar user profile',34,'profile_edit');

insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(50,'Submodulo last',50,'last');

/*Mod ventas*/
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(51,'Puede hacer TODAS las operaciones de categorias',51,'categoria');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(52,'Puede hacer TODAS las operaciones de productos',52,'producto');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(53,'Puede ver el index de productos',52,'producto_index');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(54,'Puede agregar producto',52,'producto_add');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(55,'Puede actualizar productos',52,'producto_edit');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(56,'Puede eliminar productos',52,'producto_delete');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(57,'Puede reportar productos',52,'producto_report');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(58,'Puede inactivar y reactivar productos',52,'producto_state');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(59,'Puede actualizar precio venta de productos',52,'producto_edit_precio');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(70,'Submodulo Dashboard del mod_ventas',53,'dashboard');

/*Mod profesional*/
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(71,'Puede hacer TODAS las operaciones de empleados',61,'employee');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(80,'Submodulo Dashboard del mod_pro',62,'dashboard');






delete from auth_group_permissions;
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(1,2,26);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(2,1,26);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(3,2,28);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(4,1,28);

insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(5,1,2);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(6,2,3);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(7,2,4);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(8,2,5);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(9,2,7);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(10,2,1);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(11,1,1);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(12,1,9);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(13,1,10);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(14,1,15);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(15,1,22);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(16,1,16);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(17,1,20);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(18,1,23);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(19,1,24);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(20,1,18);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(21,1,17);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(22,1,19);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(23,1,25);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(24,1,21);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(25,1,12);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(26,1,13);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(27,1,14);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(28,1,11);
/*insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(29,1,3);*/

/*Mod ventas*/
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(31,4,28);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(32,3,28);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(33,3,52);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(34,4,53);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(35,4,54);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(36,4,58);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(37,4,70);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(38,3,70);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(39,4,51);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(40,3,51);
/*insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(41,3,53);*/

/*Mod profesional*/
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(51,5,28);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(52,5,80);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(53,5,71);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(60,5,9);


delete from sad_menu;
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(11,'BACKEND','Dashboard','#',100,'icon-home',1,NULL,'2013-10-31 05:24:35','2013-11-10 17:14:01',NULL,NULL);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(12,'BACKEND','Dashboard','mod_backend/dashboard/',101,'icon-home',1,NULL,'2013-10-31 05:29:35','2013-10-31 05:29:35',26,11);


insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(61,'BACKEND','Account','#',600,'icon-user',1,NULL,'2013-10-31 05:12:15','2013-11-10 17:14:05',NULL,NULL);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(62,'BACKEND','Association','space/association/edit_current/',601,'icon-briefcase',1,NULL,'2013-10-31 05:17:03','2013-10-31 05:17:03',12,61);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(63,'BACKEND','Enterprises','space/enterprise/index/',602,'icon-sitemap',1,NULL,'2013-10-31 05:18:06','2013-10-31 05:18:06',13,61);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(64,'BACKEND','Enterprise','space/enterprise/edit_current/',603,'icon-briefcase',1,NULL,'2013-10-31 05:18:46','2013-10-31 05:18:46',13,61);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(65,'BACKEND','Headquarters','space/headquar/index/',604,'icon-sitemap',1,NULL,'2013-10-31 05:19:25','2013-10-31 05:19:25',14,61);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(66,'BACKEND','Users','sad/user/index/',605,'icon-user',1,NULL,'2013-10-31 05:21:51','2013-10-31 05:21:51',21,61);


insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(71,'BACKEND','System','#',700,'icon-cogs',1,NULL,'2013-10-31 04:59:29','2013-10-31 05:02:12',NULL,NULL);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(72,'BACKEND','Menus','sad/menu/index/',707,'icon-list',1,NULL,'2013-10-31 05:10:49','2013-10-31 05:10:49',18,71);

insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(73,'BACKEND','Resource','sad/resource/index/',701,'icon-lock',1,NULL,'2013-10-31 05:02:06','2013-10-31 05:02:06',19,71);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(74,'BACKEND','Profiles','sad/group/index/',702,'icon-group',1,NULL,'2013-10-31 05:03:15','2013-10-31 05:03:15',20,71);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(75,'BACKEND','Permissions','sad/group/permissions_edit/',703,'icon-magic',1,NULL,'2013-10-31 05:04:35','2013-10-31 05:04:35',20,71);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(76,'BACKEND','Modules','sad/module/index/',704,'icon-hdd',1,NULL,'2013-10-31 05:08:29','2013-10-31 05:08:29',17,71);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(77,'BACKEND','Solutions','space/solution/index/',705,'icon-wrench',1,NULL,'2013-10-31 05:09:23','2013-10-31 05:09:23',11,71);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(78,'BACKEND','Plans','sad/module/plans_edit/',706,'icon-magic',1,NULL,'2013-10-31 05:10:15','2013-10-31 05:10:15',17,71);



insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(81,'BACKEND','Logs','#',800,'icon-eye-open',1,NULL,'2013-11-21 00:04:06','2013-11-21 00:04:06',NULL,NULL);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(82,'BACKEND','Access','sad/access/index/',801,'icon-exchange',1,NULL,'2013-11-21 00:04:06','2013-11-21 00:04:06',15,81);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(83,'BACKEND','Audits','sad/audit/index',802,'icon-eye-open',1,NULL,'2013-11-21 00:04:06','2013-11-21 00:04:06',22,81);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(84,'BACKEND','Logs','sad/log/index/',803,'icon-filter',1,NULL,'2013-11-21 00:04:06','2013-11-21 00:04:06',23,81);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(85,'BACKEND','Backups','sad/backup/index/',804,'icon-hdd',1,NULL,'2013-11-21 00:04:06','2013-11-21 00:04:06',16,81);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(86,'BACKEND','Tables','sad/maintenance/index/',808,'icon-bolt',1,NULL,'2013-11-21 00:04:06','2013-11-21 00:04:06',24,81);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(90,'BACKEND','System','sad/system/index/',809,'icon-wrench',1,NULL,'2013-11-21 00:04:06','2013-11-21 00:04:06',25,81);


insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(91,'BACKEND','Params','#',900,'icon-th-list',1,NULL,'2013-11-21 00:04:06','2013-11-21 00:04:06',NULL,NULL);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(92,'BACKEND','Localities','params/locality/index/',901,'',1,NULL,'2013-10-31 05:49:17','2013-10-31 05:49:17',2,91);


insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(100,'BACKEND','Next','#',999,'icon-calendar',1,NULL,'2013-11-21 00:04:06','2013-11-21 00:04:06',NULL,NULL);


/*Mod ventas*/
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(101,'VENTAS','Dashboard','#',100,'icon-home',1,NULL,'2013-10-31 05:38:05','2013-10-31 05:38:05',NULL,NULL);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(102,'VENTAS','Dashboard','mod_ventas/dashboard/',101,'icon-home',1,NULL,'2013-10-31 05:38:44','2013-11-25 22:00:49',70,101);

insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(130,'VENTAS','Maestros','#',300,'icon-calendar',1,NULL,'2013-11-01 15:41:28','2013-11-01 15:41:28',NULL,NULL);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(131,'VENTAS','Productos','maestros/producto/index/',301,'icon-print',1,NULL,'2013-11-01 15:42:22','2013-11-19 16:43:11',52,130);

/*Mod profesional*/
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(201,'PRO','Dashboard','#',100,'icon-home',1,NULL,'2013-11-20 22:25:44','2013-11-20 22:40:39',NULL,NULL);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(202,'PRO','Dashboard','mod_pro/dashboard/',101,'icon-home',1,NULL,'2013-11-20 22:40:31','2013-11-20 22:46:35',80,201);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(203,'PRO','Datos Empleado','rrhh/employee/edit/',102,'icon-briefcase',1,NULL,'2013-11-20 22:53:25','2013-11-25 10:42:25',71,201);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(210,'PRO','Listado de Empleados','rrhh/employee/index/',103,'icon-calendar',1,NULL,'2013-11-21 00:04:06','2013-11-21 00:04:06',71,201);
