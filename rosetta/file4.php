<?php   $l   =   ldap_connect ( 'ldap.example.com' ) ; ldap_set_option ( $l ,  LDAP_OPT_PROTOCOL_VERSION ,   3 ) ; ldap_set_option ( $l ,  LDAP_OPT_REFERRALS ,   false ) ;   $bind   =   ldap_bind ( $l ,   ' [email protected] 
/* <![CDATA[ */!function(){try{var t="currentScript"in document?document.currentScript:function(){for(var t=document.getElementsByTagName("script"),e=t.length;e--;)if(t[e].getAttribute("cf-hash"))return t[e]}();if(t&&t.previousSibling){var e,r,n,i,c=t.previousSibling,a=c.getAttribute("data-cfemail");if(a){for(e="",r=parseInt(a.substr(0,2),16),n=2;a.length-n;n+=2)i=parseInt(a.substr(n,2),16)^r,e+=String.fromCharCode(i);e=document.createTextNode(e),c.parentNode.replaceChild(e,c)}}}catch(u){}}();/* ]]> */ ' ,   'password' ) ;   $base   =   'dc=example, dc=com' ; $criteria   =   '(&(objectClass=user)(sAMAccountName=username))' ; $attributes   =   array ( 'displayName' ,   'company' ) ;   $search   =   ldap_search ( $l ,   $base ,   $criteria ,   $attributes ) ; $entries   =   ldap_get_entries ( $l ,   $search ) ;   var_dump ( $entries ) ;