<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://codex.wordpress.org/Editing_wp-config.php
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', 'wordpress');

/** MySQL database username */
define('DB_USER', 'root');

/** MySQL database password */
define('DB_PASSWORD', 'Jasper20#');

/** MySQL hostname */
define('DB_HOST', 'localhost');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         '6$X+C!9<cj8N>|w%M[Y{a0r]yMasxX|.icR1 ~_8%&<t8S_R2H[JxP]N&rE2lQ][');
define('SECURE_AUTH_KEY',  'W11`-(Q+.s)@V^-GEa8+V*[4Yl O(lp&E0X;TB;5F-wDM,GFItbc$;f(1Ft3-Epf');
define('LOGGED_IN_KEY',    'n+vR#.k{dc8i3N*B$2.RQ<e]N==ppiOW^Fn}ghqDQpAKkxDN4m0aI-v+Tj=,V4%q');
define('NONCE_KEY',        '06K0hEIj2 urxxe9qiK!iEzLv_:EPl&K>Ki=>$M4M~z9[Mo%w>s0pHdX8DBQ}qPT');
define('AUTH_SALT',        '>l>6{Z!f97%WhtE++sI8MW7_}Z.$F-~xlZ  I8P(O?HtUuWdwZW4eP|8Ab?]Q-e-');
define('SECURE_AUTH_SALT', '<QLZb uqM_:2`IT$uAno4xy*InBX6h+d|$v@,PR Lr|2/6,-^`vnv|q?~[lQ|.|;');
define('LOGGED_IN_SALT',   '3wQEvaYaL).4,utY+r8Vu! lGrQ)YN{2RgCNm*?-O;g2v)}?06+,vl^VM%/lbGNp');
define('NONCE_SALT',       '# M@T(6AZzzVZ;P+tq#2OBIIS*58+vv,+SNp`QTj6Lh9w]b_(-pJ3%n#PQV+-;jg');

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the Codex.
 *
 * @link https://codex.wordpress.org/Debugging_in_WordPress
 */
define('WP_DEBUG', false);

/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
	define('ABSPATH', dirname(__FILE__) . '/');

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');
