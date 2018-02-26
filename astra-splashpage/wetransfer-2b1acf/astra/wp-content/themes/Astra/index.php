<?php
/**
 * The template Name: Main Page New
 *
 * This is the most generic template file in a WordPress theme
 * and one of the two required files for a theme (the other being style.css).
 * It is used to display a page when nothing more specific matches a query.
 * e.g., it puts together the home page when no home.php file exists.
 *
 * Learn more: {@link https://codex.wordpress.org/Template_Hierarchy}
 *
 * @package WordPress
 * @subpackage Twenty_Fifteen
 * @since Twenty Fifteen 1.0
 */

get_header(); ?>

	    <section class="popup-form modal fade" id="pop" role="dialog">
        <button class="close" data-dismiss="modal" type="button">&times;</button>
        <div class="formcontainer">
            <div class="tophead">
                <h2>Join the Whitelist</h2>
                <h3>Whitelist Registration Form</h3>
            </div>
            <div class="inform" id="popupform">
                <form action="" class="clearfix" id="" method="post" name="">
                    <div class="field">
                        <i aria-hidden="true" class="fa fa-user"></i> <input aria-required="true" class="required alphanumeric iecn cn1" maxlength="60" name="signup[signup_name]" ="Full Name" type="text" value="" placeholder="Full Name">
                    </div>
                    <div class="field">
                        <i aria-hidden="true" class="fa fa-envelope"></i> <input aria-required="true" class="required email em1" maxlength="60" name="signup[signup_email]" placeholder="Email Address" type="text" value="">
                    </div>
                    <div class="field phone">
                        <i aria-hidden="true" class="fa fa-lock"></i> <input aria-required="true" class="required number pn1" maxlength="25" name="signup[signup_phone]" placeholder="Create Password" type="password" value="">
                    </div>
                    <div class="field phone">
                        <i aria-hidden="true" class="fa fa-lock"></i> <input aria-required="true" class="required number pn1" maxlength="25" name="signup[signup_phone]" placeholder="Confirm Password Again" type="password" value="">
                    </div>
                    <div class="clearfix fieldwrap text-center">
                        <a class="btn btn-default" href="step-2.html" id="submitFormPopup">Next</a>
                    </div>
                </form>
            </div>
        </div>
    </section>
    
    
    <section class="popup-form modal fade" id="login" role="dialog">
        <button class="close" data-dismiss="modal" type="button">&times;</button>
        <div class="formcontainer">
            <div class="tophead">
                <h2>LOGIN TO YOUR ACCOUNT</h2>
                <h5>Earn 5 Free STAR Tokens for Approved Registration</h5>
            </div>
            <div class="inform" id="popupform">
                <form action="" class="clearfix" id="" method="post" name="">
                    
                    <div class="field">
                        <i aria-hidden="true" class="fa fa-envelope"></i> <input aria-required="true" class="required email em1" maxlength="60" name="signup[signup_email]" placeholder="Email Address" type="text" value="">
                    </div>
                    <div class="field phone">
                        <i aria-hidden="true" class="fa fa-lock"></i> <input aria-required="true" class="required number pn1" maxlength="25" name="signup[signup_phone]" placeholder="Create Password" type="password" value="">
                    </div>
                    
                    <div class="field phone">
                       <input name="" type="checkbox" value=""><span>Remember my email address</span>
                    </div>
                    
                    <div class="clearfix fieldwrap text-center">
                        <a class="btn btn-default" href="#" id="submitFormPopup">Submit</a>
                    </div>
                </form>
            </div>
        </div>
    </section>
    
    <!-- Header
========================================-->
    <header class="active-navbar appsLand-header triangle-up-bg" id="home">
        <div class="app-overlay">
            <div class="header-content">
                <div id="particles-js"></div>
                <div class="container">
                    <div class="row">
                        <div class="divse">
                            <div class="col-lg-2 col-md-2"></div>
                            <div class="col-lg-12 col-md-12">
                                <div class="site-intro-content">
                                    <h1 class="wow fadeInUp  " data-wow-delay="0s" data-wow-duration="1s">Let’s Come Together to Discover Truths!</h1>
                                    <h2 class="wow fadeInUp size-34" data-wow-delay="0s" data-wow-duration="1s">Scientific Truths & Social Truths</h2>

                                    <div id="clockdiv" class="m-botom-20">
                                      <div>
                                        <span class="days">4</span>
                                        <div class="smalltext">Days</div>
                                      </div>
                                      <div>
                                        <span class="hours">23</span>
                                        <div class="smalltext">Hours</div>
                                      </div>
                                      <div>
                                        <span class="minutes">59</span>
                                        <div class="smalltext">Minutes</div>
                                      </div>
                                      <div>
                                        <span class="seconds">54</span>
                                        <div class="smalltext">Seconds</div>
                                      </div>
                                    </div>


                                    <h2 class="wow fadeInUp m-top-20" data-wow-delay="0s" data-wow-duration="1s">STAR Token Pre-sale from Jan 24th 2018</h2>
                                    <h2 class="wow fadeInUp m-top-20 m-botom-0 size-36" data-wow-delay="0s" data-wow-duration="1s" >5 Free STAR Tokens</h2>
                                    <ul class="list-inline list-unstyled header-links">
                                        <li class="wow fadeInUp" data-wow-delay="0.5s" data-wow-duration="1s">
                                            <a class="appsLand-btn appsLand-btn-gradient btn-inverse scrollLink" href="<?php echo bloginfo('template_url');?>/videos/Astra - The Social Supercomputer.mp4"  data-lity="" ><span><i aria-hidden="true" class="fa fa-play-circle"></i> Video</span></a>
                                        </li>
                                        <li class="wow fadeInUp" data-wow-delay="0.75s" data-wow-duration="1s">
                                            <a class="appsLand-btn appsLand-btn-gradient btn-inverse scrollLink" data-aos="fade-right" data-target="#pop" data-toggle="modal" href="#"><span><i aria-hidden="true" class="fa fa-location-arrow"></i> Join the Whitelist/Join</span></a>
                                        </li>
                                        <li class="wow fadeInUp" data-wow-delay="0.75s" data-wow-duration="1s">
                                            <a class="appsLand-btn appsLand-btn-gradient btn-inverse scrollLink" href="ttps://demo-octalogo.com/astraa-wp/token/"><span><i aria-hidden="true" class="fa fa-check-circle"></i> Token Sale</span></a>
                                        </li>
                                    </ul>
                                    <div class="clearfix"></div>
                                    <div class="signupfrm">
                                        <div class="custom-input-group wow fadeInUp smlht" data-wow-delay="0.25s" data-wow-duration="1s">
                                            <a href="https://astranetix.us16.list-manage.com/subscribe/post?u=cbdcc4d7bc5aed8237a9c0b53&id=f4e6f97e1a">
                                            <input class="form-control" placeholder="Subscribe to Stay Updated" type="email"> <button class="appsLand-btn appsLand-btn-gradient subscribe-btn"><span>Subscribe</span></button>
                                            <div class="clearfix"></div></a>
                                        </div><a class="appsLand-btn appsLand-btn-gradient btn-inverse scrollLink" href="https://t.me/joinchat/GNbSLAxLtSll3H0yjkpPFw" target="_blank"><span><i aria-hidden="true" class="fa fa-location-arrow"></i> Join Astra Community</span></a>
                                    </div>
                                </div>
                            </div>
                            <div class="col-lg-2 col-md-2"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header><!-- Main Content
========================================-->

    <main class="entry-main">
        <!-- Mini Feature Section
    ========================================-->
        <section class="mini-feature section-without-title bannerbtn">
            <div class="container">
					<?php if ( have_posts() ) : while ( have_posts() ) : the_post();
						the_content();
						endwhile; else: ?>
						<p>Sorry, no posts matched your criteria.</p>
					<?php endif; ?>
			</div> 

            </div>
        </section><!-- ScreenShots Section
    ========================================-->
        <section class="iconsec">
            <div class="container">
                <div class="row">
					<?php echo the_field('scientific_truth');?>
                </div>
                <div class="row">
                	<?php
						$active = 'active';
						$i=0;
						$args = array(
						'post_type' => 'scientifictruths',
						'posts_per_page' => -1,
						);
						$the_query = new WP_Query($args);
						if ($the_query->have_posts()) {
						while ($the_query->have_posts()) {
						$the_query->the_post();
						$feat_image_url = wp_get_attachment_url(get_post_thumbnail_id());
					?>
                    <div class="col-lg-4 col-md-4 col-sm-4">
                        <div class="feature-item wow fadeIn" data-wow-delay="<?php echo $i;?>" data-wow-duration="<?php echo $i;?>">
                            <div class="feature-icon">
                                <?php echo the_field('tagss');?>
                            </div>
                            <h4><?php echo the_title();?></h4>
                            <p><?php echo the_content();?></p>
                        </div>
                    </div>
                        <?php $active ='';
							$i++;
							}
							wp_reset_postdata();
							}
						?>
                    <div class="clearfix"></div>
                    <div class="col-lg-12 col-md-12 col-sm-12">
                        <h2><?php echo the_field('earn');?></h2>
                    </div>
                </div>
            </div>
        </section>
        <section class="iconsec bottomsse">
            <div class="container">
                <div class="row">
                <?php echo the_field('social_trutch');?>
                </div>
				<div class="row">
				<?php
						$active = 'active';
						$i=0;
						$args = array(
						'post_type' => 'social_truths',
						'posts_per_page' => -1,
						);
						$the_query = new WP_Query($args);
						if ($the_query->have_posts()) {
						while ($the_query->have_posts()) {
						$the_query->the_post();
						$feat_image_url = wp_get_attachment_url(get_post_thumbnail_id());
					?>
                    <div class="col-lg-4 col-md-4 col-sm-4">
                        <div class="feature-item wow fadeIn" data-wow-delay="<?php echo $i;?>" data-wow-duration="<?php echo $i;?>">
                            <div class="feature-icon">
                                <?php echo the_field('new_taggss');?>
                            </div>
                             <h4><?php echo the_title();?></h4>
                            <p><?php echo the_content();?></p>
                        </div>
                    </div>
						<?php $active ='';
							$i++;
							}
							wp_reset_postdata();
							}
						?>
                    <div class="col-lg-12 col-md-12 col-sm-12">
                      <h2><?php echo the_field('earn');?></h2>
                    </div>
                </div>
            </div>
        </section>
        <section class="iconsec teams" id="team">
            <div class="container">
                <div class="row" id="team">
                    <h1>The Team</h1>
                </div>
                <div class="row">
					<?php
						$active = 'active';
						$i=0;
						$args = array(
						'post_type' => 'the_team',
						'posts_per_page' => -1,
						);
						$the_query = new WP_Query($args);
						if ($the_query->have_posts()) {
						while ($the_query->have_posts()) {
						$the_query->the_post();
						$feat_image_url = wp_get_attachment_url(get_post_thumbnail_id());
					?>
                    <div class="col-lg-4 col-md-4 col-sm-4">
                        <div class="view view-fifth">
                            <img alt="" src="<?php echo $feat_image_url;?>">
                            <div class="mask">
                                <h2><?php echo the_title();?></h2>
                                <p><?php echo the_content();?></p>
                               <!--  <div class="member-social-link text-center">
                                    <a href="#"><i aria-hidden="true" class="fa fa-facebook"></i></a> <a href="#"><i aria-hidden="true" class="fa fa-linkedin"></i></a>
                                </div> -->
                            </div>
                        </div>
                    </div>
						<?php $active ='';
							$i++;
							}
							wp_reset_postdata();
							}
						?>

                </div>
            </div>
        </section>
        <section class="iconsec teams" id="team">
            <div class="container">
                <div class="row">
                    <h1>The Advisors</h1>
                </div>
                <div class="row">
                    <div class="col-lg-4 col-md-4 col-sm-4">
                        <div class="image">
                            <img src="<?php echo the_field('doctor_image');?>">
                        </div>
                    </div>
                    <div class="col-lg-8 col-md-8 col-sm-8">
                        <div class="image">
                        	<?php echo the_field('content1');?>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-8 col-md-8 col-sm-8">
						<div class="image">
                        	<?php echo the_field('content2');?>
                        </div>                    </div>
                    <div class="col-lg-4 col-md-4 col-sm-4">
						<div class="image">
							<img src="<?php echo the_field('doctor_image2');?>">
						</div>
                    </div>
                </div>
            </div>
        </section>
        <!-- Features Section
    ========================================-->
        <section class="procesroad">
            <div id="particles-js1"></div>
            <div class="container">
                <div class="row">
                    <div class="sect2">
                        <div class="col-lg-12">
                            <h1><?php echo the_field('astra_heading');?></h1>
                        </div>
                        <div class="col-lg-4 col-md-4 col-sm-6 text-center">
                            <div class="msw"><img alt="" src="<?php echo bloginfo('template_url');?>/images/Iphone-x.png" width="100%"></div>
                        </div>
                        <div class="col-lg-8 col-md-8 col-sm-6">
							<?php echo the_field('astra_app');?>
						</div>
                        <div class="clearfix"></div>
                        <div class="col-lg-6 col-md-6 col-sm-6">
							<?php echo the_field('astra_economics');?>
						</div>
                        <div class="col-lg-6 col-md-6 col-sm-6 text-center">
                            <div class="msw1"><img alt="" src="<?php echo bloginfo('template_url');?>/images/mac.png" width="100%"></div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="gfts">
                        <div class="row">
                            <div class="col-lg-12 col-md-6 text-center">
                                <a class="appsLand-btn appsLand-btn-gradient btn-inverse scrollLink" href="https://demo-octalogo.com/astraa-wp/roadmap/"><span>RoadMap</span></a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section><!--<section class="subscribe subem">
        <div class="container">
            <div class="section-title title__style-2 wow fadeInUp" data-wow-duration="1s" data-wow-delay="0s" style="visibility: visible; animation-duration: 1s; animation-delay: 0s; animation-name: fadeInUp;">
                <h2>
                    Subscribe to stay up to date on the Astra Project

                    
                </h2>
                <p>
                    Keep In Touch And Register In Our News Letter
                </p>
            </div>
            <form>
                <div class="row">
                    <div class="col-md-6 col-md-offset-3 col-sm-8 col-sm-offset-2">
                        <div class="custom-input-group wow fadeInUp" data-wow-duration="1s" data-wow-delay="0.25s" style="visibility: visible; animation-duration: 1s; animation-delay: 0.25s; animation-name: fadeInUp;">
                            <input type="email" class="form-control" placeholder="Email">
                            <button class="appsLand-btn appsLand-btn-gradient subscribe-btn"><span>Subscribe</span></button>
                            <div class="clearfix"></div>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </section>-->
        <section class="video section-bg-img bg-bc" id="media">
            <div class="app-overlay">
                <div class="container">
                    <div class="section-title title__style-2 wow fadeInUp white-color" data-wow-delay="0s" data-wow-duration="1s" style="visibility: visible; animation-duration: 1s; animation-delay: 0s; animation-name: fadeInUp;">
                        <h2>Media</h2>
                        <p></p>
                    </div>
                    <div class="play-video-icon wow fadeInUp" data-wow-delay="0.25s" data-wow-duration="1s">
                        <a data-lity="" href="<?php echo bloginfo('template_url');?>/videos/Astra - The Social Supercomputer.mp4"><img alt="" src="<?php echo bloginfo('template_url');?>/images/icon-14.png"></a>
                    </div>
                </div>
            </div>
        </section><!-- Download Section
    ========================================-->
        <section class="blog" id="blog">
            <div class="container">
                <div class="row">
					<?php
						$active = 'active';
						$i=0;
						$args = array(
						'post_type' => 'home_poster',
						'posts_per_page' => -1,
						);
						$the_query = new WP_Query($args);
						if ($the_query->have_posts()) {
						while ($the_query->have_posts()) {
						$the_query->the_post();
						$feat_image_url = wp_get_attachment_url(get_post_thumbnail_id());
					?>
                    <div class="col-lg-4 col-md-4 col-sm-4">
                        <div class="single-member">
                            <img alt="" src="<?php echo $feat_image_url;?>">
                            <div class="member-title text-center">
                                <h3><a href="<?php echo the_field('link');?>" target="_blank"><?php echo the_title();?></a></h3>
                            </div>
                        </div>
                    </div>
						<?php $active ='';
							$i++;
							}
							wp_reset_postdata();
							}
						?>
                </div>
            </div>
        </section><!-- Pricing Section
    ========================================-->
        <!-- Testimonials Section
    ========================================-->
        <!-- Team Section
    ========================================-->
        <!-- Video Section
    ========================================-->
        <!-- FAQ Section
    ========================================-->
        <!-- Statistics Section
    ========================================-->
        <!-- Blog Section
    ========================================-->
        <!-- Contact Section
    ========================================-->
        <section class="contact section-bg-img" id="contact">
            <div class="app-overlay">
                <div class="container">
                    <div class="section-title title__style-2 wow fadeInUp white-color" data-wow-delay="0s" data-wow-duration="1s">
                        <h2>Connect with us</h2>
                        <p></p>
                    </div>
                    <div class="row">
                        <div class="col-lg-10 col-lg-offset-1">
                            <div class="contact-form wow fadeInUp" data-wow-delay="0.25s" data-wow-duration="1s">
                                <div class="row">
                                    <div class="col-md-4 col-lg-push-8 col-md-push-8">
                                        <div class="contact-info">
                                            <div class="info-box">
                                                <div class="icon-box">
                                                    <ul>
                                                        <li>
                                                            <a href="<?php echo $telegram = ot_get_option('telegram');?>" target="_blank"><i aria-hidden="true" class="fa fa-telegram ft"></i></a>
                                                        </li>
                                                        <li>
                                                            <a href="<?php echo $facebook = ot_get_option('facebook');?>" target="_blank"><i aria-hidden="true" class="fa fa-facebook ft pad5"></i></a>
                                                        </li>
                                                        <li>
                                                            <a href="<?php echo $linkedin = ot_get_option('linkedin');?>" target="_blank"><i aria-hidden="true" class="fa fa-linkedin ft"></i></a>
                                                        </li>
                                                        <li>
                                                            <a href="<?php echo $twitter = ot_get_option('twitter');?>" target="_blank"><i aria-hidden="true" class="fa fa-twitter ft"></i></a>
                                                        </li>
                                                    </ul>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-8 col-lg-pull-4 col-md-pull-4">
                                   		<?php echo do_shortcode('[contact-form-7 id="47" title="Footer Contact Form"]');?>     
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
		<!-- Client Logo Section
    ========================================-->
        <!-- Subscribe Section
    ========================================-->
    </main><!-- Option Template Menu
========================================-->
    <!-- Scroll To Top
========================================-->
    <div class="scrollToTop appsLand-btn appsLand-btn-gradient padd0"><span><i class="fa fa-angle-up"></i></span></div><!-- Loading
========================================-->
    <!--<div class="loading">
        <div class="spinner">
            <div class="double-bounce1"></div>
            <div class="double-bounce2"></div>
        </div>
    </div>-->
	

<?php get_footer(); ?>
