<?php
/**
 * The template for displaying the header
 *
 * Displays all of the head element and everything up until the "site-content" div.
 *
 * @package WordPress
 * @subpackage Twenty_Fifteen
 * @since Twenty Fifteen 1.0
 */
?><!DOCTYPE html>
<html <?php language_attributes(); ?> class="no-js">
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width">
	<link rel="profile" href="http://gmpg.org/xfn/11">
	<link rel="pingback" href="<?php bloginfo( 'pingback_url' ); ?>">
	<!--[if lt IE 9]>
	<script src="<?php echo esc_url( get_template_directory_uri() ); ?>/js/html5.js"></script>
	<![endif]-->
	<meta charset="utf-8">
    <meta content="IE=edge" http-equiv="X-UA-Compatible">
    <meta content="width=device-width, initial-scale=1" name="viewport">
    <title>The Social Supercomputer </title>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700,800" rel="stylesheet">
    <link href="app.ico" rel="icon">
    <link href="<?php echo bloginfo('template_url');?>/css/font-awesome.min.css" rel="stylesheet">
    <link href="<?php echo bloginfo('template_url');?>/css/bootstrap.min.css" rel="stylesheet">
    <link href="<?php echo bloginfo('template_url');?>/css/swiper.min.css" rel="stylesheet">
    <link href="<?php echo bloginfo('template_url');?>/css/animate.css" rel="stylesheet">
    <link href="<?php echo bloginfo('template_url');?>/css/lity.min.css" rel="stylesheet">
    <link href="<?php echo bloginfo('template_url');?>/css/style.css" rel="stylesheet">
    <link href="<?php echo bloginfo('template_url');?>/css/custom.css" rel="stylesheet">
    <link href="<?php echo bloginfo('template_url');?>/css/gradient_colors/theme_color_1.css" id="color-option" rel="stylesheet">
    <!--[if lt IE 9]>
    <script src="js/html5shiv.min.js"></script>
    <script src="js/respond.min.js"></script>
    <![endif]-->

    <script src="<?php echo bloginfo('template_url');?>/assets/js/libs.min.js">
    </script>
    <script src="<?php echo bloginfo('template_url');?>/js/particle-theme-1.min.js">
    </script>
	<?php wp_head(); ?>
</head>

<body class="scrollspy-example" data-offset="5" data-spy="scroll" data-target="#bs-example-navbar-collapse-1">
    <nav class="navbar navbar-default navbar-fixed-top appsLand-navbar">
        <div class="container-fluid">
            <!-- Brand and toggle get grouped for better mobile display -->
            <div class="navbar-header">
                <span class="menu-toggle"><i class="chart"></i> <i class="chart"></i> <i class="chart"></i></span> <a class="navbar-brand" href="<?php echo bloginfo('home');?>/"><img alt="" src="<?php echo $logo = ot_get_option('logo');?>">
                <h2>ASTRA<br>
                <span>The Social Supercomputer</span></h2></a>
            </div><!-- Collect the nav links, forms, and other content for toggling -->
            <div class="app-links" id="bs-example-navbar-collapse-1">
                <ul class="nav navbar-nav navbar-right appsLand-links">
                    <li class="visible-xs-block text-center mobile-size-logo">
                        <a href="<?php echo bloginfo('home');?>/"><img alt="" src="<?php echo $logo = ot_get_option('logo');?>">
                        <h2>ASTRA<br>
                        <span>The Social Supercomputer</span></h2></a>
                    </li>
                    <li>
                        <a href="https://demo-octalogo.com/astraa-wp/">Home</a>
                    </li>
                    <li>
                        <a href="https://demo-octalogo.com/astraa-wp/token/">Token</a>
                    </li>
                    <li>
                        <a href="<?php echo bloginfo('template_url');?>/assests/Astra-Introduction.pdf">Presentation</a>
                        
                    </li>
                    <li>
                        <a href="<?php echo bloginfo('template_url');?>/assests/Astra-Whitepaper.pdf"  target="_blank">Whitepaper</a>
                    </li>
                   <!-- <li> <a href="#download">One-Pager</a> </li> -->
                    <li>
                        <a href="<?php echo bloginfo('template_url');?>/assests/Astra-FAQ.pdf" target="_blank">FAQ</a>
                    </li>
                    <li>
                        <a href="#team">Team</a>
                    </li>
                    <li>
                        <a href="#media">Media</a>
                    </li>
                    <li>
                        <a href="https://demo-octalogo.com/astraa-wp/roadmap/">Roadmap</a>
                    </li>
                    <li class="roundedcrck">
                        <a href="https://t.me/Astra_Network"><i aria-hidden="true" class="fa fa-location-arrow"></i> Join Telegram</a>
                    </li>
                </ul>
            </div><!-- /.navbar-collapse -->
        </div><!-- /.container-fluid -->
    </nav>
