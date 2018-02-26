<?php
/**
 * The template for displaying the footer
 *
 * Contains the closing of the "site-content" div and all content after.
 *
 * @package WordPress
 * @subpackage Twenty_Fifteen
 * @since Twenty Fifteen 1.0
 */
?>

	</div><!-- .site-content -->

<footer class="apps-footer">
        <div class="footer-bottom">
            <div class="container">
                <p>Copyright © Astranetix 2017</p>
            </div>
        </div>
    </footer>
	<!-- start the script -->
    <script src="<?php echo bloginfo('template_url');?>/js/jquery-2.2.4.min.js">
    </script> 
    <script src="<?php echo bloginfo('template_url');?>/js/bootstrap.min.js">
    </script> 
    <script src="<?php echo bloginfo('template_url');?>/js/swiper.jquery.min.js">
    </script> 
    <script src="<?php echo bloginfo('template_url');?>/js/wow.min.js">
    </script> 
    <script src="<?php echo bloginfo('template_url');?>/js/jquery.countTo.min.js">
    </script> 
    <script src="<?php echo bloginfo('template_url');?>/js/lity.min.js">
    </script> 
    <script src="<?php echo bloginfo('template_url');?>/js/plugins.js">
    </script> 
    <script src="<?php echo bloginfo('template_url');?>/js/particles.js">
    </script> 
    <script src="<?php echo bloginfo('template_url');?>/js/app.js">
    </script> 
    <script>
     var count_particles, stats, update;
     stats = new Stats;
     stats.setMode(0);
     stats.domElement.style.position = 'absolute';
     stats.domElement.style.left = '0px';
     stats.domElement.style.top = '0px';
     document.body.appendChild(stats.domElement);
     count_particles = document.querySelector('.js-count-particles');
     update = function() {
       stats.begin();
       stats.end();
       if (window.pJSDom[0].pJS.particles && window.pJSDom[0].pJS.particles.array) {
         count_particles.innerText = window.pJSDom[0].pJS.particles.array.length;
       }
       requestAnimationFrame(update);
     };
     requestAnimationFrame(update);
    </script> <!-- end the script -->
    
<!-- Modal -->
<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title" id="myModalLabel">Presentation</h4>
      </div>
      <div class="modal-body">
       <iframe src="assests/Astra-Introduction.pdf" width="100%" height="600"></iframe>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>

<?php wp_footer(); ?>

</body>
</html>
