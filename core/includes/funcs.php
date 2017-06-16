<?php
/**
 * Open up the .ini file and read contents, save to $settings file
 */
function init_settings($file) {
  global $settings;

  $defaults = parse_ini_file($file);
  foreach ($defaults as $setting=>$value) {
    $settings->{$setting} = $value;
  }
}

/**
 *
 */
function get_setting($setting, $default=FALSE) {
  global $settings;

  if (isset($settings->{$setting})) {
    return $settings->{$setting};
  }

  return $default;
}
?>
