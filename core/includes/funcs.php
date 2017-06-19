<?php
/**
 * Open up the .ini file and read contents, save to $settings file.  Defaults
 * to initializing a standard Catan game.
 */
function init_settings($file, $flavor='standard') {
  global $settings;
  $settings = [];

  $defaults = parse_ini_file($file);
  foreach ($defaults as $setting=>$value) {
    $settings[$setting] = $value;
  }

  $settings['flavor'] = $flavor;
}

/**
 *
 */
function get_setting($setting, $default=FALSE) {
  global $settings;

  if (isset($settings[$setting])) {
    return $settings[$setting];
  }

  return $default;
}

/**
 *
 */
function get_media_file($filename='') {
  if (!strlen($filename)){ return FALSE; }

  $filepath = 'resources/' . $filename;
	if (file_exists($filepath)){
		return $filepath;
	}
	return FALSE;;
}

/**
 *
 */
function get_layout_file($filename='') {
  if (!strlen($filename)){ return FALSE; }

  $filepath = 'setup/' . get_setting('flavor') . '/' . $filename;
	if (file_exists($filepath)){
		return $filepath;
	}
	return FALSE;;
}

/**
 *  i=0 is the top right corner (2:00), iterate counterclockwise
 */
function get_hex_corner($center, $size, $i) {
  $deg = 60 * $i + 30;
  $rad = pi() / 180.0 * $deg;
  return array( 'x' => $center['x'] + $size * cos($rad), 'y' => $center['y'] + $size * sin($rad) );
}

function get_hex($center, $size) {
  $hexagon = array();
  for ($i=0; $i<6; $i++) {
    $hexagon[] = get_hex_corner($center, $size, $i);
  }
  return $hexagon;
}

?>
