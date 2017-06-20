<?php
/**
 * Open up the .ini file and read contents, save to $settings file.  Defaults
 * to initializing a standard Catan game.
 */
function init_settings($path, $flavor='standard') {
  global $settings;
  $settings = [];

  $ini = $path . 'settings.ini';
  $defaults = parse_ini_file($ini);
  foreach ($defaults as $setting=>$value) {
    $settings[$setting] = $value;
  }

  $json = file_get_contents($path.'board.json');
  $defaults = json_decode($json, true);
  foreach ($defaults as $setting=>$value) {
    $settings[$setting] = $value;
  }

  $settings['flavor'] = $flavor;

  // make some more global variables
  global $hex_dirs;
  $hex_dirs = [];
  $dirs = [[-1,1,0], [0,1,-1], [1,0,-1], [1,-1,0], [0,-1,1], [-1,0,1]];

  foreach ($dirs as $dir) {
    $hex_dirs[] = Hex($dir[0], $dir[1], $dir[2]);
  }
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
  $deg = 60 * $i + 30; $rad = pi() / 180.0 * $deg;

  $x = $center['x'] + $size * cos($rad);
  $y = $center['y'] + $size * sin($rad);

  return Pt($x, $y);
}

/**
 * returns an array of the six corners surrounding the hex centerpoint
 */
function get_hex($center, $size) {
  $hexagon = array();
  for ($i=0; $i<6; $i++) {
    $hexagon[] = get_hex_corner($center, $size, $i);
  }
  return $hexagon;
}

/**
 * given two hexes, will return true if they are adjacent and false if not
 */
function hex_hex_is_neighbor($a, $b) {
  global $hex_directions;

  foreach ($hex_dirs as $dir) {
    if (hex_equal( hex_add($a, $dir), $b )) {
      return true;
    }
  }

  return false;
}

/**
 * returns a Hex object
 */
function Hex($x, $y, $z) {
  return array('x'=>$x, 'y'=>$y, 'z'=>$z);
}

/**
 * returns the sum of two Hex objects
 */
function hex_add($a, $b) {
  $x = x($a) + x($b);
  $y = y($a) + y($b);
  $z = z($a) + z($b);
  return Hex($x, $y, $z);
}

/**
 * determines whether two Hex objects have the same coordinates
 */
function hex_equal($a, $b) {
  if (x($a) != x($b)) { return false; }
  if (y($a) != y($b)) { return false; }
  if (z($a) != z($b)) { return false; }

  return true;
}

/**
 * returns a Pt (Point) object
 */
function Pt($x, $y) {
  return array('x'=>$x, 'y'=>$y);
}

/**
 * returns the sum of two Pt objects
 */
function pt_add($a, $b) {
  $x = x($a) + x($b);
  $y = y($a) + y($b);
  return Pt($x, $y);
}

/**
 * determines whether two Pt objects have the same coordinates
 */
function pt_equal($a, $b) {
  if (x($a) != x($b)) { return false; }
  if (y($a) != y($b)) { return false; }

  return true;
}

/**
 * takes array of hex coordinates and returns an array of Hex objects
 */
function parse_hex_coordinates($hex_coords) {
  $hexes = [];

  foreach ($hex_coords as $hex_coord) {
    $hexes[] = Hex( $hex_coord[0], $hex_coord[1], $hex_coord[2] );
  }

  return $hexes;
}

/**
 * returns the x-coordinate of an object
 */
function x($obj) {
  return $obj['x'];
}

/**
 * returns the y-coordinate of an object
 */
function y($obj) {
  return $obj['y'];
}

/**
 * returns the z-coordinate of an object
 */
function z($obj) {
  return $obj['z'];
}

function hex_to_pt($hex, $size) {
  $x = $size * (x($hex) - y($hex));
  $y = $size * z($hex) * sqrt(3);
  return Pt($x,$y);
}

/**
 *
 */
function setup_board() {
  $hexes = get_setting('board_shape');
  if (!$hexes) {
    throw new Exception('Unable to load board.');
  }

  $hexes = parse_hex_coordinates($hexes);

  // determine how many hexes we have in each direction (ni=max in i direction)
  $min_x = 0; $max_x = 0;
  $min_y = 0; $max_y = 0;
  $min_z = 0; $max_z = 0;

  foreach ($hexes as $hex) {
    $x = x($hex); $y = x($hex); $z = x($hex);
    if ($x < $min_x) { $min_x = $x; } if ($x > $max_x) { $max_x = $x; }
    if ($y < $min_y) { $min_y = $y; } if ($y > $max_y) { $max_y = $y; }
    if ($z < $min_z) { $min_z = $z; } if ($z > $max_z) { $max_z = $z; }
  }

  $nx = $max_x - $min_x; $ny = $max_y - $min_y; $nz = $max_z - $min_z;

  $width = get_setting('board_container_width');
  $height = get_setting('board_container_height');

  // use the hex-count to determine the max size of each hex against the container
  $size_x = min($width / ($nx * sqrt(3) * 2), $height / (0.5 + 1.5 * $nx));
  $size_y = min($width / ($ny * sqrt(3) * 2), $height / (0.5 + 1.5 * $ny));
  $size_z = min($width / ($nz * sqrt(3) * 2), $height / (0.5 + 1.5 * $nz));

  $size = min($size_x, $size_y, $size_z);
  echo $size;

  $ctr = Pt($width/2, $height/2);
  $pts = [];

  foreach ($hexes as $hex) {
    $pt = hex_to_pt($hex, $size);
    $pt = pt_add($pt, $ctr);
    echo '<circle cx="' . x($pt) . '" cy="' . y($pt) . '" r="5" fill="black">';
    echo '</circle>';
    for ($i=0; $i<6; $i++) {
      $v = get_hex_corner($pt, $size, $i);
      echo '<circle cx="' . x($v) . '" cy="' . y($v) . '" r="1" fill="black">';
      echo '</circle>';
    }
  }
}
?>
