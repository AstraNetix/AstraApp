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
define('DB_NAME', 'astradb');

/** MySQL database username */
define('DB_USER', 'astradb');

/** MySQL database password */
define('DB_PASSWORD', 'Word1@presS');

/** MySQL hostname */
define('DB_HOST', 'localhost');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8mb4');

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
define('AUTH_KEY',         '3psq7dmnvhqnkbm1rdqsg9ixzrpurzhrultgkfyqknec8yxspke1lepyfaoddbps');
define('SECURE_AUTH_KEY',  'gtihcopcqnpz2jvbjx2ikzrgrsnh9avxm1yd8dn6wxucqghpwnxuqjedlzbx67vo');
define('LOGGED_IN_KEY',    '7p26df7hkgymgzioswnzlnjczsoo0tu4o7ew9ybxtro5jmf5fzt1h4bt48mh2jbq');
define('NONCE_KEY',        '7bjyjsbdorjawemc2kef0reo8zbtwqnows1intxo5pxuxntw5duubetmkgvbfdeb');
define('AUTH_SALT',        'kmmwxdlyi0n9hqiz540lm66rkyxi2ibhpp4fjiatcymgpcbyaok9dedtwcl7t0zq');
define('SECURE_AUTH_SALT', '4ezw6suldib2z18xufentv9gegtmffmdqyd8mnsxq8ovg801qbvdlbrb9iuujp8o');
define('LOGGED_IN_SALT',   'gul8fodceuu7taa5n8x5dkci3bq1axujffqcj4ekjkdpsoqpuoytjdu9di5nivbg');
define('NONCE_SALT',       'gw7zr64jv7nlctpzkzjqn86jule0wqonuywtmkly10teg1pbvvsjgfvrnqtwxydk');

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'wpot_';

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
