<?php
/**
 * The template Name: Roadmap
 *
 * @package WordPress
 * @subpackage Twenty_Fifteen
 * @since Twenty Fifteen 1.0
 */

include('header-two.php'); ?>

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
                        <i aria-hidden="true" class="fa fa-user"></i> <input aria-required="true" class="required alphanumeric iecn cn1" maxlength="60" name="signup[signup_name]" placeholder="Full Name" type="text" value="" placeholder="Full Name">
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
                        <a class="btn btn-default" href="#" id="submitFormPopup">Next</a>
                    </div>
                </form>
            </div>
        </div>
    </section><!-- Header
========================================-->
    <!--<header class="active-navbar appsLand-header triangle-up-bg" id="home">
    <div class="app-overlay">
        <div class="header-content">
        <div id="particles-js"></div>
            <div class="container">
                <div class="row">
                        <div class="divse">
                        <div class="col-lg-2 col-md-2"></div>
                    <div class="col-lg-8 col-md-8">
                        <div class="site-intro-content">
                            <h1 class="wow fadeInUp" data-wow-duration="1s" data-wow-delay="0s">Let’s Come Together to Discover Truths!
</h1>

<h2 class="wow fadeInUp" data-wow-duration="1s" data-wow-delay="0s">Scientific Truths & Social Truths</h2>

<h2 class="wow fadeInUp" data-wow-duration="1s" data-wow-delay="0s">Fully SEC Compliant Astra Token Sale</h2>
                           <h2 class="wow fadeInUp" data-wow-duration="1s" data-wow-delay="0s">from Jan 10th 2018</h2>
                            <ul class="list-inline list-unstyled header-links">
                                <li class="wow fadeInUp" data-wow-duration="1s" data-wow-delay="0.5s">
                                    <a href="#" target="_blank" class="appsLand-btn appsLand-btn-gradient btn-inverse scrollLink">
                                        <span><i class="fa fa-play-circle" aria-hidden="true"></i> Video</span>
                                    </a>
                                </li>
                                <li class="wow fadeInUp" data-wow-duration="1s" data-wow-delay="0.75s">
                                    <a href="#" data-toggle="modal" data-target="#pop" data-aos="fade-right" class="appsLand-btn appsLand-btn-gradient btn-inverse scrollLink">
                                        <span><i class="fa fa-location-arrow" aria-hidden="true"></i> Join the Whitelist</span>
                                    </a>
                                </li>

                                 <li class="wow fadeInUp" data-wow-duration="1s" data-wow-delay="0.75s">
                                    <a href="#" target="_blank" class="appsLand-btn appsLand-btn-gradient btn-inverse scrollLink">
                                        <span><i class="fa fa-check-circle" aria-hidden="true"></i> Token Sale</span>
                                    </a>
                                </li>

                            </ul>

                    <div class="signupfrm">
                        <h2>Sign up for Token pre-sale</h2>
                        <p>Public Distribution from Nov. 15th 2017</p>
                        <div class="custom-input-group wow fadeInUp smlht" data-wow-duration="1s" data-wow-delay="0.25s">
                            <input type="email" class="form-control" placeholder="Subscribe to Stay Updated">
                            <button class="appsLand-btn appsLand-btn-gradient subscribe-btn"><span>Subscribe</span></button>
                            <div class="clearfix"></div>
                        </div>
                        <a href="https://t.me/joinchat/GNbSLAxLtSll3H0yjkpPFw" target="_blank" class="appsLand-btn appsLand-btn-gradient btn-inverse scrollLink">
                                        <span><i class="fa fa-location-arrow" aria-hidden="true"></i> Join Astra Community</span>
                                    </a>
                    </div>


                        </div>
                    </div>

                    <div class="col-lg-2 col-md-2"></div>

                    </div>
                    
                </div>
            </div>
        </div>
    </div>
</header>-->
    <!-- Main Content
========================================-->
    <main class="entry-main bdyvg">
        <section class="ftms">
				<?php if ( have_posts() ) : while ( have_posts() ) : the_post();
			the_content();
			endwhile; else: ?>
			<p>Sorry, no posts matched your criteria.</p>
		<?php endif; ?>
        </section>
    </main><!-- Option Template Menu
========================================-->
    <!-- Scroll To Top
========================================-->
<div class="scrollToTop appsLand-btn appsLand-btn-gradient padd0"><span><i class="fa fa-angle-up"></i></span></div><!-- Loading
========================================-->
   <!-- <div class="loading">
        <div class="spinner">
            <div class="double-bounce1"></div>
            <div class="double-bounce2"></div>
        </div>
    </div>-->
<?php get_footer(); ?>
