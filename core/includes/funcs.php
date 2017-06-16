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
  var_dump($settings);
  echo get_setting('flavor');
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
	if (file_exists('resources/' . $filename)){
		return 'resources/' . $filename;
	}
	return FALSE;;
}

/**
 *
 */
function get_layout_file($filename='') {
  if (!strlen($filename)){ return FALSE; }
  $filepath = 'setup/' . get_setting('flavor') . '/' . $filename;
  echo $filepath;
	if (file_exists($filepath)){
		return $filepath;
	}
	return FALSE;;
}
?>
