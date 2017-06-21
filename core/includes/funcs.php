<?php
/******************
 *
 * FUNCS.php >>> php functions accessible to every page on the site
 *
 ******************/



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
}

/**
 * returns the value of a setting from the ini or json initialization file
 */
function get_setting($setting, $default=FALSE) {
  global $settings;

  if (isset($settings[$setting])) {
    return $settings[$setting];
  }

  return $default;
}

/**
 * returns the full path to a media file (in resources/)
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
 * returns the full path to a setup file (in setup/)
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
 * returns a Hex object
 */
function Hex($x, $y, $z) {
  return array('x'=>$x, 'y'=>$y, 'z'=>$z);
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
 *  i=0 is the bottom right corner (4:00), iterate clockwise
 */
function get_hex_corner($center, $size, $i) {
  $deg = 60 * $i + 30; $rad = pi() / 180.0 * $deg;

  $x = x($center) + $size * cos($rad);
  $y = y($center) + $size * sin($rad);

  return Pt($x, $y);
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
 * determines whether two Pt objects have the same coordinates (w/in $dist)
 */
function pt_equal($a, $b, $dist=0.001) {
   if (pt_dist($a, $b) < $dist) {
     return true;
   }

   return false;
}

/**
 * returns the triangular distance between two Pt objects
 */
function pt_dist($a, $b) {
  $dx = x($a) - x($b);
  $dy = y($a) - y($b);
  return sqrt(pow($dx,2) + pow($dy,2));
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
 * transforms a Hex object into a Pt object for rendering
 */
function hex_to_pt($hex, $size) {
  $x = $size * (x($hex) - y($hex)) * sqrt(3)/2;
  $y = $size * z($hex) * -1.5;
  return Pt($x,$y);
}

/**
 * transforms a Pt object into a Hex object for computation
 */
function pt_to_hex($pt, $size) {
  $z = y($pt) / $size * -2.0 / 3.0;
  $y = x($pt) / $size * -1.0 / sqrt(3.0) - $z / 2.0;
  $x = - ($y + $z);
  return Hex($x,$y,$z);
}

/**
 * given two (Pt) objs, will return true if they are $dist away and false if not
 */
function is_neighbor($a, $b, $dist, $margin=0.001) {
  if (pow(pt_dist($a, $b) - $dist, 2) < $margin) {
    return true;
  }

  return false;
}

/**
 * returns whether a given object is on the edge of the hexes
 * ( helper function for setup_board() )
 */
function is_edge_hex($hex, &$min_x, &$max_x, &$min_y, &$max_y, &$min_z, &$max_z) {
  $x = x($hex); $y = y($hex); $z = z($hex);

  if ( $x == $min_x || $x == $max_x || $y == $min_y || $y == $max_y || $z == $min_z || $z == $max_z) {
    return true;
  } else {
    return false;
  }
}

/**
 * outputs the HTML code for either a roll chip or a robber, depending on the
 * value of a given object's $roll
 */
function echo_roll_chip($hex) {
  $x = x($hex['pt']);
  $y = y($hex['pt']);

  if ($hex['roll'] != 0) {
    // only place a chip if this hex yields resources
    $color = 'black';
    if ($hex['roll'] == 6 || $hex['roll'] == 8) {
      $color = 'red';
    }
    echo '<circle class="roll_chip" cx="' . $x . '" cy="' . $y . '" r="15"> </circle>';
    echo '<text class="roll" x="' . $x . '" y="' . $y . '" fill="' . $color . '">';
      echo $hex['roll'];
    echo '</text>';
  } else {
    // otherwise place a robber on the hex
    echo '<g class="robber">';

      echo '<circle class="shadow" cx="' . $x . '" cy="' . ($y-7) . '" r="8"> </circle>';
      echo '<polygon class="shadow" points="' . $x . ' ' . ($y-8)  . ' ';
      echo ($x-12) . ' ' . ($y+15) . ' ' . ($x+12) . ' ' . ($y+15) . '"> </polygon>';

      echo '<circle cx="' . $x . '" cy="' . ($y-7) . '" r="7"> </circle>';
      echo '<polygon points="' . $x . ' ' . ($y-7)  . ' ';
      echo ($x-10) . ' ' . ($y+14) . ' ' . ($x+10) . ' ' . ($y+14) . '"> </polygon>';

    echo '</g>';
  }
}

/**
 * outputs the HTML code for all of the objects that get rendered server-side, including
 * hexes, edges, and nodes
 */
function echo_objects(&$data) {
  $style = get_setting('background_style');

  // print the ocean hexes first
  foreach ($data['hexes'] as $hex) {
    if ($hex['type'] == 'ocean') {
      echo '<polygon class="hex" id="' . 'ocean-' . $style . '" points="';
      foreach ($hex['points'] as $p) {
        echo x($data['nodes'][$p]['pt']) . ' ';
        echo y($data['nodes'][$p]['pt']) . ' ';
      }
      echo '"> </polygon>';
    }
  }

  // then the resource hexes
  foreach ($data['hexes'] as $hex) {
    if ($hex['type'] != 'ocean') {
      echo '<polygon class="hex" id="' . $hex['type'] . '-' . $style . '" points="';
      foreach ($hex['points'] as $p) {
        echo x($data['nodes'][$p]['pt']) . ' ';
        echo y($data['nodes'][$p]['pt']) . ' ';
      }
      echo '"> </polygon>';
      echo_roll_chip($hex);
    }
  }

  // then the edges
  foreach ($data['edges'] as $edge) {
    echo '<line class="edge" x1="' . x($edge['pts'][0]) . '" y1="' . y($edge['pts'][0]);
    echo '" x2="' . x($edge['pts'][1]) . '" y2="' . y($edge['pts'][1]) . '" > </line>';
  }

  // and finally the nodes (if set to display)
  if (get_setting('display_nodes')) {
    foreach ($data['nodes'] as $node) {
      if ($node['type'] != 'ocean') {
        echo '<circle class="node" cx="' . x($node['pt']) . '" cy="' . y($node['pt']) . '" stroke="black" stroke-width="2" fill="white" r="5"> </circle>';
      }
    }
  }
}

/**
 * add a node to the $data array, perform various other related operations
 */
function append_node(&$data, $node, $hex_id) {
  $new_node = array('i'=>'', 'coords'=>pt_to_hex($node,$data['size']),
    'pt'=>$node, 'hexes'=>array($hex_id), 'type'=>'ocean');
  $index = false;

  for ($n=0; $n<$data['node_count']; $n++) {
    if (pt_dist($node, $data['nodes'][$n]['pt']) < 0.001) {
      $index = $n;
    }
  }

  if ($index === false) {

    if ($data['hexes'][$hex_id]['type'] != 'ocean') {
      $new_node['type'] = 'land';
    }

    $new_node['i'] = $data['node_count'];
    array_push($data['nodes'], $new_node);
    array_push($data['hexes'][$hex_id]['points'], $data['node_count']);

    $data['node_count']++;

  } else {

    if ($data['nodes'][$index]['type'] == 'ocean') {
      if ($data['hexes'][$hex_id]['type'] != 'ocean') {
        $data['nodes'][$index]['type'] = 'land';
      }
    }

    array_push($data['nodes'][$index]['hexes'], $hex_id);
    array_push($data['hexes'][$hex_id]['points'], $index);

  }
}

/**
 * add a node to the $data array, perform various other related operations
 */
function append_edge(&$data, $a, $b) {
  $new_edge = array('i'=>'', 'pts'=>array(), 'pt_ids'=>array());
  $pts = array($a['pt'], $b['pt']);
  $alt  = array($b['pt'], $a['pt']);

  $match = false;

  foreach ($data['edges'] as $edge) {
    if ( pt_equal($edge['pts'][0], $pts[0]) && pt_equal($edge['pts'][1], $pts[1]) ) {
      $match = true;
    }
    if ( pt_equal($edge['pts'][0], $alt[0]) && pt_equal($edge['pts'][1], $alt[1]) ) {
      $match = true;
    }
  }

  if (!$match) {
    $new_edge['i'] = $data['edge_count'];
    $new_edge['pts'] = $pts;
    $new_edge['pt_ids'] = array($a['i'], $b['i']);
    array_push($data['edges'], $new_edge);

    $data['edge_count']++;
  }
}

/**
 * iterates over all the hexes and returns an array of all those hexes
 * which neighbor a given hex.. if $filter_oceans==true, return only those
 * hexes of type!='ocean'
 */
function hex_get_neighbors(&$data, $hex, $filter_oceans=false) {
  $neighbors = array();

  // iterate over all the hexes and check each one
  foreach ($data['hexes'] as $h) {
    $dist = pt_dist($h['pt'], $hex['pt']);
    if ($dist < 2*$data['size'] && $dist > 0) {
      if ($filter_oceans) {
        if ($h['type'] != 'ocean') {
          array_push($neighbors, $h);
        }
      } else {
        array_push($neighbors, $h);
      }
    }
  }

  return $neighbors;
}

/**
 * iterates over the board to make sure a red hex is not adjacent to another
 * red hex or to two 4-dot hexes
 */
function validate_board(&$data) {
  foreach ($data['nodes'] as $node) {

    $tension = 0;
    foreach ($node['hexes'] as $hex_id) {

      $hex = $data['hexes'][$hex_id];
      if ($hex['roll'] == 6 || $hex['roll'] == 8) {
        $tension += 0.5;
      }
      if ($hex['roll'] == 5 || $hex['roll'] == 9) {
        $tension += 0.25;
      }

      if ($tension >= 1.0) {
        return false;
      }
    }
  }

  return true;
}

/**
 * most important function that outputs HTML code for all of the objects on the game board
 */
function setup_board() {

  // default to not valid board arrangement
  $valid = false;

  // continuously attempt to setup the board until we achieve a valid configuration
  while (!$valid) {

    // delete the $data from old attempts
    unset($data);

    // to store most of the variables, pass around references to it
    $data = array('dirs'=>array(), 'tiles'=>array(), 'hexes'=>array(),
      'pts'=>array(), 'nodes'=>array(), 'edges'=>array(), 'hex_count'=>0,
      'node_count'=>0, 'edge_count'=>0);

    // set up the valid directions (in hex coords)
    $dirs = [[-1,1,0], [0,1,-1], [1,0,-1], [1,-1,0], [0,-1,1], [-1,0,1]];
    foreach ($dirs as $dir) {
      array_push($data['dirs'], Hex($dir[0], $dir[1], $dir[2]));
    }

    // load the board shape
    $board_shape = get_setting('board_shape');
    if (!$board_shape) {
      throw new Exception('Unable to load board.');
    }

    // convert basic arrays into Hex() objects
    $hexes = parse_hex_coordinates($board_shape);

    // get min and max values in each coordinate direction
    $min_x = 0; $max_x = 0;
    $min_y = 0; $max_y = 0;
    $min_z = 0; $max_z = 0;

    // and each pixel direction
    $min_width = 0; $max_width = 0;
    $min_height= 0; $max_height= 0;

    foreach ($hexes as $hex) {
      $data['hex_count']++; // iterate the hex counter

      if (x($hex) < $min_x) { $min_x = x($hex); }
      if (x($hex) > $max_x) { $max_x = x($hex); }

      if (y($hex) < $min_y) { $min_y = y($hex); }
      if (y($hex) > $max_y) { $max_y = y($hex); }

      if (z($hex) < $min_z) { $min_z = z($hex); }
      if (z($hex) > $max_z) { $max_z = z($hex); }

      $x = x(hex_to_pt($hex,1));
      if ($x < $min_width) { $min_width = $x; }
      if ($x > $max_width) { $max_width = $x; }

      $y = y(hex_to_pt($hex,1));
      if ($y <$min_height) { $min_height= $y; }
      if ($y >$max_height) { $max_height= $y; }
    }

    // calculate the size (radius) of each hexagon based on number of hexes & container size
    $width = get_setting('board_container_width');
    $height= get_setting('board_container_height');
    $center = Pt($width/2.0, $height/2.0);

    $data['size'] = min($width / (2 + $max_width - $min_width), $height/ (2 + $max_height-$min_height));

    // load and shuffle the resource tiles
    $data['tiles'] = get_setting('tiles');
    shuffle($data['tiles']);

    // and do the same for the dicerolls
    $data['dicerolls'] = get_setting('dicerolls');
    shuffle($data['dicerolls']);

    // and again for harbors
    $data['harbors'] = get_setting('harbors');
    shuffle($data['harbors']);

    // reset a local counter
    $count = 0;

    // add data to each hex object and create the nodes
    foreach ($hexes as $hex) {

      $h = array('i'=>$count, 'type'=>'', 'roll'=>0);

      if (is_edge_hex($hex, $min_x, $max_x, $min_y, $max_y, $min_z, $max_z)) {
        $h['type'] = 'ocean';
      } else {
        $h['type'] = array_pop($data['tiles']);
        if ($h['type'] != 'desert') {
          $h['roll'] = array_pop($data['dicerolls']);
        }
      }

      $h['coords'] = $hex;
      $h['pt'] = pt_add($center, hex_to_pt($hex, $data['size']));
      $h['points'] = array();

      array_push($data['hexes'], $h);

      for ($i=0; $i<6; $i++) {
        $node = get_hex_corner($h['pt'], $data['size'], $i);
        append_node($data, $node, $count);
      }

      $count++;
    }

    // create the edges
    foreach ($data['nodes'] as $node) {
      if ($node['type'] != 'ocean') { // no edges should extend into the ocean
        foreach ($data['nodes'] as $candidate) {
          if ($candidate['type'] != 'ocean') {
            if (is_neighbor($node['pt'], $candidate['pt'], $data['size'])) {
              append_edge($data, $node, $candidate);
            }
          }
        }
      }
    }

    $valid = validate_board($data);
  }

  echo_objects($data);

}
?>
