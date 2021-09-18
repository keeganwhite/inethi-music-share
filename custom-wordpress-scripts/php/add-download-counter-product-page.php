<?php
/**
    To be added to the code snippet plugin. Removes the fields listed below from the checkout page
**/
if( is_product() ) {
	wp_enqueue_script('crm_js', get_stylesheet_directory_uri().'/assets/js/crm.js', array('jquery'),filemtime(get_stylesheet_directory() . '/assets/js/crm.js'),true);
}