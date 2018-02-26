<?php
/**
 * The template Name: Token
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
                <form action="http://demo-octalogo.com/astraa-wp/step2/" class="clearfix" id="myform" method="post" name="">
                    <div class="field">
                        <i aria-hidden="true" class="fa fa-user"></i> <input aria-required="true" class="required alphanumeric iecn cn1" maxlength="60" name="full_name" ="Full Name" type="text" value="" placeholder="Full Name">
                    </div>
                    <div class="field">
                        <i aria-hidden="true" class="fa fa-envelope"></i> <input aria-required="true" class="required email em1" maxlength="60" name="email" placeholder="Email Address" type="text" value="">
                    </div>
                    <div class="field phone">
                        <i aria-hidden="true" class="fa fa-lock"></i> <input aria-required="true" class="number pn1" maxlength="25" name="password" placeholder="Create Password" type="password" value="" id="Password">
                        <p id="error_Passwordrequire"></p>
                    </div>
                    <div class="field phone">
                        <i aria-hidden="true" class="fa fa-lock"></i> <input aria-required="true" class="number pn1" maxlength="25" name="PasswordConfirm" placeholder="Confirm Password Again" type="password" value="" id="PasswordConfirm">
                        <p id="error_confirmPassword"></p>
                    </div>
                    <div class="clearfix fieldwrap text-center">
                       <!--  <a class="btn btn-default" href="" id="submitFormPopup">Next</a> -->
                       <input type="Submit" name="form_submit" value="Submit" class="sign_up">
                    </div>
                </form>
            </div>
        </div>
    </section>
	<script type="text/javascript">
    jQuery(document).ready(function(){
   jQuery('.sign_up').click(function(event){
   var errorFlag = 0;
   event.preventDefault()
  
           if ($("#Password").length > 0) { 
                    //Fields are hidden if logged in
                    if ($("#Password").val() != $("#PasswordConfirm").val()) {
                        $("small[data-validate*='PasswordMatch']").addClass("active");
                        $("#Password").addClass("required");
                        $("#PasswordConfirm").addClass("required");
                        validForm = false;
                    } else if ($("#Password").val().length <= 4) {
                        $("small[data-validate*='PasswordLength']").addClass("active");
                        $("#Password").addClass("required");
                        $("#PasswordConfirm").addClass("required");
                        validForm = false;
                    }
                }

            var password = $("#Password").val();
            var confirmPassword = $("#PasswordConfirm").val();
            
            if (password == '') {
                $('#error_Passwordrequire').text("Please Enter password.");
                var errorFlag = 1;
                return false;
            }else{
              $('#error_Passwordrequire').text("");  
            }   

            if (password != confirmPassword) {
                $('#error_confirmPassword').text("Password do not match.");
                var errorFlag = 1;
                return false;
            }else{
                $('#error_confirmPassword').text("Password matched.");
                
            } 
         if(errorFlag == 0 ){
           $( "#myform" ).submit();
          }     
           // return true;
           

        })

    })

</script>	


<!-- Header
========================================-->
<header class="active-navbar appsLand-header triangle-up-bg" id="home">
    <div class="app-overlay">
        <div class="header-content">
        <div id="particles-js"><canvas class="particles-js-canvas-el" width="1423" height="667" style="width: 100%; height: 100%;"></canvas></div>
            <div class="container">
                <div class="row">
                        <div class="divse">
                        <div class="col-lg-2 col-md-2"></div>
<div class="col-lg-12 col-md-12">
                                <div class="site-intro-content">
                                    <h1 class="wow fadeInUp  " data-wow-delay="0s" data-wow-duration="1s">STAR Token Pre-sale from Jan 24th 2018</h1>                                   

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


                                   
                                    <h2 class="wow fadeInUp m-top-20 m-botom-0 size-36" data-wow-delay="0s" data-wow-duration="1s" >5 Free STAR Tokens</h2>
                                    <ul class="list-inline list-unstyled header-links">
                                        <li class="wow fadeInUp" data-wow-delay="0.5s" data-wow-duration="1s">
                                            <a class="appsLand-btn appsLand-btn-gradient btn-inverse scrollLink" href="http://goastra.network/assets/Astra-Whitepaper.pdf"><span>Whitepaper&nbsp;</span></a>
                                        </li>
                                        <li class="wow fadeInUp" data-wow-delay="0.75s" data-wow-duration="1s">
                                            <a class="appsLand-btn appsLand-btn-gradient btn-inverse scrollLink" data-aos="fade-right" href="login-form.html"><span><i aria-hidden="true" class="fa fa-location-arrow"></i> Join the Whitelist/Join</span></a>
                                        </li>
                                        <li class="wow fadeInUp" data-wow-delay="0.75s" data-wow-duration="1s">
                                            <a class="appsLand-btn appsLand-btn-gradient btn-inverse scrollLink" href="assests/Astra - Terms of Token Sale - 180108.pdf"><span><i aria-hidden="true" class="fa fa-check-circle"></i>Terms of Token Sale</span></a>
                                        </li>
                                    </ul>
                                    <div class="clearfix"></div>
                                    <div class="signupfrm2">
                                        <div class="custom-input-group wow fadeInUp smlht" data-wow-delay="0.25s" data-wow-duration="1s">
                                            <a href="https://astranetix.us16.list-manage.com/subscribe/post?u=cbdcc4d7bc5aed8237a9c0b53&id=f4e6f97e1a">
                                            <input class="form-control" placeholder="Subscribe to Stay Updated" type="email"> <button class="appsLand-btn appsLand-btn-gradient subscribe-btn"><span>Subscribe</span></button>
                                            <div class="clearfix"></div></a>
                                        </div><a class="appsLand-btn appsLand-btn-gradient btn-inverse scrollLink" href="https://t.me/joinchat/GNbSLAxLtSll3H0yjkpPFw" target="_blank"><span><i aria-hidden="true" class="fa fa-location-arrow"></i> Join Astra Telegram</span></a>
                                    </div>
                                </div>
                            </div>

                    <div class="col-lg-2 col-md-2"></div>

                    </div>
                    
                </div>
            </div>
        </div>
    </div>
</header>

<!-- Main Content
========================================-->
<main class="entry-main">

    <!-- Mini Feature Section
    ========================================-->
    
    <?php echo the_field('content');?>




<div class="sepratebox">
    
    <div class="container">
        
        <div class="row">
            
            <div class="col-lg-6 col-md-6 col-sm-6">
				<?php echo the_field('distribution_of_tokens');?>
            </div>

            <div class="col-lg-6 col-md-6 col-sm-6">
				<?php echo the_field('allocation_of_funds');?>	
            </div>


        </div>

    </div>

</div>


<div class="insturtions">
    
    <div class="container">
        
        <div class="row">
			<?php echo the_field('instructions_for_participating');?>
        </div>
         <div class="site-intro-content">
                                   
                                    
                                    <ul class="list-inline list-unstyled header-links">
                                        <li class="wow fadeInUp" data-wow-delay="0.5s" data-wow-duration="1s">
                                            <a class="appsLand-btn appsLand-btn-gradient btn-inverse scrollLink" href="http://goastra.network/assets/Astra-Whitepaper.pdf"><span>Whitepaper&nbsp;</span></a>
                                        </li>
                                        <li class="wow fadeInUp" data-wow-delay="0.75s" data-wow-duration="1s">
                                            <a class="appsLand-btn appsLand-btn-gradient btn-inverse scrollLink" data-aos="fade-right" data-target="#pop" data-toggle="modal" href="#"><span><i aria-hidden="true" class="fa fa-location-arrow"></i> Join the Whitelist/Join</span></a>
                                        </li>
                                        <li class="wow fadeInUp" data-wow-delay="0.75s" data-wow-duration="1s">
                                            <a class="appsLand-btn appsLand-btn-gradient btn-inverse scrollLink" href="<?php echo bloginfo('template_url');?>/assests/Astra - Terms of Token Sale - 180108.pdf"><span><i aria-hidden="true" class="fa fa-check-circle"></i>Terms of Token Sale</span></a>
                                        </li>
                                    </ul>
                                    <div class="clearfix"></div>
                                    <div class="signupfrm2">
                                        <div class="custom-input-group wow fadeInUp smlht" data-wow-delay="0.25s" data-wow-duration="1s">
                                            <a href="https://astranetix.us16.list-manage.com/subscribe/post?u=cbdcc4d7bc5aed8237a9c0b53&id=f4e6f97e1a">
                                            <input class="form-control" placeholder="Subscribe to Stay Updated" type="email"> <button class="appsLand-btn appsLand-btn-gradient subscribe-btn"><span>Subscribe</span></button>
                                            <div class="clearfix"></div></a>
                                        </div><a class="w-38 appsLand-btn appsLand-btn-gradient btn-inverse scrollLink m-left-6" href="https://t.me/joinchat/GNbSLAxLtSll3H0yjkpPFw" target="_blank"><span><i aria-hidden="true" class="fa fa-location-arrow"></i> Join Astra Telegram</span></a>
                                      <!--  <a class="appsLand-btn appsLand-btn-gradient btn-inverse scrollLink" href="https://t.me/joinchat/GNbSLAxLtSll3H0yjkpPFw" target="_blank"><span> Terms of Token Sale</span></a>-->
                                    </div>
                                </div>

    </div>

</div>


    <!-- ScreenShots Section
    ========================================-->
    
         



    <!-- Features Section
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
  
</main>

<!-- Option Template Menu
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
