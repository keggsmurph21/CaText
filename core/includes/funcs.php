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

  global $tiles;
  $tiles = get_setting('tiles');
  shuffle($tiles);
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

  $x = x($center) + $size * cos($rad);
  $y = y($center) + $size * sin($rad);

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
function hex_equal($a, $b, $dist=0.001) {
  if (abs(x($a) - x($b)) < $dist) { return false; }
  if (abs(y($a) - y($b)) < $dist) { return false; }
  if (abs(z($a) - z($b)) < $dist) { return false; }

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
 function pt_equal($a, $b, $dist=0.001) {
   if (pt_dist($a, $b) < $dist) {
     return true;
   }

   return false;
 }

function pt_dist($a, $b) {
  $dx = x($a) - x($b);
  $dy = y($a) - y($b);
  return sqrt(pow($dx,2) + pow($dy,2));
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

/**
 *
 */
function hex_to_pt($hex, $size) {
  $x = $size * (x($hex) - y($hex)) * sqrt(3)/2;
  $y = $size * z($hex) * -1.5;
  return Pt($x,$y);
}

function is_node_in_list($node, $nodes, $dist=0.0001) {
  foreach ($nodes as $n) {
    if (pt_dist($node, $n) < $dist) {
      return true;
    }
  }

  return false;
}

/**
 * given two hexes, will return true if they are adjacent and false if not
 */
function is_neighbor($a, $b) {
  global $hex_dirs;

  foreach ($hex_dirs as $dir) {
    if (pt_equal( pt_add($a, $dir), $b )) {
      return true;
    }
  }

  return false;
}

function get_hex_id($hex, $hexes) {
  // count number of neighbors.. anything less than 6 is an ocean spot
  $neighbors = 0;

  foreach ($hexes as $h) {
    if (is_neighbor($hex, $h)) {
      $neighbors++;
    }
  }

  if ($neighbors < 6) {
    return 'ocean';
  } else {
    global $tiles;
    return array_pop($tiles);
  }
}

function echo_hexagon($id, $pt, $size, $points) {
  echo '<polygon class="hex" id="' . $id . '" points="';
  for ($i=0; $i<6; $i++) {
    $node = get_hex_corner($pt, $size, $i);
    echo x($node) . ' ' . y($node) . ' ';
  }
  echo '" />';
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

  foreach ($hexes as $hex) {
    $x = x(hex_to_pt($hex,1));
    if ($x < $min_x) { $min_x = $x; }
    if ($x > $max_x) { $max_x = $x; }

    $y = y(hex_to_pt($hex,1));
    if ($y < $min_y) { $min_y = $y; }
    if ($y > $max_y) { $max_y = $y; }
  }

  $width = get_setting('board_container_width');
  $height = get_setting('board_container_height');

  $size = min($width / (2 + $max_x - $min_x), $height / (2 + $max_y - $min_y));

  // update hex directions to points
  global $hex_dirs;
  $tmp = [];
  foreach ($hex_dirs as $dir) {
    $tmp[] = hex_to_pt($dir, $size);
  }
  $hex_dirs = $tmp;

  // create and draw the hexagons
  $ctr = Pt($width/2, $height/2);
  $cntrs = [];
  $cntr_nodes = [];
  $nodes = [];

  foreach ($hexes as $hex) {
    $pt = hex_to_pt($hex, $size);
    $pt = pt_add($pt, $ctr);
    $cntrs[] = $pt;

    for ($i=0; $i<6; $i++) {
      $node = get_hex_corner($pt, $size, $i);
      $tmp[] = $node;
      if (!is_node_in_list($node, $nodes)) {
        $nodes[] = $node;
      }
    }

    array_push($cntr_nodes, $tmp);
  }

  for ($i=0; $i<count($cntrs); $i++) {
    $id = get_hex_id($cntrs[$i], $cntrs);
    echo_hexagon($id, $cntrs[$i], $size, $cntr_nodes[$i]);
  }

  // create and draw the lines

  echo count($nodes);
}
?>
